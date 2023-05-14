from models.models import Team, Player, Matchday, Match, Split, BonusPlayer, Mvp, TopScorer, TopAssists
from models.models import db
from sqlalchemy import text

from .scraper import Scraper


class DatabaseManager:
    def __init__(self, scraper: Scraper) -> None:
        self.scraper = scraper
    
    
    def update(self):
        self.delete_previous_data()
        self.reset_all_sequences()
        self.update_all_tables()
    

    ###################################################
    #                   RESET                        
    ###################################################
    
    
    
    def delete_previous_data(self):
        Match.query.delete()
        Player.query.delete()
        Team.query.delete()
        Matchday.query.delete()
        Split.query.delete()
        BonusPlayer.query.delete()
        Mvp.query.delete()
        TopScorer.query.delete()
        TopAssists.query.delete()
    
    
    def reset_id_sequence(self, table_name, sequence_name):
        max_id = db.session.execute(text(f"SELECT MAX(id) FROM {table_name};")).scalar() or 0
        db.session.execute(text(f"ALTER SEQUENCE {sequence_name} RESTART WITH {max_id + 1};"))

    def reset_all_sequences(self):
        sequences = [
            ("team", "team_id_seq"),
            ("player", "player_id_seq"),
            ("matchday", "matchday_id_seq"),
            ("match", "match_id_seq"),
            ("split", "split_id_seq"),
            ("bonus_player", "bonus_player_id_seq"),
            ("mvp", "mvp_id_seq"),
            ("top_scorer", "top_scorer_id_seq"),
            ("top_assists", "top_assists_id_seq"),
        ]

        for table_name, sequence_name in sequences:
            self.reset_id_sequence(table_name, sequence_name)

        db.session.commit()
    
    
    def update_all_tables(self):
        self.update_split_table()
        self.update_matchday_table()
        self.update_match_table()
        self.update_team_table()
        self.update_player_table()
        self.update_bonusplayer_table()
        self.update_mvp_table()
        self.update_top_scorers_table()
        self.update_top_assists_table()
        

    ###################################################
    #                   UPDATE                        
    ###################################################
    
    
    def update_player_table(self):
        for player_data in self.scraper.players_data:
            player = Player(
                team_name = player_data["team_name"],
                split_id = self.scraper.current_split,
                name = player_data["name"],
                role = player_data["role"],
                position = player_data["position"],
            )
            db.session.add(player)
        
        db.session.commit()
    
    
    def update_team_table(self):

        for team_data in self.scraper.teams_data:
            team = Team(
                split_id = team_data["split_id"],
                name = team_data["name"],
                points = team_data["points"],
                position = team_data["position"],
                victories = team_data["victories"],
                penalty_victories = team_data["penalty_victories"],
                penalty_defeats = team_data["penalty_defeats"],
                defeats = team_data["defeats"],
                goals_scored = team_data["goals_scored"],
                goals_conceded = team_data["goals_conceded"],
                goals_difference = team_data["goals_difference"],
            )
            db.session.add(team)
            
        # guardo los cambios
        db.session.commit()
    
    
    def update_matchday_table(self):
        for matchday_data in self.scraper.matchdays_data:
            matchday = Matchday(
                date = matchday_data["date"],
            )
            db.session.add(matchday)
        
        db.session.commit()
        
        
    def update_match_table(self):
        for match_data in self.scraper.matches_data:
            match_ = Match(
                matchday_id = match_data["matchday_id"],
                home_team_name = match_data["home_team_name"],
                away_team_name = match_data["away_team_name"],
                time = match_data["time"]
            )
            db.session.add(match_)
        
        db.session.commit()
        
        
    def update_split_table(self):
        for split_data in self.scraper.splits_data:
            split = Split(
                start_date = split_data["start_date"],
            )
            db.session.add(split)
        
        db.session.commit()
        
        
    def update_bonusplayer_table(self):
        for bonusplayer_data in self.scraper.bonus_players_data:
            bonus_player = BonusPlayer(
                name = bonusplayer_data["name"],
                team_name = bonusplayer_data["team_name"],
                role = bonusplayer_data["role"],
                position = bonusplayer_data["position"],
            )
            db.session.add(bonus_player)
            
        db.session.commit()
        
        
    def update_mvp_table(self):
        for mvp_data in self.scraper.mvp_data:
            mvp = Mvp(
                ranking = mvp_data["ranking"],
                name = mvp_data["name"],
                team_name = mvp_data["team_name"],
                mvps = mvp_data["mvps"],
                games_played = mvp_data["games_played"],
            )
            db.session.add(mvp)
        
        db.session.commit()
        
        
    def update_top_scorers_table(self):
        for top_scorer_data in self.scraper.top_scorers_data:
            top_scorer = TopScorer(
                ranking = top_scorer_data["ranking"],
                name = top_scorer_data["name"],
                team_name = top_scorer_data["team_name"],
                goals = top_scorer_data["goals"],
                games_played = top_scorer_data["games_played"],
            )
            db.session.add(top_scorer)
        
        db.session.commit()
        
        
    def update_top_assists_table(self):
        for top_assists_data in self.scraper.top_assists_data:
            top_assists = TopAssists(
                ranking = top_assists_data["ranking"],
                name = top_assists_data["name"],
                team_name = top_assists_data["team_name"],
                assists = top_assists_data["assists"],
                games_played = top_assists_data["games_played"],
            )
            db.session.add(top_assists)
        
        db.session.commit()