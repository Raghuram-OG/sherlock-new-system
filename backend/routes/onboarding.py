from flask import Blueprint, jsonify
from services.supabase_service import SupabaseService

onboarding_bp = Blueprint("onboarding", __name__)

@onboarding_bp.route("/onboarding", methods=["GET"])
def get_onboarding():
    try:
        data = SupabaseService.get_table_data("onboarding")
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500