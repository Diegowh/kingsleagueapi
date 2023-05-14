from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
from flask_migrate import Migrate
import os
from models import db

import config
import unicodedata

from database_manager import DatabaseManager
from endpoint_data import leaderboard, matchdays

load_dotenv()

def normalize(name):
    return unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode("utf-8")

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Desactiva una funcion de Flask-SQLAlchemy que rastrea modificaciones en los objetos del modelo (Mejor rendimiento)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

    db.init_app(app)
    migrate = Migrate(app, db)
    
    with app.app_context():
        db.create_all()
        
        database_manager = DatabaseManager()
        database_manager.update()
    
    return app

app = create_app()


@app.route('/leaderboard', defaults={'team_name': None})
@app.route('/leaderboard/<team_name>')
def leaderboard_endpoint(team_name):
    if team_name is None:
        return jsonify(leaderboard())
    else:
        normalized_team_name = normalize(team_name)
    leaderboard_data = leaderboard()
    team_data = next((team for team in leaderboard_data if normalize(team['team']['name']) == normalized_team_name), None)
    if team_data is None:
        return {"error": "Team not found"}, 404
    else:
        return jsonify(team_data)



@app.route('/leaderboard/<team_name>/players-twelve')
def players_twelve_endpoint(team_name):
    # TODO faltan por scrapear los datos de los jugadores 12 y 13
    pass


@app.route('/matchdays')
def matchdays_endpoint():
    return jsonify(matchdays())


@app.route('/matchdays/<int:match_id>')
def matchday_endpoint(match_id):
    matchdays_data = matchdays()
    matchday_data = next((matchday for matchday in matchdays_data if matchday["id"] == match_id), None)
    if matchday_data is None:
        return {"error": "Matchday not found"}, 404
    else:
        return jsonify(matchday_data)


if __name__ == '__main__':
    app.run(debug=config.DEBUG)