from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app
from backend.ml_models.regression import dataframe
import pandas as pd
import streamlit as st


countries = Blueprint("country_routes", __name__)

# Get list of all countries
# Example: /country/countries 
@countries.route("/countries", methods=["GET"])
def all_countries():
    try:
        current_app.logger.info('Starting all_countries request')
        cursor = db.get_db().cursor()

        # Get query parameters for filtering
        score = request.args.get("score")
            
        current_app.logger.debug(f'Query parameters - score: {score}')

        # Prepare the Base query
        query = "SELECT * FROM Countries WHERE 1=1"
        
        cursor.execute(query)

        
        columns = [col[0] for col in cursor.description]
        countries = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(countries)} Countries')
        return jsonify(countries), 200
    except Error as e:
        current_app.logger.error(f'Database error in all_countries: {str(e)}')
        return jsonify({"error": str(e)}), 500

# Helper for /features/<input> route
def is_value(pair) :
    value_key = 'VALUE'
    key, value = pair
    if key == value_key : 
        return True
    else:
        return False

#get route for six features for a given country
#input is country
@countries.route("/features/<input>", methods=["GET"])
def all_features(input):
    try:
        current_app.logger.info('Starting all_features request')
        cursor = db.get_db().cursor()

        # LiveBirths
        cursor.execute("SELECT * FROM LiveBirths WHERE COUNTRY = %s ORDER BY YEAR DESC", (input,))
        livebirths = cursor.fetchone()
        if not livebirths:
            livebirths = {
                "COUNTRY": input,
                "VALUE": "N/A",
                "YEAR": "N/A",
                "id": "N/A"
                }
            livebirths_cols = [desc[0] for desc in cursor.description]
            df_livebirths = pd.DataFrame([livebirths], columns=livebirths_cols)
        else :
            livebirths_cols = [desc[0] for desc in cursor.description]
            df_livebirths = pd.DataFrame([livebirths], columns=livebirths_cols)
        
        # LifeExpectancy
        cursor.execute("SELECT * FROM LifeExpectancy WHERE COUNTRY = %s ORDER BY YEAR DESC", (input,))
        lifeexpec = cursor.fetchone()
        if not lifeexpec:
            lifeexpec = {
                "COUNTRY": input,
                "VALUE": "N/A",
                "YEAR": "N/A",
                "id": "N/A"
            }
            lifeexpec_cols = [desc[0] for desc in cursor.description]
            df_lifeexpec = pd.DataFrame([lifeexpec], columns=lifeexpec_cols)
        else :
            lifeexpec_cols = [desc[0] for desc in cursor.description]
            df_lifeexpec = pd.DataFrame([lifeexpec], columns=lifeexpec_cols)

        # GenPractitioners
        cursor.execute("SELECT * FROM GenPractitioners WHERE COUNTRY = %s ORDER BY YEAR DESC", (input,))
        genpractitioners = cursor.fetchone()
        if not genpractitioners:
            genpractitioners = {
                "COUNTRY": input,
                "VALUE": "N/A",
                "YEAR": "N/A",
                "id": "N/A"
            }
            genpract_cols = [desc[0] for desc in cursor.description]
            df_genpract = pd.DataFrame([genpractitioners], columns=genpract_cols)
        else:
            genpract_cols = [desc[0] for desc in cursor.description]
            df_genpract = pd.DataFrame([genpractitioners], columns=genpract_cols)

        # Health Expenditure
        cursor.execute("SELECT * FROM HealthExpend WHERE COUNTRY = %s ORDER BY YEAR DESC", (input,))
        healthexpend = cursor.fetchone()
        if not healthexpend:
            healthexpend = {
                "COUNTRY": input,
                "VALUE": "N/A",
                "YEAR": "N/A",
                "id": "N/A"
            }
            healthexpend_cols = [desc[0] for desc in cursor.description]
            df_healthexpend = pd.DataFrame([healthexpend], columns=healthexpend_cols)
        else:
            healthexpend_cols = [desc[0] for desc in cursor.description]
            df_healthexpend = pd.DataFrame([healthexpend], columns=healthexpend_cols)

        # Impoverished Households
        cursor.execute("SELECT * FROM ImpoverishedHouse WHERE COUNTRY = %s ORDER BY YEAR DESC", (input,))
        impoverishedhouse = cursor.fetchone()
        if not impoverishedhouse:
            impoverishedhouse = {
                "COUNTRY": input,
                "VALUE": "N/A",
                "YEAR": "N/A",
                "id": "N/A"
            }
            impoverishedhouse_cols = [desc[0] for desc in cursor.description]
            df_impovhouse = pd.DataFrame([impoverishedhouse], columns=impoverishedhouse_cols)
        else:
            impoverishedhouse_cols = [desc[0] for desc in cursor.description]
            df_impovhouse = pd.DataFrame([impoverishedhouse], columns=impoverishedhouse_cols)

        # Infant Mortality
        cursor.execute("SELECT * FROM InfantMortality WHERE COUNTRY = %s ORDER BY YEAR DESC", (input,))
        infmortality = cursor.fetchone()
        if not infmortality:
            infmortality = {
                "COUNTRY": input,
                "VALUE": "N/A",
                "YEAR": "N/A",
                "id": "N/A"
            }
            infmort_cols = [desc[0] for desc in cursor.description]
            df_infmort = pd.DataFrame([infmortality], columns=infmort_cols)
        else: 
            infmort_cols = [desc[0] for desc in cursor.description]
            df_infmort = pd.DataFrame([infmortality], columns=infmort_cols)

        cursor.close

        # df to dicts
        livebirths_dict = df_livebirths.to_dict(orient="records")[0]
        lifeexpec_dict = df_lifeexpec.to_dict(orient="records")[0]
        genpract_dict = df_genpract.to_dict(orient="records")[0]
        healthexpend_dict = df_healthexpend.to_dict(orient="records")[0]
        impovhouse_dict = df_impovhouse.to_dict(orient="records")[0]
        infmort_dict = df_infmort.to_dict(orient="records")[0]

        # filtered dicts
        filter_livebirths = dict(filter(is_value,  livebirths_dict.items()))
        filter_lifeexpec = dict(filter(is_value, lifeexpec_dict.items()))
        filter_genpract = dict(filter(is_value, genpract_dict.items()))
        filter_healthexpend = dict(filter(is_value, healthexpend_dict.items()))
        filter_impovhouse = dict(filter(is_value, impovhouse_dict.items()))
        filter_infmort = dict(filter(is_value, infmort_dict.items()))


        # Combine data from multiple related queries into one object to return (after jsonify)
        result = {
            "Live Births++": filter_livebirths,
            "Life Expectancy (years)": filter_lifeexpec,
            "General Practitioners*": filter_genpract,
            "Health Expenditure**": filter_healthexpend,
            "Impoverished Households+": filter_impovhouse,
            "Infant Mortality Rate (%)": filter_infmort,
        }

        return jsonify(result), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get detailed information about a specific country including its projects and donors
# Example: /country/countries/ARG
@countries.route("/countries/<country_code>", methods=["GET"])
def country_info(country_code):
    try:
        cursor = db.get_db().cursor()

        # Get country details
        cursor.execute("SELECT * FROM Countries WHERE code = %s", (country_code,))
        country = cursor.fetchone()

        if not country:
            return jsonify({"error": "Country not found"}), 404

        # Get associated info and articles
        cursor.execute("SELECT * FROM CountryInfo WHERE countryCode = %s", (country_code,))
        info = cursor.fetchall()

        cursor.execute("SELECT * FROM CountryArticles WHERE country_code = %s", (country_code,))
        article = cursor.fetchall()

        # Combine data from multiple related queries into one object to return (after jsonify)
        country["info"] = info
        country["articles"] = article

        cursor.close()
        return jsonify(country), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


@countries.route('/countries/<country_code>/articles', methods=['GET'])
def articles_by_country(country_code):
    try:

        cursor = db.get_db().cursor()

        query = """
            SELECT id, article_title, source, article_link
            FROM CountryArticles
            WHERE country_code = %s
        """
        cursor.execute(query, (country_code,))
        articles = cursor.fetchall()

        result = [
            {
                "id": row["id"],
                "title": row["article_title"],
                "source": row["source"],
                "link": row["article_link"]
            }
            for row in articles
        ]

        return jsonify(result)
    except Error as e: 
        return jsonify({"error": str(e)}), 500
    
# Posts article in favorites table
@countries.route('/articles/favorite', methods=['POST'])
def favorite_articles():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["articleID"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        # Insert new article 
        query = """
        INSERT INTO Favorites (articleID)
        VALUES (%s)
        """
        cursor.execute(
            query,
            (
                data["articleID"]
            ),
        )

        db.get_db().commit()
        fav_article_id = cursor.lastrowid
        cursor.close()

        return (
            jsonify({"message": "Article favorited successfully", "article_id": fav_article_id}),
            201,
        )
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# gets all favorite articles and information about them
@countries.route('/articles/favorite', methods=['GET'])
def fav_articles():
    try:
        cursor = db.get_db().cursor()

        userID = st.session_state['id']

        # Get country details
        cursor.execute("SELECT * FROM Favorites WHERE userID = %s", (userID,))

        articles = cursor.fetchall()

        if not articles:
            return jsonify({"error": "Articles not found"}), 404

        # Get associated article info
        for items in articles :
            cursor.execute("SELECT * FROM CountryArticles WHERE articleID = %s", (articles['id'],))
            info = cursor.fetchall()
            articles["info"] = info


        cursor.close()
        return jsonify(articles), 200
    except Error as e:
        return jsonify({"error": str(e)}), 5

# unfavorite an article, deleting it from Favorites table
@countries.route('/articles/favorite/<articleID>', methods=['DELETE'])
def unfavorite_article(articleID):
    try:
        current_app.logger.info("Attempting to Unfavorite an Article %s", articleID)

        cursor = db.get_db().cursor()
        
        userID = st.session_state['id']

        # First, check if the article exists
        cursor.execute("SELECT articleID FROM Favorites WHERE articleID = %s AND userID = %s", (articleID,userID,))
        if not cursor.fetchone():
            current_app.logger.warning("Article ID %s not found", articleID)
            cursor.close()
            return jsonify({"error": "Article not found"}), 404

        # Delete the country
        cursor.execute("DELETE FROM Favorites WHERE articleID = %s AND userID = %s", (articleID,userID,))
        db.get_db().commit()
        cursor.close()

        current_app.logger.info("Successfully deleted articleID %s", articleID)
        return jsonify({"message": f"Article {articleID} deleted successfully"}), 200

    except Error as e:
        current_app.logger.error("Database error in unfavorite_article: %s", str(e))
        return jsonify({"error": str(e)}), 500

# Get list of all recommendation factors with descriptions
# Example: /country/factor_descriptions
@countries.route("/factor_descriptions", methods=["GET"])
def factor_descriptions():
    try:
        factors = [
            {
                "name": "Prevention",
                "description": "Measures to prevent the emergence and spread of infectious diseases"
            },
            {
                "name": "Detection and Reporting",
                "description": "Capacity for early detection, testing, and transparent reporting of health threats"
            },
            {
                "name": "Rapid Response",
                "description": "Readiness and speed of response to outbreaks and emergencies"
            },
            {
                "name": "Health System",
                "description": "Availability, accessibility, and strength of healthcare infrastructure and services"
            },
            {
                "name": "Compliance with International Norms",
                "description": "Degree of compliance with WHO and other global health regulations"
            },
            {
                "name": "Risk Environment",
                "description": "The country's social, political, and environmental vulnerability to health threats"
            }
        ]
        return jsonify(factors), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500