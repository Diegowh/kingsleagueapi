from flask import Blueprint, jsonify
from services.endpoint_data import get_bonus_players

bonus_players_bp = Blueprint('bonus_players', __name__)

@bonus_players_bp.route('/bonus-players')
def bonus_players_endpoint():
    return jsonify(get_bonus_players())