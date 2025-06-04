from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app


comparison = Blueprint("comparison", __name__)

"""
Query Params:
- countries: comma-separated list of country IDs (e.g., 1,2,3)

Returns:
- A table of all available factors and their scores for each country
"""
# Compare selected countries by all factors (for the table view)
# Example: /compare?countries=1,2,3
@comparison.route("/compare", methods=["GET"])
def compare_countries():
    pass


"""
Query Params:
- feature: the name of the healthcare factor (e.g., 'Health System')
- countries: comma-separated country IDs (e.g., 1,2,3)

Returns:
- Historical data over time for each country (no prediction)
"""
# Time series of a specific feature across selected countries
# Example: /compare/timeseries?feature=Health System&countries=1,2,3
@comparison.route("/compare/timeseries", methods=["GET"])
def compare_feature_over_time():
    pass
