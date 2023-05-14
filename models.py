from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    split_id = db.Column(db.Integer, db.ForeignKey('split.id'), nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)
    
    
    points = db.Column(db.Integer, default=0)
    position = db.Column(db.Integer, nullable=False)
    victories = db.Column(db.Integer, default=0)
    penalty_victories = db.Column(db.Integer, default=0)
    penalty_defeats = db.Column(db.Integer, default=0)
    defeats = db.Column(db.Integer, default=0)
    goals_scored = db.Column(db.Integer, default=0)
    goals_conceded = db.Column(db.Integer, default=0)
    goals_difference = db.Column(db.Integer, default=0)



class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String, nullable=False)
    split_id = db.Column(db.Integer, db.ForeignKey('split.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=True)
    position = db.Column(db.String, nullable=True)



class Matchday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    
    matches = db.relationship('Match', backref='matchday', lazy=True)


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matchday_id = db.Column(db.Integer, db.ForeignKey('matchday.id'), nullable=False)
    home_team_name = db.Column(db.String, nullable=False)
    away_team_name = db.Column(db.String, nullable=False)
    time = db.Column(db.Time, nullable=True)


    
class Split(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    start_date = db.Column(db.Date, nullable=False)
    
    teams = db.relationship('Team', backref='split', lazy=True)
    players = db.relationship('Player', backref='split', lazy=True)
    

class BonusPlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    team_name = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=True)