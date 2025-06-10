from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app
from backend.ml_models.regression import dataframe
import pandas as pd

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
        query = "SELECT * FROM Countries WHERE 1=1"
        
        cursor.execute(query)

        
        columns = [col[0] for col in cursor.description]
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
        current_app.logger.info(f'Successfully retrieved profile for country ID: {country_id}')
        return jsonify(country), 200
    
    except Error as e:
            current_app.logger.error(f'Database error in get_country_profile: {str(e)}')
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
    try:
        data = request.get_json()

        # Extract fields from JSON
        name = data.get("name")
        region = data.get("region")
        strengths = data.get("strengths")
        weaknesses = data.get("weaknesses")
        score = data.get("score")
        info = data.get("info")

        current_app.logger.info("Updating country ID %s with new metadata", country_id)

        # Validate at least one field is provided
        if not any([name, region, strengths, weaknesses, score, info]):
            return jsonify({"error": "No fields provided for update"}), 400

        fields = []
        values = []

        if name:
            fields.append("name = %s")
            values.append(name)
        if region:
            fields.append("region = %s")
            values.append(region)
        if strengths:
            fields.append("strengths = %s")
            values.append(strengths)
        if weaknesses:
            fields.append("weaknesses = %s")
            values.append(weaknesses)
        if score is not None:
            fields.append("score = %s")
            values.append(score)
        if info:
            fields.append("info = %s")
            values.append(info)

        values.append(country_id)  # for WHERE clause

        query = f"UPDATE country SET {', '.join(fields)} WHERE id = %s"

        cursor = db.get_db().cursor()
        cursor.execute(query, values)
        db.get_db().commit()
        cursor.close()

        current_app.logger.info("Successfully updated country ID %s", country_id)
        return jsonify({"message": "Country updated successfully"}), 200

    except Error as e:
        current_app.logger.error("Database error in update_country: %s", str(e))
        return jsonify({"error": str(e)}), 500


# Delete a country record (Admin only)
# Example: /countries/<country_id>
@countries.route("/countries/<int:country_id>", methods=["DELETE"])
def delete_country(country_id):
    try:
        current_app.logger.info("Attempting to delete country ID %s", country_id)

        cursor = db.get_db().cursor()

        # First, check if the country exists
        cursor.execute("SELECT id FROM country WHERE id = %s", (country_id,))
        if not cursor.fetchone():
            current_app.logger.warning("Country ID %s not found", country_id)
            cursor.close()
            return jsonify({"error": "Country not found"}), 404

        # Delete the country
        cursor.execute("DELETE FROM country WHERE id = %s", (country_id,))
        db.get_db().commit()
        cursor.close()

        current_app.logger.info("Successfully deleted country ID %s", country_id)
        return jsonify({"message": f"Country {country_id} deleted successfully"}), 200

    except Error as e:
        current_app.logger.error("Database error in delete_country: %s", str(e))
        return jsonify({"error": str(e)}), 500

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

# Reads in Practitioners dataset
# Example: /countries/practitioners
@countries.route("/countries/practitioners", methods=["GET"])
def get_practitioners():
    if_exists = "replace"
    headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    url = f'https://dw.euro.who.int/api/v3/measures/HLTHRES_67?output=data'
    url_text = requests.get(url, headers=headers).text

    result = json.loads(url_text)

    data = result['data']

    #print(data)
    df_practitioners = pd.DataFrame()
    final_dict = dict()

    for item in data:
    
        final_dict['country'] = item['dimensions']['COUNTRY']
        #final_dict['country_grp'] = item['dimensions']['COUNTRY_GRP']
        final_dict['year'] = item['dimensions']['YEAR']
        final_dict['practitioners'] = item['value']['numeric']
        series = pd.Series(final_dict)
        df_practitioners = pd.concat([df_practitioners, series.to_frame().T], ignore_index = True)

    #current_app.logger.info(f'Successfully retrieved {len(countries)} Countries')
    conn = sqlite3.connect(r"..\\..\database-files\\cc_db.sql")
    df_practitioners.to_sql('practitioner_table', conn, if_exists="replace", index=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM practitioner_table")
    countries = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(countries), 200

#model calls post to put weights in database
# adds new regression weight from model to database
@countries.route("/countries/data/<input>", methods=["GET"])
def get_data(input):
    result = dataframe(input)
    table = result.to_dict()
    return jsonify(table)

#post route for six features 

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
def get_all_features(input):
    try:
        current_app.logger.info('Starting get_all_features request')
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
            "Live Births per 1000 Population": filter_livebirths,
            "Life Expectancy (years)": filter_lifeexpec,
            "General Practitioners per 10,000 Population": filter_genpract,
            "Total Health Expenditure per Capita": filter_healthexpend,
            "Impoverished Households due to out-of-pocket healthcare payments": filter_impovhouse,
            "Infant Mortality Rate (%)": filter_infmort,
        }

        return jsonify(result), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500

