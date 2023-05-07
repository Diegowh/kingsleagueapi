from dotenv import load_dotenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

import config

load_dotenv()
app = Flask(__name__)
app.config.from_object(config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Desactiva una funcion de Flask-SQLAlchemy que rastrea modificaciones en los objetos del modelo (Mejor rendimiento)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def helloworld():
    return 'Hello, world!'


if __name__ == '__main__':
    app.run(debug=config.DEBUG)