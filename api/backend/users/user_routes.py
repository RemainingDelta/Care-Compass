from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for User routes
users = Blueprint("users", __name__)


# Get all users with optional filtering by userRole
# Example: /users/users
@users.route("/users", methods=["GET"])
def get_all_users():
    try: 
        current_app.logger.info('Starting get_all_users request')
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
        current_app.logger.error(f'Database error in get_all_users: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Get detailed information about a specific User 
# Example: /user/users/1
@users.route("/users/<int:user_id>", methods=["GET"])
def get_ngo(user_id):
    try:
        cursor = db.get_db().cursor()

        # Get User details
        cursor.execute("SELECT * FROM Users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        cursor.close()
        return jsonify(user), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# get user id from last name
@users.route("/users/id/<input>", methods=["GET"])
def get_user_id(input):
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