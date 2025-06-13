from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app
from flask import make_response
import numpy as np
from backend.ml_models.cosine_similarity import get_similar
from backend.ml_models.regression import dataframe
from backend.ml_models.regression import predict
from backend.ml_models.regression import autoreg_predict
from backend.ml_models.regression import create_xy
from backend.ml_models.regression import create_xy_full
from backend.ml_models.regression import create_xy_select
from backend.ml_models.regression import autoreg_train
from backend.ml_models.regression import autoreg_predict_full
from backend.ml_models.regression import add_predict
import pandas as pd
import json



ml = Blueprint("ml", __name__)


"""
Query Params:
- feature: Name of the healthcare factor (e.g. 'Health System')
- countries: Comma-separated country IDs (e.g. 1,2,3)

Returns:
- Regression-based predictions for each country
- Format: { country_id: [ { year, value }, ... ] }
"""
# Generate regression prediction for a feature across countries
# Example: /ml/predict?feature=Health System&countries=1,2,3
@ml.route("/ml/predict/<expenditure>/<country>", methods=["GET"])
def predict_feature_over_time(expenditure,country):
    # get a database cursor 
    cursor = db.get_db().cursor()
    
    current_app.logger.info(f'expenditure = {expenditure}')
    current_app.logger.info(f'country = {country}')

    # get the model params from the database
    query = 'SELECT year, expenditure, country FROM regression_model_params WHERE country = %s'
    cursor.execute(query, (country),)
    rows = cursor.fetchall()

    #used chat -- said to build list of column names
    col_names = [desc[0] for desc in cursor.description]

    df_expenditure = pd.DataFrame(rows, columns=col_names)
    
    result = predict(df_expenditure, country)

    return_dict = {
        "slope": result["slope"],
        "intercept": result["intercept"],
        "mse": result['"mse"'],
        "r2": result["r2"]
    }

    the_response = make_response(jsonify(return_dict))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
    

# model calls post to put weights in database
# adds new regression weight from model to database
@ml.route("/ml/store-weights", methods=["POST"])
def store_weights():
    try:
        data = request.get_json()
        result = predict(dataframe(), chosen_country)

        # Validate required fields
        required_fields = ["country", "feature", "slope", "intercept", "mse", "r2"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        cursor = db.get_db().cursor()

        # Insert new Weight
        query = """
        INSERT INTO regression_weights (country, feature, slope, intercept, mse, r2)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["country"],
                data["feature"],
                data["slope"],
                data["intercept"],
                data.get["mse", None],
                data.get("r2", None)
            )
        )

        db.get_db().commit()
        new_weight_id = cursor.lastrowid
        cursor.close()

        return (
            jsonify({"message": "Weight created successfully", "weight_id": new_weight_id}),
            201,
        )
    except Error as e:
        return jsonify({"error": str(e)}), 500


#model calls post to put weights in database
# adds new regression weight from model to database
@ml.route("/ml/get_regression/<input>", methods=["GET"])
def get_regression(input):
    inputs = [str(x.strip()) for x in input.split(',')]
    result = predict(dataframe(inputs[1]), inputs[0])
    print("Country received:", inputs[0])

    return jsonify(result)

#model calls post to put weights in database
# adds new regression weight from model to database
@ml.route("/ml/get_autoregressive/<chosen_country>/<data_code>/<chosen_year>", methods=["GET"])
def get_autoregressive(chosen_country, data_code, chosen_year):

    cursor = db.get_db().cursor()
    #print("the chosen year")
    #print(chosen_year)
    if data_code == 'HFA_16':
        query = """SELECT * FROM LiveBirths"""
    elif data_code == 'HFA_570':
        query = """SELECT * FROM HealthExpend"""
    elif data_code == 'HLTHRES_67':
        query = "SELECT * FROM GenPractitioners"
    #print(query)
    cursor.execute(query)
    rows = cursor.fetchall()
    #print(rows)

    # Convert to DataFrame
    columns = ["COUNTRY", "YEAR", "VALUE"]
    df = pd.DataFrame(rows, columns=columns)
    value_list = []
    for value in df["VALUE"]:
        value_list.append(float(value))
    
    df["VALUE"] = value_list
    #print("the chosen country")
    #print(chosen_country)
    #print("df")
    #print(df)
    
    inputs = [chosen_country, data_code, chosen_year]
    #xy = create_xy_full(dataframe(inputs[1]))
    #df = dataframe(inputs[1])
    #df_country = df[(df['COUNTRY'] == inputs[0])]
    df_country = df[df['COUNTRY'] == inputs[0]]
    #print("df_country")
    #print(df_country)
    #print("df_country")
    #print(df_country)
    df_filtered = df_country.reset_index(drop=True)
    print("filtered dataframe")
    print(df_filtered)
    #print("df_filtered")
    #print(df_filtered)
    year = int(df_filtered.iloc[len(df_filtered) - 1]['YEAR'])
    years = int(inputs[2]) - year
    #print("number of years")
    #print(years)
    input = create_xy_select(df, inputs[0])
    train = create_xy_full(df)
    preds = autoreg_predict_full(input[0], input[1], autoreg_train(train[0], train[1]), years, train[2])
    result = add_predict(df_country, preds, input[0])
    print("Country received:", inputs[0])
    result_final = result.to_json()
    #result_final = result.to_dict()
    #result_final = json.dumps(result_final)
    print("final data frame")
    print(result_final)
    return jsonify(result_final)

#model calls post to put weights in database
# adds new regression weight from model to database
@ml.route("/ml/get_autoregressive_all/<input>", methods=["GET"])
def get_autoregressive_all(input):
    inputs = [str(x.strip()) for x in input.split(',')]
    xy = create_xy_full(dataframe(inputs[1]))
    inputs = create_xy(dataframe(inputs[1]), inputs[0])
    result = autoreg_predict_full(inputs[0], inputs[1], autoreg_train(xy[0], xy[1]), inputs[2])
    print("Country received:", inputs[0])

    return jsonify(result)

#model calls post to put weights in database
# adds new regression weight from model to database
@ml.route("/ml/store_autoregressive/<chosen_country>/<data_code>/<chosen_year>", methods=["PUT"])
def store_autoregressive(chosen_country, data_code, chosen_year):

    cursor = db.get_db().cursor()
    #print("the chosen year")
    #print(chosen_year)
    if data_code == 'HFA_16':
        query = """SELECT * FROM LiveBirths"""
    elif data_code == 'HFA_570':
        query = """SELECT * FROM HealthExpend"""
    elif data_code == 'HLTHRES_67':
        query = "SELECT * FROM GenPractitioners"
    #print(query)
    cursor.execute(query)
    rows = cursor.fetchall()
    #print(rows)

    # Convert to DataFrame
    columns = ["COUNTRY", "YEAR", "VALUE"]
    df = pd.DataFrame(rows, columns=columns)
    value_list = []
    for value in df["VALUE"]:
        value_list.append(float(value))
    
    df["VALUE"] = value_list
    #print("the chosen country")
    #print(chosen_country)
    #print("df")
    #print(df)
    
    inputs = [chosen_country, data_code, chosen_year]
    #xy = create_xy_full(dataframe(inputs[1]))
    #df = dataframe(inputs[1])
    #df_country = df[(df['COUNTRY'] == inputs[0])]
    df_country = df[df['COUNTRY'] == inputs[0]]
    #print("df_country")
    #print(df_country)
    #print("df_country")
    #print(df_country)
    df_filtered = df_country.reset_index(drop=True)
    print("filtered dataframe")
    print(df_filtered)
    #print("df_filtered")
    #print(df_filtered)
    year = int(df_filtered.iloc[len(df_filtered) - 1]['YEAR'])
    years = int(inputs[2]) - year
    #print("number of years")
    #print(years)
    input = create_xy_select(df, inputs[0])
    train = create_xy_full(df)
    result = autoreg_train(train[0], train[1])
    print("Country received:", inputs[0])
    result_final = result.to_json()
    #result_final = result.to_dict()
    #result_final = json.dumps(result_final)
    print(result_final)
    return jsonify(result_final)

#model calls post to put weights in database
# adds new regression weight from model to database
@ml.route("/ml/get_graph_data/<input>", methods=["GET"])
def get_graph_data(input):
    result = dataframe(input)
    table = result.to_dict()
    return jsonify(table)

#gets all the countries in the live births dataset
@ml.route("/ml/get_countries", methods=["GET"])
def get_countries():
    # get a database cursor 
    cursor = db.get_db().cursor()
    
    #cursor.execute('''
    #CREATE TABLE IF NOT EXISTS births_table(
       #COUNTRY     VARCHAR(3) NOT NULL PRIMARY KEY
      #,COUNTRY_GRP VARCHAR(17)
      #,SEX         VARCHAR(3) NOT NULL
      #,YEAR        INTEGER  NOT NULL
      #,VALUE       NUMERIC(5,2) NOT NULL
    #)
    #''')
    
    
    # Query distinct countries
    cursor.execute("SELECT DISTINCT COUNTRY FROM births_table WHERE COUNTRY IS NOT NULL ORDER BY COUNTRY")
    countries = [row[0] for row in cursor.fetchall()]
    return countries


#Gets the cosine similarity numbers for the chosen country 
@ml.route("/ml/cosine/<chosen_country>/<weights_dict>", methods=["GET"])
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


@ml.route("/cosine/<int:user_id>", methods=["GET"])
def cosine_for_user(user_id):
    try:
        # Step 1: Fetch user weights from the DB
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT 
                preventionWeight,
                detectReportWeight,
                rapidRespWeight,
                healthSysWeight,
                intlNormsWeight,
                riskEnvWeight
            FROM UserWeights WHERE userID = %s
        """, (user_id,))
        row = cursor.fetchone()

        if not row:
            cursor.close()
            return jsonify({"error": "User preferences not found."}), 404

        weights_vect = [
            float(row["preventionWeight"]),
            float(row["detectReportWeight"]),
            float(row["rapidRespWeight"]),
            float(row["healthSysWeight"]),
            float(row["intlNormsWeight"]),
            float(row["riskEnvWeight"])
        ]

        cursor.close()

        # Step 2: Fetch GHS scores for each country
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT 
                country,
                prevention,
                detectReport,
                rapidResp,
                healthSys,
                intlNorms,
                riskEnv
            FROM OverallScore
        """)
        rows = cursor.fetchall()
        columns = ["country", "prevention", "detectReport", "rapidResp", "healthSys", "intlNorms", "riskEnv"]
        df_unscaled = pd.DataFrame(rows, columns=columns)

        # Step 3: Normalize the scores
        df_scaled = df_unscaled[["prevention", "detectReport", "rapidResp", "healthSys", "intlNorms", "riskEnv"]].copy()
        for feat in df_scaled.columns:
            df_scaled[feat] = (df_scaled[feat] - df_scaled[feat].mean()) / df_scaled[feat].std()

        # Step 4: Get recommendations
        chosen_country = df_unscaled["country"].iloc[0]  # optional: override if needed
        result_df = get_similar(chosen_country, weights_vect, df_unscaled, df_scaled)
        return jsonify(result_df.to_dict()), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
