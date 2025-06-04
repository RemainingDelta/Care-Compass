from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app


recommendations = Blueprint("recommendations", __name__)

# Get list of all recommendation factors with descriptions
# Example: /recommendations/factors
@recommendations.route("/factors", methods=["GET"])
def get_recommendation_factors():
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
@recommendations.route("/recommendations", methods=["POST"])
def get_country_recommendations():
    pass
