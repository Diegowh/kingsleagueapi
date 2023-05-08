import requests
from bs4 import BeautifulSoup, Tag
from models import Team, Player, Matchday, Match, Split
from models import db
from sqlalchemy import text
import datetime



HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def filter_player_div(tag):
    if not tag.has_attr('class'):
        return False
    if 'el-item' not in tag['class'] or 'uk-panel' not in tag['class']:
        return False
    if not tag.find('div', class_='el-content uk-panel uk-text-large'):
        return False
    return True



class DatabaseManager:
    def __init__(self) -> None:
        self.players_data = self.player_data_scrap()
        self.matches_data = self.match_data_scrap()
        self.matchdays_data = self.matchday_data_scrap()
        self.current_split, self.splits_data = self.split_data_scrap()
        self.teams_data = self.team_data_scrap()
    
    
    def update(self):
        self.delete_previous_data()
        self.reset_id_sequences()
        self.update_all_tables()
    

    ###################################################
    #                   RESET                        
    ###################################################
    
    
    
    def delete_previous_data(self):
        Team.query.delete()
        Player.query.delete()
        Matchday.query.delete()
        Match.query.delete()
        Split.query.delete()
    
    
    def reset_id_sequences(self):
        # team_id
        max_team_id = db.session.execute(text("SELECT MAX(id) FROM team;")).scalar() or 0
        db.session.execute(text(f"ALTER SEQUENCE team_id_seq RESTART WITH {max_team_id + 1};"))
        
        # player_id
        max_player_id = db.session.execute(text("SELECT MAX(id) FROM player;")).scalar() or 0
        db.session.execute(text(f"ALTER SEQUENCE player_id_seq RESTART WITH {max_player_id + 1};"))
        
        # matchday_id
        max_matchday_id = db.session.execute(text("SELECT MAX(id) FROM matchday;")).scalar() or 0
        db.session.execute(text(f"ALTER SEQUENCE matchday_id_seq RESTART WITH {max_matchday_id + 1};"))
        
        # match_id
        max_match_id = db.session.execute(text("SELECT MAX(id) FROM match;")).scalar() or 0
        db.session.execute(text(f"ALTER SEQUENCE match_id_seq RESTART WITH {max_match_id + 1};"))
        
        # split_id
        max_split_id = db.session.execute(text("SELECT MAX(id) FROM split;")).scalar() or 0
        db.session.execute(text(f"ALTER SEQUENCE split_id_seq RESTART WITH {max_split_id + 1};"))
    
        db.session.commit()
    
    
    def update_all_tables(self):
        self.update_team_table()
        self.update_matchday_table()
        self.update_match_table()
        self.update_player_table()
        self.update_split_table()
    
    
    def reset_team_id_sequence(self):
        max_id = db.session.execute(text("SELECT MAX(id) FROM team;")).scalar() or 0
        db.session.execute(text(f"ALTER SEQUENCE team_id_seq RESTART WITH {max_id + 1};"))
        db.session.commit()
    
    
    def reset_player_id_sequence(self):
        max_id = db.session.execute(text("SELECT MAX(id) FROM player;")).scalar() or 0
        db.session.execute(text(f"ALTER SEQUENCE player_id_seq RESTART WITH {max_id + 1};"))
        db.session.commit()
        
        
    ###################################################
    #                   SCRAP                    
    ###################################################


    def split_data_scrap(self):
        url = "https://kingsleague.pro/partidos/"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        split_select = soup.find("select", {"id": "split"})
        split_options = split_select.find_all("option")
        
        splits_data = []
        current_split = None
        
        for split_option in split_options:
            split_id = int(split_option["value"])
            start_date = self.matchdays_data[0]["date"]
            
            split_data = {
                "id": split_id,
                "start_date": start_date,
            }
            splits_data.append(split_data)
            
            if "selected" in split_option.attrs:
                current_split = split_id
    
        return current_split, splits_data



    def player_data_scrap(self) -> list:
        endpoint_team_names = {
            "1K FC": "1k",
            "Aniquiladores FC": "aniquiladores-fc",
            "El Barrio": "el-barrio",
            "Jijantes FC": "jijantes-fc",
            "Kunisports": "kunisports",
            "Los Troncos FC": "los-troncos-fc",
            "PIO FC": "pio-fc",
            "Porcinos FC": "porcinos-fc",
            "Rayo de Barcelona": "rayo-barcelona",
            "Saiyans FC": "saiyans-fc",
            "Ultimate Móstoles": "ultimate-mostoles",
            "xBuyer Team": "xbuyer-team",
        }
        
        players_data = []
        
        for index, (endpoint) in enumerate(endpoint_team_names.values()):
            team_id = index + 1
            url = f"https://kingsleague.pro/team/{endpoint}"
            response = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(response.text, 'html.parser')



            for player_div in soup.find_all(filter_player_div):
                position = player_div.find('span').get_text(strip=True)
                if position == "presidentepresidente":
                    position = position.replace("presidente", "", 1)
                elif position == "entrenadorentrenador":
                    position = position.replace("entrenador", "", 1)
                print("Position: ", position)
                player_name = player_div.find('h3').get_text(strip=True)
                print("Player name: ", player_name)
                player_data = {
                    'team_id': team_id,
                    'name': player_name,
                    'position': position,
                }
                
                player_stats_container = player_div.find('div', class_='league-player')
                if player_stats_container is not None:
                    for stat in player_stats_container.find_all("div", class_="uk-margin"):
                        stat_name = stat.find('div', class_='el-meta').get_text(strip=True)
                        stat_value = stat.find('h3', class_='el-title').get_text(strip=True) if stat.find('h3', class_='el-title') else None
                        stat_key = stat_name.lower().replace('.', '').replace(' ', '_')
                        player_data[stat_key] = int(stat_value) if stat_value else None
                
                # establezco estadisticas que no existen en ciertos roles en None
                if position not in ["Presidente", "Entrenador"]:
                    for stat_key in ['velocidad', 'fisico', 'tiro', 'pase', 'talento', 'defensa', 'reflejo', 'paradas', 'saque', 'estirada']:
                        if stat_key not in player_data:
                            player_data[stat_key] = None

                if position == "Portero":
                    for stat_key in ['reflejo', 'paradas', 'saque', 'estirada']:
                        if stat_key not in player_data:
                            player_data[stat_key] = None

                else:
                    player_data['reflejo'] = None
                    player_data['paradas'] = None
                    player_data['saque'] = None
                    player_data['estirada'] = None

                players_data.append(player_data)

        return players_data
    
    
    def team_data_scrap(self) -> list:
        url = f"https://kingsleague.pro/clasificacion/"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("tr.el-item")
        teams_data = []
        
        for row in rows:
            team_data = {}
            
            columns = row.find_all("td.fs-table-column")
            
            team_data["split_id"] = self.current_split
            team_data["name"] = columns[2].text.strip()
            team_data["points"] = int(columns[3].text.strip())
            team_data["position"] = int(columns[0].text.strip())
            team_data["victories"] = int(columns[4].text.strip())
            team_data["penalty_victories"] = int(columns[5].text.strip())
            team_data["penalty_defeats"] = int(columns[6].text.strip())
            team_data["defeats"] = int(columns[7].text.strip())
            team_data["goals_scored"] = int(columns[8].text.strip())
            team_data["goals_conceded"] = int(columns[9].text.strip())
            team_data["goals_difference"] = int(columns[10].text.strip())
            
            teams_data.append(team_data)
        
        return  teams_data
    
    
    def matchday_data_scrap(self) -> list:
        url = "https://kingsleague.pro/partidos/"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        
        matchday_sections = soup.find_all("div", class_="fs-table uk-overflow-auto uk-margin-large-bottom calendar-match uk-hidden")
        
        matchdays_data = []
        
        for matchday_section in matchday_sections:
            date_str = matchday_section.find('h3', class_='el-table-title').text.strip().split('–')[-1].strip()
            date = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()
            matchday_data = {
                "date": date,
            }
            matchdays_data.append(matchday_data)
        
        return matchdays_data
    
    
    def match_data_scrap(self) -> list:
        url = "https://kingsleague.pro/partidos/"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        
        matchday_sections = soup.find_all("div", class_="fs-table uk-overflow-auto uk-margin-large-bottom calendar-match uk-hidden")
        
        matches_data = []
        
        
        for index, matchday_section in enumerate(matchday_sections):
            match_rows = matchday_section.find_all("tr", class_="el-item fs-table-row")
            
            for match_row in match_rows:
                time_str = match_row.find_all('div', class_='el-text_4')[0].text.strip()
                time = datetime.datetime.strptime(time_str, '%H:%M').time()
                
                home_team_name = match_row.find_all('div', class_='el-text_1')[0].text.strip()
                away_team_name = match_row.find_all('div', class_='el-text_1')[2].text.strip()
                
                # consulto tabla Team para obtener los ID
                home_team = Team.query.filter_by(name=home_team_name).first()
                away_team = Team.query.filter_by(name=away_team_name).first()
                
                matchday_id = index + 1
                matchday = Matchday.query.get(matchday_id)
                
                if home_team and away_team and matchday:
                    match_data = {
                        "matchday_id": matchday.id,
                        "home_team_id": home_team.id,
                        "away_team_id": away_team.id,
                        "time": time,
                    }
                    matches_data.append(match_data)
                    
        return matches_data
    
    
    ###################################################
    #                   UPDATE                        
    ###################################################
    
    
    def update_player_table(self):
        for player_data in self.players_data:
            player = Player(
                team_id = player_data["team_id"],
                split_id = self.current_split,
                name = player_data["name"],
                role = player_data["role"],
                position = player_data["position"],
                matches = player_data["partidos"],
                goals_conceded = player_data["goles encajados"],
                penalties_saved = player_data["penaltis parados"],
                yellow_cards = player_data["t.amarilla"],
                red_cards = player_data["t.roja"],
                mvp = player_data["mvp"],
                goals = player_data["goles"],
                assists = player_data["asist."],
                reflex = player_data["reflejo"],
                saves = player_data["paradas"],
                kickoff = player_data["saque"],
                stretch = player_data["estirada"],
                speed = player_data["velocidad"],
                physicality = player_data["físico"],
                shot = player_data["tiro"],
                passing = player_data["pase"],
                talent = player_data["talento"],
                defense = player_data["defensa"],
            )
            db.session.add(player)
        
        db.session.commit()
    
    
    def update_team_table(self):
        for team_data in self.teams_data:
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
        for matchday_data in self.matchdays_data:
            matchday = Matchday(
                date = matchday_data["date"],
            )
            db.session.add(matchday)
        
        db.session.commit()
        
        
    def update_match_table(self):
        for match_data in self.matches_data:
            match_ = Match(
                matchday_id = match_data["matchday_id"],
                home_team_id = match_data["home_team_id"],
                away_team_id = match_data["away_team_id"],
                time = match_data["time"]
            )
            db.session.add(match_)
        
        db.session.commit()
        
        
    def update_split_table(self):
        for split_data in self.splits_data:
            split = Split(
                start_date = split_data["start_date"],
            )
            db.session.add(split)
        
        db.session.commit()