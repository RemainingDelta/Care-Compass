from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for NGO routes
ngos = Blueprint("ngos", __name__)


# Get all NGOs with optional filtering by country, focus area, and founding year
# Example: /ngo/ngos?country=United%20States&focus_area=Environmental%20Conservation
@ngos.route("/ngos", methods=["GET"])
def get_all_ngos():
    try: 
        current_app.logger.info('Starting get_all_ngos request')
        cursor = db.get_db().cursor()

        # Note: Query parameters are added after the main part of the URL.
        # Here is an example:
        # http://localhost:4000/ngo/ngos?founding_year=1971
        # founding_year is the query param.

        # Get query parameters for filtering
        country = request.args.get("country")
        focus_area = request.args.get("focus_area")
        founding_year = request.args.get("founding_year")

        current_app.logger.debug(f'Query parameters - country: {country}, focus_area: {focus_area}, founding_year: {founding_year}')

        # Prepare the Base query
        query = "SELECT * FROM WorldNGOs WHERE 1=1"
        params = []

        # Add filters if provided
        if country:
            query += " AND Country = %s"
            params.append(country)
        if focus_area:
            query += " AND Focus_Area = %s"
            params.append(focus_area)
        if founding_year:
            query += " AND Founding_Year = %s"
            params.append(founding_year)

        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        ngos = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(ngos)} NGOs')
        return jsonify(ngos), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_ngos: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Get detailed information about a specific NGO including its projects and donors
# Example: /ngo/ngos/1
@ngos.route("/ngos/<int:ngo_id>", methods=["GET"])
def get_ngo(ngo_id):
    try:
        cursor = db.get_db().cursor()

        # Get NGO details
        cursor.execute("SELECT * FROM WorldNGOs WHERE NGO_ID = %s", (ngo_id,))
        ngo = cursor.fetchone()

        if not ngo:
            return jsonify({"error": "NGO not found"}), 404

        # Get associated projects then donors
        cursor.execute("SELECT * FROM Projects WHERE NGO_ID = %s", (ngo_id,))
        projects = cursor.fetchall()

        cursor.execute("SELECT * FROM Donors WHERE NGO_ID = %s", (ngo_id,))
        donors = cursor.fetchall()

        # Combine data from multiple related queries into one object to return (after jsonify)
        ngo["projects"] = projects
        ngo["donors"] = donors

        cursor.close()
        return jsonify(ngo), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Create a new NGO
# Required fields: Name, Country, Founding_Year, Focus_Area, Website
# Example: POST /ngo/ngos with JSON body
@ngos.route("/ngos", methods=["POST"])
def create_ngo():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["Name", "Country", "Founding_Year", "Focus_Area", "Website"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        # Insert new NGO
        query = """
        INSERT INTO WorldNGOs (Name, Country, Founding_Year, Focus_Area, Website)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["Name"],
                data["Country"],
                data["Founding_Year"],
                data["Focus_Area"],
                data["Website"],
            ),
        )

        db.get_db().commit()
        new_ngo_id = cursor.lastrowid
        cursor.close()

        return (
            jsonify({"message": "NGO created successfully", "ngo_id": new_ngo_id}),
            201,
        )
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Update an existing NGO's information
# Can update any field except NGO_ID
# Example: PUT /ngo/ngos/1 with JSON body containing fields to update
@ngos.route("/ngos/<int:ngo_id>", methods=["PUT"])
def update_ngo(ngo_id):
    try:
        data = request.get_json()

        # Check if NGO exists
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM WorldNGOs WHERE NGO_ID = %s", (ngo_id,))
        if not cursor.fetchone():
            return jsonify({"error": "NGO not found"}), 404

        # Build update query dynamically based on provided fields
        update_fields = []
        params = []
        allowed_fields = ["Name", "Country", "Founding_Year", "Focus_Area", "Website"]

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(ngo_id)
        query = f"UPDATE WorldNGOs SET {', '.join(update_fields)} WHERE NGO_ID = %s"

        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "NGO updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get all projects associated with a specific NGO
# Example: /ngo/ngos/1/projects
@ngos.route("/ngos/<int:ngo_id>/projects", methods=["GET"])
def get_ngo_projects(ngo_id):
    try:
        cursor = db.get_db().cursor()

        # Check if NGO exists
        cursor.execute("SELECT * FROM WorldNGOs WHERE NGO_ID = %s", (ngo_id,))
        if not cursor.fetchone():
            return jsonify({"error": "NGO not found"}), 404

        # Get all projects for the NGO
        cursor.execute("SELECT * FROM Projects WHERE NGO_ID = %s", (ngo_id,))
        projects = cursor.fetchall()
        cursor.close()

        return jsonify(projects), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get all donors associated with a specific NGO
# Example: /ngo/ngos/1/donors
@ngos.route("/ngos/<int:ngo_id>/donors", methods=["GET"])
def get_ngo_donors(ngo_id):
    try:
        cursor = db.get_db().cursor()

        # Check if NGO exists
        cursor.execute("SELECT * FROM WorldNGOs WHERE NGO_ID = %s", (ngo_id,))
        if not cursor.fetchone():
            return jsonify({"error": "NGO not found"}), 404

        # Get all donors for the NGO
        cursor.execute("SELECT * FROM Donors WHERE NGO_ID = %s", (ngo_id,))
        donors = cursor.fetchall()
        cursor.close()

        return jsonify(donors), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
