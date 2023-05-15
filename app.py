from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
from flask_migrate import Migrate
import os
from models.models import db

import config

from apscheduler.schedulers.blocking import BlockingScheduler
from threading import Thread
from services.db_manager import DatabaseManager

from routes.bonus_players import bonus_players_bp
from routes.documentation import documentation_bp
from routes.leaderboard import leaderboard_bp
from routes.matchdays import matchdays_bp
from routes.presidents import presidents_bp
from routes.coaches import coaches_bp
from routes.rankings import rankings_bp

from services.scraper import Scraper

UPDATE_HOURS = 168


load_dotenv()



def configure_app(app):
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Desactiva una funcion de Flask-SQLAlchemy que rastrea modificaciones en los objetos del modelo (Mejor rendimiento)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JSON_SORT_KEYS'] = False

def create_app():
    app = Flask(__name__)
    configure_app(app)
    
    db.init_app(app)
    migrate = Migrate(app, db)
    
    with app.app_context():
        db.create_all()
        

    
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

sched = BlockingScheduler()


@sched.scheduled_job('interval', hours=UPDATE_HOURS)
def weekly_update():
    with app.app_context():
        scraper = Scraper()
        database_manager = DatabaseManager(scraper=scraper)
        database_manager.update()
        
# inicio el programador en un hilo separado para evitar que interfiera con la ejecucion de app.py
scheduler_thread = Thread(target=sched.start)
scheduler_thread.start()


if __name__ == '__main__':
    app.run(debug=config.DEBUG)