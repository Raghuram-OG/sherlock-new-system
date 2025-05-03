from flask import Blueprint, jsonify, request
from services.supabase_service import SupabaseService
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

calls_bp = Blueprint("calls", __name__)

@calls_bp.route("/calls", methods=["GET"])
def get_calls():
    try:
        days = request.args.get("days", type=int)
        
        # Fetch all calls
        data = SupabaseService.get_table_data("calls")
        logger.debug(f"Fetched {len(data)} calls")
        
        if days is not None and days >= 0 and data:
            # Calculate date threshold
            date_threshold = datetime.utcnow() - timedelta(days=days)
            logger.debug(f"Days filter: {days}, Date threshold: {date_threshold}")
            
            # Filter calls in-memory
            data = [
                call for call in data
                if datetime.fromisoformat(call["date_time"].replace("Z", "+00:00")) >= date_threshold
            ]
            logger.debug(f"Filtered to {len(data)} calls")
        
        if not data:
            logger.warning("No calls found")
            return jsonify([]), 200
        
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error fetching calls: {str(e)}")
        return jsonify({"error": f"Failed to fetch calls: {str(e)}"}), 500