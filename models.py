from app import db

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String, nullable=False)
    
    presidente = db.Column(db.String, nullable=False)
    entrenador = db.Column(db.String, nullable=True)
    jugador_11 = db.Column(db.String, nullable=True)
    jugador_12_nombre = db.Column(db.String, nullable=True)
    jugador_12_posicion = db.Column(db.String, nullable=True)
    jugador_13_nombre = db.Column(db.String, nullable=True)
    jugador_13_posicion = db.Column(db.String, nullable=True)
    jugadores = db.relationship('Player', backref='team', lazy=True)
    
    puntos = db.Column(db.Integer, default=0)
    victorias = db.Column(db.Integer, default=0)
    victorias_penaltis = db.Column(db.Integer, default=0)
    derrotas_penaltis = db.Column(db.Integer, default=0)
    derrotas = db.Column(db.Integer, default=0)
    goles_favor = db.Column(db.Integer, default=0)
    goles_contra = db.Column(db.Integer, default=0)
    diferencia_goles = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f"Team(id={self.id}, team_name={self.team_name}, presidente={self.presidente}, entrenador={self.entrenador}, jugador_11={self.jugador_11}, jugador_12_nombre={self.jugador_12_nombre}, jugador_12_posicion={self.jugador_12_posicion}, jugador_13_nombre={self.jugador_13_nombre}, jugador_13_posicion={self.jugador_13_posicion}, puntos={self.puntos}, victorias={self.victorias}, victorias_penaltis={self.victorias_penaltis}, derrotas_penaltis={self.derrotas_penaltis}, derrotas={self.derrotas}, goles_favor={self.goles_favor}, goles_contra={self.goles_contra}, diferencia_goles={self.diferencia_goles})"


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    player_name = db.Column(db.String, nullable=False)
    posicion = db.Column(db.String, nullable=False)
    partidos = db.Column(db.Integer, nullable=False, default=0)
    goles_encajados = db.Column(db.Integer, nullable=True, default=0)
    penaltis_parados = db.Column(db.Integer, nullable=True, default=0)
    t_amarilla = db.Column(db.Integer, nullable=False, default=0)
    t_roja = db.Column(db.Integer, nullable=False, default=0)
    mvp = db.Column(db.Integer, nullable=False, default=0)
    goles = db.Column(db.Integer, nullable=False, default=0)
    asist = db.Column(db.Integer, nullable=False, default=0)
    reflejo = db.Column(db.Integer, nullable=True, default=0)
    paradas = db.Column(db.Integer, nullable=True, default=0)
    saque = db.Column(db.Integer, nullable=True, default=0)
    estirada = db.Column(db.Integer, nullable=True, default=0)
    velocidad = db.Column(db.Integer, nullable=False, default=0)
    fisico = db.Column(db.Integer, nullable=False, default=0)
    tiro = db.Column(db.Integer, nullable=False, default=0)
    pase = db.Column(db.Integer, nullable=False, default=0)
    talento = db.Column(db.Integer, nullable=False, default=0)
    defensa = db.Column(db.Integer, nullable=False, default=0)


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