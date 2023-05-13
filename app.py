from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
from flask_migrate import Migrate
import os
from models import db

import config

from database_manager import DatabaseManager

load_dotenv()

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

prueba = {
    "cosa": 15,
    "otra_cosa": "mas cositas",
    "Viento": "Muchisimo"
}

@app.route('/api/leaderboard')
def leaderboard():
    return jsonify(prueba)


if __name__ == '__main__':
    app.run(debug=config.DEBUG)