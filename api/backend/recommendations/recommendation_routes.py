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


'''
{
  "weights": {
    "Prevention": 0.25,
    "Detection and Reporting": 0.15,
    "Rapid Response": 0.10,
    "Health System": 0.20,
    "Compliance with International Norms": 0.20,
    "Risk Environment": 0.10
  },
  "home_country_id": 12,
  "include_home_context": true
}
'''
# Generate personalized country recommendations based on weighted factors
# Example: /recommendations/recommendations
@recommendations.route("/recommendations/recommendations", methods=["POST"])
def get_country_recommendations():
    pass
