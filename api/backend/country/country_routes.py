from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app
import pandas as pd 
import sqlite3


countries = Blueprint("country_routes", __name__)

# Get list of all countries
# Example: /country/countries 
@countries.route("/countries", methods=["GET"])
def get_all_countries():
    try:
        current_app.logger.info('Starting get_all_countries request')
        cursor = db.get_db().cursor()

        # Get query parameters for filtering
        score = request.args.get("score")
            
        current_app.logger.debug(f'Query parameters - score: {score}')

        # Prepare the Base query
        query = "SELECT * FROM Country WHERE 1=1"
        params = []

        # Add filters if provided
        if score:
            query += " AND SCORE = %s"
            params.append(score)
           
        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        countries = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(countries)} Countries')
        return jsonify(countries), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_countries: {str(e)}')
        return jsonify({"error": str(e)}), 500



# Get detailed country profile
# Example: /countries/{country_id}/profile
@countries.route("/countries/<int:country_id>/profile", methods=["GET"])
def get_country_profile(country_id):
    try:
        current_app.logger.info("Retrieving profile for country ID: %s", country_id)
        cursor = db.get_db().cursor()
        
        # subject to change
        cursor.execute("""
            SELECT id, name, region, strengths, weaknesses, score, info, time     
            FROM country
            WHERE id = %s
        """, (country_id,))
        country = cursor.fetchone()

        if not country:
            current_app.logger.warning("Country ID %s not found", country_id)
            return jsonify({"error": "Country not found"}), 404
        
        # Fetch all factor scores associated with the country
        cursor.execute("""
            SELECT name AS factor_name, score, weight
            FROM factors
            WHERE countryID = %s
        """, (country_id,))
        factors = cursor.fetchall()

        # Attach factors to profile
        country["factors"] = factors

        cursor.close()
        current_app.logger.info("Successfully retrieved profile for country ID: ", {country_id})
        return jsonify(country), 200
    
    except Error as e:
            current_app.logger.error("Database error in get_country_profile: ", {str(e)})
            return jsonify({"error": str(e)}), 500


# Get factor scores for a country
# Example: /countries/{country_id}/factors
@countries.route("/countries/<int:country_id>/factors", methods=["GET"])
def get_country_factors(country_id):
    try:
        current_app.logger.info("Retrieving factor scores for country ID: %s", country_id)
        cursor = db.get_db().cursor()
        
        # subject to change
        cursor.execute("""
            SELECT SELECT factorID, name AS factor_name, score, weight    
            FROM factors
            WHERE id = %s
        """, (country_id,))
        factors = cursor.fetchone()

        cursor.close()

        if not factors:
            current_app.logger.warning("Factor scores for this Country ID %s not found", country_id)
            return jsonify({"error": "Factor score for this country not found"}), 404

        current_app.logger.info("Successfully fetched %d factors for country ID %s", {country_id})
        return jsonify(factors), 200
    
    except Error as e:
            current_app.logger.error("Database error in get_country_profile: ", {str(e)})
            return jsonify({"error": str(e)}), 500


# Get top/bottom factors compared to other countries
# Example: /countries/{country_id}/strengths-weaknesses
@countries.route("/countries/<int:country_id>/strengths-weaknesses", methods=["GET"])
def get_strengths_weaknesses(country_id):
    pass


# Return list of countries with similar scores
# Example: /countries/{country_id}/similar
@countries.route("/countries/<int:country_id>/similar", methods=["GET"])
def get_similar_countries(country_id):
    pass


'''
'''
# Update a country’s metadata (Admin only)
# Example: /countries/<country_id>
@countries.route("/countries/<int:country_id>", methods=["PUT"])
def update_country(country_id):
    pass


# Delete a country record (Admin only)
# Example: /countries/<country_id>
@countries.route("/countries/<int:country_id>", methods=["DELETE"])
def delete_country(country_id):
    pass

# Reads in GHS Index data
# Example: /countries/ghs_index
@countries.route("/countries/ghs_index", methods=["GET"])
def get_ghs_index():
    if_exists = "replace"
    df = pd.read_csv('https://www.ghsindex.org/wp-content/uploads/2022/04/2021-GHS-Index-April-2022.csv')
    #current_app.logger.info(f'Successfully retrieved {len(countries)} Countries')
    conn = sqlite3.connect(r"..\\..\database-files\\cc_db.sql")
    df.to_sql('ghs_table', conn, if_exists="replace", index=False)
    cursor = conn.cursor()
    cursor.execute("SELECT 'Afghanistan' FROM ghs_table")
    countries = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(countries), 200


    