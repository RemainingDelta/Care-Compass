from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app


recommendations = Blueprint("recommendations", __name__)

# Get list of all recommendation factors with descriptions
# Example: /recommendations/factors
@recommendations.route("/recommendations/factors", methods=["GET"])
def get_recommendation_factors():
    pass


# Generate personalized country recommendations based on weighted factors
# Example: /recommendations/recommendations
@recommendations.route("/recommendations/recommendations", methods=["POST"])
def get_country_recommendations():
    pass
