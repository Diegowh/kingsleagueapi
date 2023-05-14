from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
from flask_migrate import Migrate
import os
from models.models import db

import config


from services.database_manager import DatabaseManager

from routes.bonus_players import bonus_players_bp
from routes.coaches import coaches_bp
from routes.documentation import documentation_bp
from routes.leaderboard import leaderboard_bp
from routes.matchdays import matchdays_bp
from routes.presidents import presidents_bp
from routes.coaches import coaches_bp
from routes.rankings import rankings_bp

load_dotenv()


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
    
    # registro los blueprints
    app.register_blueprint(bonus_players_bp)
    app.register_blueprint(coaches_bp)
    app.register_blueprint(documentation_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(matchdays_bp)
    app.register_blueprint(presidents_bp)
    app.register_blueprint(rankings_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=config.DEBUG)