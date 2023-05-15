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
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object(config.ProductionConfig())
    elif env == 'testing':
        app.config.from_object(config.TestingConfig())
    else:
        app.config.from_object(config.DevelopmentConfig())

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
        try:
            scraper = Scraper()
            database_manager = DatabaseManager(scraper=scraper)
            database_manager.update()
        except Exception as e:
            print(f"Error during weekly update: {e}")
        
# inicio el programador en un hilo separado para evitar que interfiera con la ejecucion de app.py
scheduler_thread = Thread(target=sched.start)
scheduler_thread.start()


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=str(e)), 404


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])