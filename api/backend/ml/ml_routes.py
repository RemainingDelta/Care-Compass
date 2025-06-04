from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app


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
@ml.route("/ml/predict", methods=["GET"])
def predict_feature_over_time():
    feature = request.args.get("feature")
    countries = request.args.get("countries")
    return jsonify({"message": "Predicted values coming soon"})



