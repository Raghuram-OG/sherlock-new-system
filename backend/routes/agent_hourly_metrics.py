from flask import Blueprint, jsonify
from services.supabase_service import SupabaseService

agent_hourly_metrics_bp = Blueprint("agent_hourly_metrics", __name__)

@agent_hourly_metrics_bp.route("/agent_hourly_metrics", methods=["GET"])
def get_metrics():
    try:
        data = SupabaseService.get_table_data("agent_hourly_metrics")
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500