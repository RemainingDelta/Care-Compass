from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for User routes
users = Blueprint("users", __name__)


# Get all users with optional filtering by userRole
# Example: /users/users
@users.route("/users", methods=["GET"])
def all_users():
    try: 
        current_app.logger.info('Starting all_users request')
        cursor = db.get_db().cursor()

        # Get query parameters for filtering
        roleID = request.args.get("roleID")

        current_app.logger.debug(f'Query parameters - User Role: {roleID}')

        # Prepare the Base query
        query = "SELECT * FROM Users WHERE 1=1"
        params = []

        # Add filters if provided
        if roleID:
            query += " AND roleID = %s"
            params.append(roleID)
        

        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        users = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(users)} Users')
        return jsonify(users), 200
    except Error as e:
        current_app.logger.error(f'Database error in all_users: {str(e)}')
        return jsonify({"error": str(e)}), 500


# get user id from last name
@users.route("/users/id/<input>", methods=["GET"])
def user_id(input):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT id FROM Users WHERE email = %s", (input,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404
        
        cursor.close()
        return jsonify(user), 200
        
    except Error as e:
        return jsonify({"error": "User not found"}), 404
    

@users.route("/users/<int:user_id>/preferences", methods=["PUT"])
def update_user_preferences(user_id):
    try:
        current_app.logger.info(f"Updating preferences for user ID {user_id}")
        cursor = db.get_db().cursor()

        data = request.get_json()
        prevention = data.get("preventionWeight")
        detect = data.get("detectReportWeight")
        rapid = data.get("rapidRespWeight")
        health = data.get("healthSysWeight")
        intl = data.get("intlNormsWeight", 1.0)
        risk = data.get("riskEnvWeight", 1.0)

        if not all(isinstance(val, (int, float)) for val in [prevention, detect, rapid, health, intl, risk]):
            return jsonify({"error": "All weights must be numbers."}), 400

        cursor.execute("SELECT id FROM UserWeights WHERE userID = %s", (user_id,))
        existing = cursor.fetchone()

        if existing:
            update_query = """
                UPDATE UserWeights
                SET preventionWeight = %s,
                    detectReportWeight = %s,
                    rapidRespWeight = %s,
                    healthSysWeight = %s,
                    intlNormsWeight = %s,
                    riskEnvWeight = %s
                WHERE userID = %s
            """
            cursor.execute(update_query, (prevention, detect, rapid, health, intl, risk, user_id))
        else:
            insert_query = """
                INSERT INTO UserWeights (userID, preventionWeight, detectReportWeight, rapidRespWeight, healthSysWeight, intlNormsWeight, riskEnvWeight)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (user_id, prevention, detect, rapid, health, intl, risk))

        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "Preferences saved successfully."}), 200

    except Error as e:
        current_app.logger.error(f"Database error in update_user_preferences: {str(e)}")
        return jsonify({"error": str(e)}), 500

    
@users.route("/users/<int:user_id>/preferences", methods=["GET"])
def get_user_preferences(user_id):
    try:
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
            return jsonify({"message": "No preferences set yet."}), 404


        weights = {
            "preventionWeight": row["preventionWeight"],
            "detectReportWeight": row["detectReportWeight"],
            "rapidRespWeight": row["rapidRespWeight"],
            "healthSysWeight": row["healthSysWeight"],
            "intlNormsWeight": row["intlNormsWeight"],
            "riskEnvWeight": row["riskEnvWeight"]
        }

        return jsonify(weights), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
