from flask import Blueprint, jsonify
from services.endpoint_data import get_leaderboard, get_team_bonus_players
import unicodedata


def normalize(name):
    return unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode("utf-8")

leaderboard_bp = Blueprint('leaderboard', __name__)

# leaderboard endpoints
@leaderboard_bp.route('/leaderboard', defaults={'team_name': None})
@leaderboard_bp.route('/leaderboard/<team_name>')
def leaderboard_endpoint(team_name):
    if team_name is None:
        return jsonify(get_leaderboard())
    else:
        normalized_team_name = normalize(team_name)
        leaderboard_data = get_leaderboard()
        team_data = next((team for team in leaderboard_data if normalize(team['team']['name']) == normalized_team_name), None)
        if team_data is None:
            return {"error": "Team not found"}, 404
        else:
            return jsonify(team_data)


@leaderboard_bp.route('/leaderboard/<team_name>/bonus-players')
def team_bonus_players_endpoint(team_name):
    normalized_team_name = normalize(team_name)
    bonus_players = get_team_bonus_players(normalized_team_name)
    if not bonus_players:
        return {"error": "Team not found"}, 404
    else:
        return jsonify(bonus_players)