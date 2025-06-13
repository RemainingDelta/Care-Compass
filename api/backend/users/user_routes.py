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
    

# Update a user's healthcare factor preferences
@users.route("/users/<int:user_id>/preferences", methods=["PUT"])
def update_user_preferences(user_id):
    try:
        current_app.logger.info(f"Updating preferences for user ID {user_id}")
        cursor = db.get_db().cursor()

        data = request.get_json()
        quality = data.get("qualityWeight")
        accessibility = data.get("accessibilityWeight")
        affordability = data.get("affordabilityWeight")
        outcome = data.get("outcomeWeight")

        # Basic validation
        if not all(isinstance(val, (int, float)) for val in [quality, accessibility, affordability, outcome]):
            return jsonify({"error": "All weights must be numbers."}), 400

        update_query = """
            UPDATE Users
            SET qualityWeight = %s,
                accessibilityWeight = %s,
                affordabilityWeight = %s,
                outcomeWeight = %s
            WHERE id = %s
        """
        cursor.execute(update_query, (quality, accessibility, affordability, outcome, user_id))
        db.get_db().commit()

        if cursor.rowcount == 0:
            current_app.logger.warning(f"No user found with ID {user_id}")
            return jsonify({"error": "User not found."}), 404

        current_app.logger.info(f"Successfully updated preferences for user ID {user_id}")
        return jsonify({"message": "Preferences updated successfully."}), 200

    except Error as e:
        current_app.logger.error(f"Database error in update_user_preferences: {str(e)}")
        return jsonify({"error": str(e)}), 500

