from flask import Blueprint, jsonify
from services.endpoint_data import api_documentation

documentation_bp = Blueprint('documentation', __name__)

@documentation_bp.route('/')
def documentation():
    return jsonify(api_documentation())