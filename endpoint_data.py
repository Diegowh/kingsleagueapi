from models import Team, Player, Matchday, Match, Split, BonusPlayer


def api_documentation():
    documentation = [
        {
            "endpoint": "/leaderboard",
            "description": "Devuelve la tabla de clasificación de la Kings League",
            "parameters":[
                {
                    "name": "team",
                    "endpoint": "/leaderboard/:team_name",
                    "description": "Devuelve la información de un equipo de la leaderboard de la Kings League por Team Name."
                },
                {
                    "name": "bonus-players",
                    "endpoint": "/leaderboard/:team_name/bonus-players",
                    "description": "Devuelve la información de los jugadores 12 y 13 de un equipo de la leaderboard de la Kings League por Team Name."
                },
            ],
        },
        {
            "endpoint": "/matchdays",
            "description": "Devuelve la información de todas las jornadas del split actual de la Kings League.",
            "parameters": [
                {
                    "name": "matchday",
                    "endpoint": "/matchdays/:matchday_id",
                    "description": "Devuelve la información de una jornada del split actual de la Kings league por Matchday Id.",
                },
            ],
        },
        {
            "endpoint": "/presidents",
            "description": "Devuelve los presidentes de la Kings League.",
        },
        {
            "endpoint": "/coaches",
            "description": "Devuelve los coaches de la Kings League.",
        },
    ]
    return documentation

def get_leaderboard():
    teams = Team.query.order_by(Team.position).all()
    leaderboard = []
    for team in teams:
        
        president = Player.query.filter_by(team_name=team.name, role="presidente").first()
        coach = Player.query.filter_by(team_name=team.name, role="entrenador").first()
        players = Player.query.filter(Player.team_name == team.name, Player.role.notin_(["presidente", "entrenador"])).all()
        
        player_list = [{"name": player.name, "role": player.role, "position": player.position} for player in players]
        
        bonus_players = BonusPlayer.query.filter_by(team_name=team.name).all()
        bonus_players_list = [{"name": player.name, "role": player.role, "position": player.position} for player in bonus_players]
        
        entry = {
            "rank": team.position,
            "wins": team.victories,
            "penalty_wins": team.penalty_victories,
            "losses": team.defeats,
            "penalty_losses": team.penalty_defeats,
            "goals_scored": team.goals_scored,
            "goals_conceded": team.goals_conceded,
            "goals_difference": team.goals_difference,
            "team": {
                "name": team.name,
                "president": president.name,
                "coach": coach.name,
                "players": player_list,
                "bonus_players": bonus_players_list,
            }
        }
        leaderboard.append(entry)
    
    return leaderboard



def get_matchdays():
    matchdays = []
    for matchday in Matchday.query.all():
        matchday_dict = {"id": matchday.id, "date": matchday.date}
        matches = Match.query.filter(Match.matchday_id == matchday.id).all()
        
        # cambio match.time a string porque sino me da error al pasaro a json
        matchday_dict["matches"] = [{"home_team_name": match.home_team_name, "away_team_name": match.away_team_name, "time": match.time.strftime("%H:%M") if match.time else None} for match in matches]
        
        matchdays.append(matchday_dict)
    return matchdays


def get_team_bonus_players(team_name):
    bonus_players = BonusPlayer.query.filter_by(team_name=team_name).all()
    bonus_players_list = [{"name": player.name, "role": player.role, "position": player.position} for player in bonus_players]
    
    return bonus_players_list


def get_bonus_players():
    bonus_players = [{"name": player.name, "team_name": player.team_name, "role": player.role, "position": player.position} for player in BonusPlayer.query.all()]
    
    return bonus_players




def get_presidents():
    presidents = Player.query.filter_by(role="presidente").all()
    presidents_list = [{"name": president.name, "team_name": president.team_name} for president in presidents]
    
    return presidents_list



def get_coaches():
    coaches = Player.query.filter_by(role="entrenador").all()
    coaches_list = [{"name": coach.name, "team_name": coach.team_name} for coach in coaches]
    
    return coaches_list


def get_mvps():
    pass


def get_top_scorers():
    pass


def get_top_assists():
    pass