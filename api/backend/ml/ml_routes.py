from flask import Blueprint, jsonify
from backend.db_connection import db
from backend.ml_models.cosine_similarity import get_similar
from backend.ml_models.regression import dataframe
from backend.ml_models.regression import predict
from backend.ml_models.regression import create_xy_full
from backend.ml_models.regression import create_xy_select
from backend.ml_models.regression import autoreg_train
from backend.ml_models.regression import autoreg_predict_full
from backend.ml_models.regression import add_predict
from backend.ml_models.regression import predict_using_stored_autoreg
import pandas as pd
import json



ml = Blueprint("ml", __name__)

# Modified ml.py route for regression with storage

@ml.route("/regression/<input>", methods=["GET"])
def regression(input):
    inputs = [str(x.strip()) for x in input.split(',')]
    result = predict(dataframe(inputs[1]), inputs[0])
    print("Country received:", inputs[0])
    
    # NEW: Store regression weights in database
    try:
        cursor = db.get_db().cursor()
        
        # First, get the factorID for this data code
        factor_query = """
            SELECT factorID FROM RegressionFactors 
            WHERE who_code = %s OR factor_code = %s
        """
        cursor.execute(factor_query, (inputs[1], inputs[1]))
        factor_result = cursor.fetchone()
        
        if factor_result:
            factor_id = factor_result['factorID']
        else:
            # If factor doesn't exist, create it
            insert_factor = """
                INSERT INTO RegressionFactors (factor_code, who_code, table_name) 
                VALUES (%s, %s, %s)
            """
            # Map data codes to table names
            table_mapping = {
                'HFA_16': 'LiveBirths',
                'HFA_570': 'HealthExpend',
                'HLTHRES_67': 'GenPractitioners',
                # Add other mappings as needed
            }
            table_name = table_mapping.get(inputs[1], 'Unknown')
            cursor.execute(insert_factor, (inputs[1], inputs[1], table_name))
            factor_id = cursor.lastrowid
        
        # Check if regression weights already exist for this country/factor/user
        check_query = """
            SELECT id FROM RegressionWeights 
            WHERE country = %s AND factorID = %s AND userID = %s
        """
        # Assuming userID = 1 for now, modify as needed
        user_id = 1
        cursor.execute(check_query, (inputs[0], factor_id, user_id))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing weights
            update_query = """
                UPDATE RegressionWeights 
                SET slope = %s, intercept = %s, mse = %s, r2 = %s
                WHERE id = %s
            """
            cursor.execute(update_query, (
                result['slope'], 
                result['intercept'], 
                result['mse'], 
                result['r2'],
                existing['id']
            ))
        else:
            # Insert new weights
            insert_query = """
                INSERT INTO RegressionWeights 
                (country, slope, intercept, mse, r2, factorID, userID)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                inputs[0],
                result['slope'],
                result['intercept'],
                result['mse'],
                result['r2'],
                factor_id,
                user_id
            ))
        
        db.get_db().commit()
        cursor.close()
        
    except Exception as e:
        print(f"Error storing regression weights: {e}")
        db.get_db().rollback()

    return jsonify(result)


#model calls post to put weights in database
# adds new regression weight from model to database
@ml.route("/autoregressive/<chosen_country>/<data_code>/<chosen_year>", methods=["GET"])
def autoregressive(chosen_country, data_code, chosen_year):
    cursor = db.get_db().cursor()
    
    # Get data based on data_code
    if data_code == 'HFA_16':
        query = """SELECT * FROM LiveBirths"""
    elif data_code == 'HFA_570':
        query = """SELECT * FROM HealthExpend"""
    elif data_code == 'HLTHRES_67':
        query = "SELECT * FROM GenPractitioners"
    
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convert to DataFrame
    columns = ["COUNTRY", "YEAR", "VALUE"]
    df = pd.DataFrame(rows, columns=columns)
    value_list = []
    for value in df["VALUE"]:
        value_list.append(float(value))
    
    df["VALUE"] = value_list
    
    inputs = [chosen_country, data_code, chosen_year]
    df_country = df[df['COUNTRY'] == inputs[0]]
    df_filtered = df_country.reset_index(drop=True)
    
    year = int(df_filtered.iloc[len(df_filtered) - 1]['YEAR'])
    years = int(inputs[2]) - year
    
    input = create_xy_select(df, inputs[0])
    train = create_xy_full(df)
    
    # Get the weight vector from autoregression training
    weight_vector = autoreg_train(train[0], train[1])
    
    # NEW: Store autoregression weights
    try:
        # Get factorID
        factor_query = """
            SELECT factorID FROM RegressionFactors 
            WHERE who_code = %s OR factor_code = %s
        """
        cursor.execute(factor_query, (data_code, data_code))
        factor_result = cursor.fetchone()
        
        if factor_result:
            factor_id = factor_result['factorID']
        else:
            # Create factor if it doesn't exist
            insert_factor = """
                INSERT INTO RegressionFactors (factor_code, who_code, table_name) 
                VALUES (%s, %s, %s)
            """
            table_mapping = {
                'HFA_16': 'LiveBirths',
                'HFA_570': 'HealthExpend',
                'HLTHRES_67': 'GenPractitioners',
            }
            table_name = table_mapping.get(data_code, 'Unknown')
            cursor.execute(insert_factor, (data_code, data_code, table_name))
            factor_id = cursor.lastrowid
        
        user_id = 1  # Or get from session
        
        # Convert numpy array to list for JSON storage
        weight_vector_list = weight_vector.flatten().tolist()
        
        # Check if autoreg weights exist
        check_query = """
            SELECT id FROM AutoregWeights 
            WHERE country = %s AND factorID = %s AND userID = %s
        """
        cursor.execute(check_query, (chosen_country, factor_id, user_id))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing weights
            update_query = """
                UPDATE AutoregWeights 
                SET weight_vector = %s
                WHERE id = %s
            """
            cursor.execute(update_query, (
                json.dumps(weight_vector_list),
                existing['id']
            ))
        else:
            # Insert new weights
            insert_query = """
                INSERT INTO AutoregWeights 
                (country, factorID, userID, weight_vector)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                chosen_country,
                factor_id,
                user_id,
                json.dumps(weight_vector_list)
            ))
        
        db.get_db().commit()
        
    except Exception as e:
        print(f"Error storing autoregression weights: {e}")
        db.get_db().rollback()
    
    # Continue with prediction
    preds = autoreg_predict_full(input[0], input[1], weight_vector, years, train[2])
    result = add_predict(df_country, preds, input[0])
    
    cursor.close()
    
    print("Country received:", inputs[0])
    result_final = result.to_json()
    print("final data frame")
    print(result_final)
    return jsonify(result_final)


@ml.route("/predict_autoreg_fast/<country>/<data_code>/<int:year>/<int:user_id>", methods=["GET"])
def predict_autoreg_fast(country, data_code, year, user_id):
    """
    Fast prediction using stored autoregression weights
    This actually USES the predict_using_stored_autoreg function you imported
    """
    try:
        # This line actually uses the imported function!
        result = predict_using_stored_autoreg(country, data_code, year, user_id)
        return jsonify(result)
    except ValueError as e:
        # No stored weights found
        return jsonify({
            "error": str(e),
            "message": "No stored weights found. Use /autoregressive/ to calculate and store weights first."
        }), 404
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

#Gets the cosine similarity numbers for the chosen country 
@ml.route("/cosine/<chosen_country>/<weights_dict>", methods=["GET"])
def cosine(chosen_country, weights_dict):
# Get DB cursor
    cursor = db.get_db().cursor()

    # Query only relevant columns for year 2021
    query = """
        SELECT 
            country,
            prevention,
            detectReport,
            rapidResp,
            healthSys,
            intlNorms,
            riskEnv
        FROM OverallScore
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convert to DataFrame
    columns = ["country", "prevention", "detectReport", "rapidResp", "healthSys", "intlNorms", "riskEnv"]
    df_unscaled = pd.DataFrame(rows, columns=columns)
    print("UNSCALED ROUTE:", df_unscaled)

    #SCALE THE DATA: 
    ghs_index_2021_factors =df_unscaled[["prevention", "detectReport", "rapidResp", "healthSys", "intlNorms", "riskEnv"]]
    # gets the numeric features for the 6 main categories for ghs_index and standardize them
    df_scaled = ghs_index_2021_factors[["prevention", "detectReport", "rapidResp", "healthSys", "intlNorms", "riskEnv"]]

    for feat in df_scaled.columns:
        df_scaled[feat] = (df_scaled[feat] - df_scaled[feat].mean()) / df_scaled[feat].std()
    print("SCALED ROUTE:", df_scaled)


    weights_vect = []
    #weights_dict_dump = json.dumps(weights_dict) 
    weights_dict2 = json.loads(weights_dict)
    print("THIS IS WEIGHTS DICT 2")
    print(weights_dict2)
    for key in weights_dict2:
        #print("ITERATION 1")
        if key == "Prevention":
            #print("This is prevention")
            #print(weights_dict2[key])
            weights_vect.append(weights_dict2[key])
    for key in weights_dict2:
        if key == "Detection & Reporting":
            weights_vect.append(weights_dict2[key])
    for key in weights_dict2:
        if key == "Rapid Response":
            weights_vect.append(weights_dict2[key])
    for key in weights_dict2:
        if key == "Health System":
            weights_vect.append(weights_dict2[key])
    for key in weights_dict2:
        if key == "International Norms Compliance":
            weights_vect.append(weights_dict2[key])
    for key in weights_dict2:
        if key == "Risk Environment":
            weights_vect.append(weights_dict2[key])
    print(weights_vect)
    df = get_similar(chosen_country, weights_vect, df_unscaled, df_scaled)
    print("Country received:", chosen_country)

    result = df.to_dict()
    return jsonify(result)

# Future routes 
# @ml.route("/cosine/<int:user_id>", methods=["GET"])
# def cosine_for_user(user_id):
#     try:
#         # Step 1: Fetch user weights from the DB
#         cursor = db.get_db().cursor()
#         cursor.execute("""
#             SELECT 
#                 preventionWeight,
#                 detectReportWeight,
#                 rapidRespWeight,
#                 healthSysWeight,
#                 intlNormsWeight,
#                 riskEnvWeight
#             FROM CosineWeights WHERE userID = %s
#         """, (user_id,))
#         row = cursor.fetchone()

#         if not row:
#             cursor.close()
#             return jsonify({"error": "User preferences not found."}), 404

#         weights_vect = [
#             float(row["preventionWeight"]),
#             float(row["detectReportWeight"]),
#             float(row["rapidRespWeight"]),
#             float(row["healthSysWeight"]),
#             float(row["intlNormsWeight"]),
#             float(row["riskEnvWeight"])
#         ]

#         cursor.close()

#         # Step 2: Fetch GHS scores for each country
#         cursor = db.get_db().cursor()
#         cursor.execute("""
#             SELECT 
#                 country,
#                 prevention,
#                 detectReport,
#                 rapidResp,
#                 healthSys,
#                 intlNorms,
#                 riskEnv
#             FROM OverallScore
#         """)
#         rows = cursor.fetchall()
#         columns = ["country", "prevention", "detectReport", "rapidResp", "healthSys", "intlNorms", "riskEnv"]
#         df_unscaled = pd.DataFrame(rows, columns=columns)

#         # Step 3: Normalize the scores
#         df_scaled = df_unscaled[["prevention", "detectReport", "rapidResp", "healthSys", "intlNorms", "riskEnv"]].copy()
#         for feat in df_scaled.columns:
#             df_scaled[feat] = (df_scaled[feat] - df_scaled[feat].mean()) / df_scaled[feat].std()

#         # Step 4: Get recommendations
#         chosen_country = df_unscaled["country"].iloc[23]  # optional: override if needed
#         result_df = get_similar(chosen_country, weights_vect, df_unscaled, df_scaled)
#         # Sort by cosine similarity descending
#         sorted_df = result_df.sort_values(by="the_country_cosine", ascending=False)

#         # Return only top N if desired
#         top_n = 5
#         result_json = sorted_df.head(top_n).to_dict(orient="records")
#         return jsonify(result_json), 200


#     except Error as e:
#         return jsonify({"error": str(e)}), 500
    

# @ml.route("/cosine/custom", methods=["POST"])
# def custom_cosine():
#     try:
#         data = request.get_json()
#         origin_country = data.get("origin_country")
#         use_origin_toggle = data.get("use_origin_toggle", False)
#         weights = data.get("weights")

#         if not origin_country or not weights:
#             return jsonify({"error": "Missing data"}), 400

#         weights_vect = [
#             float(weights["preventionWeight"]),
#             float(weights["detectReportWeight"]),
#             float(weights["rapidRespWeight"]),
#             float(weights["healthSysWeight"]),
#             float(weights["intlNormsWeight"]),
#             float(weights["riskEnvWeight"])
#         ]

#         # Fetch scores
#         cursor = db.get_db().cursor()
#         cursor.execute("""
#             SELECT 
#                 country,
#                 prevention,
#                 detectReport,
#                 rapidResp,
#                 healthSys,
#                 intlNorms,
#                 riskEnv
#             FROM OverallScore
#         """)
#         rows = cursor.fetchall()
#         columns = ["country", "prevention", "detectReport", "rapidResp", "healthSys", "intlNorms", "riskEnv"]
#         df_unscaled = pd.DataFrame(rows, columns=columns)

#         df_scaled = df_unscaled[columns[1:]].copy()  # Keep raw, unnormalized


#         df_weightsim = get_similar(origin_country, weights_vect, df_unscaled, df_scaled)
#         df_weightsim.columns = ["country", "dot_weight", "cosine_weight"]

#         if use_origin_toggle:
#             df_originsim = get_similar(origin_country, [1,1,1,1,1,1], df_unscaled, df_scaled)
#             df_originsim.columns = ["country", "dot_origin", "cosine_origin"]

#             merged = pd.merge(df_weightsim, df_originsim, on="country")
#             merged["final_score"] = 0.75 * merged["cosine_weight"] + 0.25 * merged["cosine_origin"]
#             result_df = merged[merged["country"] != origin_country].sort_values(by="final_score", ascending=False)
#         else:
#             df_weightsim["final_score"] = df_weightsim["cosine_weight"]
#             result_df = df_weightsim[df_weightsim["country"] != origin_country].sort_values(by="final_score", ascending=False)

#         return jsonify(result_df.head(5).to_dict(orient="records")), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

