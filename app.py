from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
from flask_migrate import Migrate
import os
from models import db

import config
import unicodedata
import json

from database_manager import DatabaseManager
from endpoint_data import get_leaderboard, get_matchdays, get_team_bonus_players, api_documentation, get_bonus_players

load_dotenv()

def normalize(name):
    return unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode("utf-8")

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Desactiva una funcion de Flask-SQLAlchemy que rastrea modificaciones en los objetos del modelo (Mejor rendimiento)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JSON_SORT_KEYS'] = False
    

    db.init_app(app)
    migrate = Migrate(app, db)
    
    with app.app_context():
        db.create_all()
        
        database_manager = DatabaseManager()
        database_manager.update()
    
    return app

app = create_app()


@app.route('/')
def documentation():
    response = app.response_class(
        response=json.dumps(api_documentation(), sort_keys=False),
        status=200,
        mimetype='application/json'
    )
    return response

# leaderboard endpoints
@app.route('/leaderboard', defaults={'team_name': None})
@app.route('/leaderboard/<team_name>')
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


@app.route('/leaderboard/<team_name>/bonus-players')
def team_bonus_players_endpoint(team_name):
    normalized_team_name = normalize(team_name)
    bonus_players = get_team_bonus_players(normalized_team_name)
    if not bonus_players:
        return {"error": "Team not found"}, 404
    else:
        return jsonify(bonus_players)


# bonus players endpoint
@app.route('/bonus-players')
def bonus_players_endpoint():
    return jsonify(get_bonus_players())


# matchdays endpoints
@app.route('/matchdays')
def matchdays_endpoint():
    return jsonify(get_matchdays())


@app.route('/matchdays/<int:matchday_id>')
def matchday_endpoint(matchday_id):
    matchdays_data = get_matchdays()
    matchday_data = next((matchday for matchday in matchdays_data if matchday["id"] == matchday_id), None)
    if matchday_data is None:
        return {"error": "Matchday not found"}, 404
    else:
        return jsonify(matchday_data)




if __name__ == '__main__':
    app.run(debug=config.DEBUG)