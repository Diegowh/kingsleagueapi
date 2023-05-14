import requests
from bs4 import BeautifulSoup, Tag
from models.models import Team, Player, Matchday, Match, Split, BonusPlayer, Mvp, TopScorer, TopAssists
from models.models import db
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
        self.matchdays_data = self.matchday_data_scrap()
        self.matches_data = self.match_data_scrap()
        self.current_split, self.splits_data = self.split_data_scrap()
        self.players_data = self.player_data_scrap()
        self.teams_data = self.team_data_scrap()
        self.bonus_players_data = self.bonus_player_scrap()
        self.mvp_data = self.mvp_data_scrap()
        self.top_scorers_data = self.top_scorer_data_scrap()
        self.top_assists_data = self.top_assists_data_scrap()
    
    
    def update(self):
        self.delete_previous_data()
        self.reset_id_sequences()
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
        
        # bonus_player_id
        max_bonus_player_id = db.session.execute(text("SELECT MAX(id) FROM bonus_player;")).scalar() or 0
        db.session.execute(text(f"ALTER SEQUENCE bonus_player_id_seq RESTART WITH {max_bonus_player_id + 1};"))
        
        # mvp_id
        max_mvp_id = db.session.execute(text("SELECT MAX(id) FROM mvp;")).scalar() or 0
        db.session.execute(text(f"ALTER SEQUENCE mvp_id_seq RESTART WITH {max_mvp_id + 1};"))

        # top_scorer_id
        max_top_scorer_id = db.session.execute(text("SELECT MAX(id) FROM top_scorer;")).scalar() or 0
        db.session.execute(text(f"ALTER SEQUENCE top_scorer_id_seq RESTART WITH {max_top_scorer_id + 1};"))
        db.session.commit()
        
        # top_assists_id
        max_top_assists_id = db.session.execute(text("SELECT MAX(id) FROM top_assists;")).scalar() or 0
        db.session.execute(text(f"ALTER SEQUENCE top_assists_id_seq RESTART WITH {max_top_assists_id + 1};"))
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
        
        for key, value in endpoint_team_names.items():
            # itero por cada equipo
            url = f"https://kingsleague.pro/team/{value}"
            response = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(response.text, 'html.parser')


            team_lenght = len(soup.find_all("h3", class_="el-title uk-heading-medium uk-font-secondary uk-text-secondary uk-margin-remove-top uk-margin-remove-bottom"))

            for player_i in range(team_lenght):
                # itero por cada jugador de cada equipo
                player_data = {
                    "team_name": key,
                    "split_id": self.current_split,
                    "name": None,
                    "role": None,
                    "position": None,
                }
                # extraigo los datos del presidente de otro sitio porque la pagina web la ha hecho un orangutan
                if player_i == 0:
                    player_data["name"] = soup.find_all("h3", class_="el-title uk-heading-medium uk-font-secondary uk-text-secondary uk-margin-remove-top uk-margin-remove-bottom")[player_i]
                    player_data["role"] = "president"
                    player_data["position"] = "president"
                    
                elif player_i == 1:
                    player_data["position"] = "player_11"
                    player_data["name"] = soup.find_all("h1", class_="uk-heading-large uk-font-secondary uk-text-secondary uk-margin-large uk-margin-remove-top uk-text-center")[player_i]
                    player_data["role"] = soup.find_all("div", class_="uk-panel uk-text-large uk-text-secondary uk-text-bold uk-text-uppercase uk-margin")
                    
                elif player_i == team_lenght - 1:
                    player_data["position"] = "coach"
                    player_data["role"] = "coach"
                    player_data["name"] = soup.find_all("h1", class_="uk-heading-large uk-font-secondary uk-text-secondary uk-margin-large uk-margin-remove-top uk-text-center")[0]

            
            all_player_divs = soup.find_all(filter_player_div)
            all_stats_container = soup.find_all("div", class_="container-stats")
            
            for player_div, stats_container in zip(all_player_divs, all_stats_container):
                position = player_div.find('span').get_text(strip=True)
                if position == "presidentepresidente":
                    position = position.replace("presidente", "", 1)
                elif position == "entrenadorentrenador":
                    position = position.replace("entrenador", "", 1)
                    
                player_name = player_div.find('h3').get_text(strip=True)
                player_role = player_div.find("div", class_= "el-content uk-panel uk-text-large")
                
                if hasattr(player_role.contents[0], 'text'):
                    role = player_role.contents[0].text.split('<')[0].strip()
                else:
                    role = player_role.contents[0].strip()[0]
                    
                
                # checkeo si role esta duplicado
                if len(role) == 21:
                    role = role.split(" ")[0]
            
                
                stats_divs = stats_container.find_all('div', class_='el-item uk-panel uk-margin-remove-first-child')
                player_stats = {}
                player_data = {
                    'team_name': key,
                    'name': player_name,
                    'position': position,
                    'role': role,
                }
                    
                for stat_div in stats_divs:
                    stat_name = stat_div.find('div').get_text(strip=True)
                    stat_value_div = stat_div.find('h3')
                    if stat_value_div is None:
                        stat_value = None
                    else:
                        stat_value = stat_value_div.get_text(strip=True)
                    player_stats[stat_name] = stat_value
                

                players_data.append(player_data)

        return players_data
    
    
    def mvp_data_scrap(self):
        url = f"https://kingsleague.pro/estadisticas/mvp/"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        mvps_list = []
        table_rows = soup.find('tbody').find_all('tr')
        for i, tr in enumerate(table_rows):
            mvp_data = {
                "ranking": i + 1,
                "name": tr.find_all("td")[1].find("div").text.strip(),
                "team_name": tr.find_all("td")[3].find("div").text.strip(),
                "mvps": tr.find_all("td")[4].find("div").text.strip(),
                "games_played": tr.find_all("td")[5].find("div").text.strip(),
            }
            mvps_list.append(mvp_data)
        
        return mvps_list
    
    
    def top_scorer_data_scrap(self):
        url = f"https://kingsleague.pro/estadisticas/goles/"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        top_scorers_list = []
        table_rows = soup.find('tbody').find_all('tr')
        for i, tr in enumerate(table_rows):
            top_scorer_data = {
                "ranking": i + 1,
                "name": tr.find_all("td")[1].find("div").text.strip(),
                "team_name": tr.find_all("td")[3].find("div").text.strip(),
                "goals": tr.find_all("td")[4].find("div").text.strip(),
                "games_played": tr.find_all("td")[5].find("div").text.strip(),
            }
            top_scorers_list.append(top_scorer_data)
        
        return top_scorers_list
    
    
    def top_assists_data_scrap(self):
        url = f"https://kingsleague.pro/estadisticas/asistencias/"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        table_rows = soup.find('tbody').find_all('tr')
        top_assists_list = []
        for i, tr in enumerate(table_rows):
            top_assists_data = {
                "ranking": i + 1,
                "name": tr.find_all("td")[1].find("div").text.strip(),
                "team_name": tr.find_all("td")[3].find("div").text.strip(),
                "assists": tr.find_all("td")[4].find("div").text.strip(),
                "games_played": tr.find_all("td")[5].find("div").text.strip(),
            }
            top_assists_list.append(top_assists_data)
        
        return top_assists_list
    
    
    def team_data_scrap(self) -> list:
        url = f"https://kingsleague.pro/clasificacion/"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        tbody = soup.find("tbody")
        teams_data = []
        
        for tr in tbody.find_all('tr'):
            team_data = {}
            
            columns = tr.find_all('td')
            
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
            match_rows = matchday_section.find_all("tr")
            
            for match_row in match_rows:
                time_str = match_row.find_all('td')[3].text.strip()
                
                try:
                    time = datetime.datetime.strptime(time_str, '%H:%M').time()
                except ValueError:
                    time = None

                home_team_name = match_row.find_all('td')[0].text.strip()
                away_team_name = match_row.find_all('td')[6].text.strip()

                # consulto tabla Team para obtener los ID
                home_team = Team.query.filter_by(name=home_team_name).first()
                
                away_team = Team.query.filter_by(name=away_team_name).first()

                matchday_id = index + 1
                matchday = Matchday.query.get(matchday_id)

                if home_team and away_team and matchday:
                    match_data = {
                        "matchday_id": matchday_id,
                        "home_team_name": home_team.name,
                        "away_team_name": away_team.name,
                        "time": time,
                    }
                    matches_data.append(match_data)

        return matches_data
    
    
    def bonus_player_scrap(self):
        url = "https://kingsleague.pro/jugador-12/"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        
        card_divs = [div for div in soup.find_all("div", class_="fs-grid-item-holder uk-flex uk-flex-column")]
        
        players_info = []
        
        for card_div in card_divs:
            team_name = card_div.find("div", class_="fs-grid-text fs-grid-text-2 uk-text-lead uk-text-secondary uk-margin-remove-bottom uk-margin-remove-top").text.strip()
            
            player_name = card_div.find("h3", class_="fs-grid-meta fs-grid-meta-3 uk-heading-medium uk-heading-medium uk-text-secondary uk-link-reset uk-margin-remove-bottom uk-margin-remove-top").text.strip()
            
            position = card_div.find("div", class_="fs-grid-text fs-grid-text-4 uk-heading-small uk-text-primary uk-margin-remove-bottom uk-margin-remove-top").text.strip()
            
            role = card_div.find("div", class_="fs-grid-meta fs-grid-meta-1 uk-text-secondary").text.strip()

            players_info.append({
                "team_name": team_name,
                "name": player_name,
                "position": f"jugador {position}",
                "role": role,
            })
        return players_info
    
    ###################################################
    #                   UPDATE                        
    ###################################################
    
    
    def update_player_table(self):
        # print(self.players_data)
        for player_data in self.players_data:
            player = Player(
                team_name = player_data["team_name"],
                split_id = self.current_split,
                name = player_data["name"],
                role = player_data["role"],
                position = player_data["position"],
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
                home_team_name = match_data["home_team_name"],
                away_team_name = match_data["away_team_name"],
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
        
        
    def update_bonusplayer_table(self):
        for bonusplayer_data in self.bonus_players_data:
            bonus_player = BonusPlayer(
                name = bonusplayer_data["name"],
                team_name = bonusplayer_data["team_name"],
                role = bonusplayer_data["role"],
                position = bonusplayer_data["position"],
            )
            db.session.add(bonus_player)
            
        db.session.commit()
        
        
    def update_mvp_table(self):
        for mvp_data in self.mvp_data:
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
        for top_scorer_data in self.top_scorers_data:
            top_scorer = TopScorer(
                ranking = top_scorer_data["ranking"],
                name = top_scorer_data["name"],
                team_name = top_scorer_data["team_name"],
                goals = top_scorer_data["goals"],
                games_played = top_scorer_data["games_played"],
            )
            db.session.add(top_scorer)
        
        db.session.commit()
        
        
        self.top_assists_data = self.top_assists_data_scrap()
        
    def update_top_assists_table(self):
        for top_assists_data in self.top_assists_data:
            top_assists = TopAssists(
                ranking = top_assists_data["ranking"],
                name = top_assists_data["name"],
                team_name = top_assists_data["team_name"],
                assists = top_assists_data["assists"],
                games_played = top_assists_data["games_played"],
            )
            db.session.add(top_assists)
        
        db.session.commit()