from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app


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
    pass


# Get factor scores for a country
# Example: /countries/{country_id}/factors
@countries.route("/countries/<int:country_id>/factors", methods=["GET"])
def get_country_factors(country_id):
    pass


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
