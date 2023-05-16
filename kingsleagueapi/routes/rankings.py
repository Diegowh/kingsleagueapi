from flask import Blueprint, jsonify
from services.endpoint_data import get_rankings, get_mvps, get_top_scorers, get_top_assists

rankings_bp = Blueprint('rankings', __name__)

@rankings_bp.route('/rankings', defaults={'ranking_name': None})
@rankings_bp.route('/rankings/<ranking_name>')
def rankings_endpoint(ranking_name):
    if ranking_name is None:
        return jsonify(get_rankings())
    elif ranking_name == "mvps":
        return jsonify(get_mvps())
    elif ranking_name == "top-scorers":
        return jsonify(get_top_scorers())
    elif ranking_name == "top-assists":
        return jsonify(get_top_assists())
