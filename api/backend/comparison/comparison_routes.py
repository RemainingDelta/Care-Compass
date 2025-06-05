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
    country_ids = request.args.get("countries")
    if not country_ids:
        return jsonify({"error": "Missing required query parameter: countries"}), 400

    country_ids = [int(cid) for cid in country_ids.split(",")]

    cursor = db.get_db().cursor()

    query = """
    SELECT c.id AS country_id, c.name AS country_name, f.name AS factor_name, f.score
    FROM country c JOIN factors f ON f.countryID = c.id
    WHERE c.id IN (%s)
    ORDER BY c.id, f.name
    """ % (",".join(["%s"] * len(country_ids)))

    cursor.execute(query, tuple(country_ids))
    results = cursor.fetchall()

    return jsonify(results)



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
    feature = request.args.get("feature")
    countries = request.args.get("countries")
    if not feature or not countries:
        return jsonify({"error": "Missing required query parameters: feature and countries"}), 400

    country_ids = [int(cid) for cid in countries.split(",")]

    cursor = db.get_db().cursor()

    query = """
    SELECT c.name AS country_name, f.name AS factor_name, f.score, c.time
    FROM country c JOIN factors f ON f.countryID = c.id
    WHERE f.name = %s AND c.id IN (%s)
    ORDER BY c.name, c.time
    """ % ("%s", ",".join(["%s"] * len(country_ids)))

    cursor.execute(query, (feature, *country_ids))
    results = cursor.fetchall()

    return jsonify(results)

