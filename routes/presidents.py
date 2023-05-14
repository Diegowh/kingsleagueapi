from flask import Blueprint, jsonify
from services.endpoint_data import get_presidents

presidents_bp = Blueprint('presidents', __name__)

@presidents_bp.route('/presidents')
def presidents_endpoint():
    return jsonify(get_presidents())