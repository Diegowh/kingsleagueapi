from flask import Blueprint, jsonify
from services.endpoint_data import get_coaches

coaches_bp = Blueprint('coaches', __name__)

@coaches_bp.route('/coaches')
def coaches_endpoint():
    return jsonify(get_coaches())