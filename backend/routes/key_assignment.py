from flask import Blueprint, jsonify
from services.supabase_service import SupabaseService

key_assignment_bp = Blueprint("key_assignment", __name__)

@key_assignment_bp.route("/key_assignment", methods=["GET"])
def get_key_assignment():
    try:
        data = SupabaseService.get_table_data("key_assignment")
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500