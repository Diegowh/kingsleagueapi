from flask import Blueprint, jsonify
from services.endpoint_data import get_matchdays


matchdays_bp = Blueprint('matchdays', __name__)


@matchdays_bp.route('/matchdays')
def matchdays_endpoint():
    return jsonify(get_matchdays())


@matchdays_bp.route('/matchdays/<int:matchday_id>')
def matchday_endpoint(matchday_id):
    matchdays_data = get_matchdays()
    matchday_data = next((matchday for matchday in matchdays_data if matchday["id"] == matchday_id), None)
    if matchday_data is None:
        return {"error": "Matchday not found"}, 404
    else:
        return jsonify(matchday_data)