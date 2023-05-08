from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    split_id = db.Column(db.Integer, db.ForeignKey('split.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    
    players = db.relationship('Player', backref='team', lazy=True)
    
    points = db.Column(db.Integer, default=0)
    position = db.Column(db.Integer, nullable=False)
    victories = db.Column(db.Integer, default=0)
    penalty_victories = db.Column(db.Integer, default=0)
    penalty_defeats = db.Column(db.Integer, default=0)
    defeats = db.Column(db.Integer, default=0)
    goals_scored = db.Column(db.Integer, default=0)
    goals_conceded = db.Column(db.Integer, default=0)
    goals_difference = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f"Team(id={self.id}, name={self.name}, points={self.points}, victories={self.victories}, penalty_victories={self.penalty_victories}, penalty_defeats={self.penalty_defeats}, defeats={self.defeats}, goals_scored={self.goals_scored}, goals_conceded={self.goals_conceded}, goals_difference={self.goals_difference})"


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    split_id = db.Column(db.Integer, db.ForeignKey('split.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=True)
    position = db.Column(db.String, nullable=True)
    
    matches = db.Column(db.Integer, nullable=True, default=0)
    goals_conceded = db.Column(db.Integer, nullable=True, default=0)
    penalties_saved = db.Column(db.Integer, nullable=True, default=0)
    yellow_cards = db.Column(db.Integer, nullable=True, default=0)
    red_cards = db.Column(db.Integer, nullable=True, default=0)
    mvp = db.Column(db.Integer, nullable=True, default=0)
    goals = db.Column(db.Integer, nullable=True, default=0)
    assists = db.Column(db.Integer, nullable=True, default=0)
    reflex = db.Column(db.Integer, nullable=True, default=0)
    saves = db.Column(db.Integer, nullable=True, default=0)
    kickoff = db.Column(db.Integer, nullable=True, default=0)
    stretch = db.Column(db.Integer, nullable=True, default=0)
    speed = db.Column(db.Integer, nullable=True, default=0)
    physicality = db.Column(db.Integer, nullable=True, default=0)
    shot = db.Column(db.Integer, nullable=True, default=0)
    passing = db.Column(db.Integer, nullable=True, default=0)
    talent = db.Column(db.Integer, nullable=True, default=0)
    defense = db.Column(db.Integer, nullable=True, default=0)


class Matchday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    
    matches = db.relationship('Match', backref='matchday', lazy=True)


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matchday_id = db.Column(db.Integer, db.ForeignKey('matchday.id'), nullable=False)
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    time = db.Column(db.Time, nullable=True)

    home_team = db.relationship('Team', foreign_keys=[home_team_id])
    away_team = db.relationship('Team', foreign_keys=[away_team_id])
    
    
class Split(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    
    teams = db.relationship('Team', backref='split', lazy=True)
    players = db.relationship('Player', backref='split', lazy=True)