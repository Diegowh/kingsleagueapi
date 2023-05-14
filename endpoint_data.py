from models import Team, Player, Matchday, Match, Split, BonusPlayer


def leaderboard():
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



def matchdays(): 
    matchdays = [{"id": matchday.id, "date": matchday.date} for matchday in Matchday.query.all()]
    return matchdays