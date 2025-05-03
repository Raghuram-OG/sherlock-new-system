from flask import Blueprint, jsonify
from services.supabase_service import SupabaseService

agents_bp = Blueprint("agents", __name__)

@agents_bp.route("/agents", methods=["GET"])
def get_agents():
    try:
        data = SupabaseService.get_table_data("agents")
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500