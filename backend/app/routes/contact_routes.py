from flask import Blueprint, request, jsonify
from app.services.firestore_service import (
    save_general_query,
    save_enterprise_incident
)

# Blueprint Initialization
contact_bp = Blueprint("contact_bp", __name__)


# -----------------------------------
# GENERAL BUSINESS QUERY ROUTE
# -----------------------------------
@contact_bp.route("/general", methods=["POST"])
def general_query():
    try:
        data = request.get_json()

        # Check for empty body or content-type mismatch
        if not data:
            return jsonify({
                "success": False,
                "message": "No data provided"
            }), 400

        # Strict input validation for crucial frontend data points
        required_fields = ['name', 'email', 'message']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({
                "success": False,
                "message": f"Missing required parameters: {', '.join(missing_fields)}"
            }), 400

        # Save payload to Firestore via Service layer
        result = save_general_query(data)

        if result.get("success"):
            return jsonify({
                "success": True,
                "message": "General query submitted successfully",
                "id": result.get("id")
            }), 200
        else:
            return jsonify(result), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# -----------------------------------
# ENTERPRISE EMERGENCY ROUTE
# -----------------------------------
@contact_bp.route("/enterprise", methods=["POST"])
def enterprise_incident():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "No data provided"
            }), 400

        # Enterprise verification requires deeper B2B operational hooks 
        required_fields = ['name', 'email', 'company', 'message']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({
                "success": False,
                "message": f"Missing critical enterprise metrics: {', '.join(missing_fields)}"
            }), 400

        # Save incident profile to Firebase
        result = save_enterprise_incident(data)

        if result.get("success"):
            return jsonify({
                "success": True,
                "message": "Enterprise incident received. Security team alerted.",
                "id": result.get("id")
            }), 200
        else:
            return jsonify(result), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# -----------------------------------
# ROUTE HEALTH VERIFICATION
# -----------------------------------
@contact_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "PenHex Contact API Sub-router"
    }), 200