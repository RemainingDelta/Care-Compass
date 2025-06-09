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
    
# model calls post to put weights in database
# adds new regression weight from model to database
@ml.route("/ml/get_cosine_similar/<chosen_country>/<weights_dict>", methods=["GET"])
def get_cosine_similar(chosen_country, weights_dict):
    weights_vect = []
    #weights_dict_dump = json.dumps(weights_dict) 
    weights_dict2 = json.loads(weights_dict)
    print("THIS IS WEIGHTS DICT 2")
    print(weights_dict2)
    for key in weights_dict2:
        print("ITERATION 1")
        if key == "Prevention":
            print("This is prevention")
            print(weights_dict2[key])
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
    df = get_similar(chosen_country, weights_vect)
    print("Country received:", chosen_country)

    result = df.to_dict()
    return jsonify(result)


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
@ml.route("/ml/get_autoregressive/<input>", methods=["GET"])
def get_autoregressive(input):
    inputs = [str(x.strip()) for x in input.split(',')]
    result = autoreg_predict(dataframe(inputs[1]), inputs[0])
    print("Country received:", inputs[0])

    return jsonify(result)

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
