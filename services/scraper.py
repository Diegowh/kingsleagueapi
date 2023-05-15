import requests
from bs4 import BeautifulSoup
import datetime
from models.models import Team, Matchday


class Scraper():
    def __init__(self) -> None:
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        self.matchdays_data = self.matchday_data_scrap()
        self.matches_data = self.match_data_scrap()
        self.current_split, self.splits_data = self.split_data_scrap()
        self.players_data = self.player_data_scrap()
        self.teams_data = self.team_data_scrap()
        self.bonus_players_data = self.bonus_player_scrap()
        self.mvp_data = self.mvp_data_scrap()
        self.top_scorers_data = self.top_scorer_data_scrap()
        self.top_assists_data = self.top_assists_data_scrap()
    
    
    def make_request(self, url: str):
        response = requests.get(url, headers=self.HEADERS)
        return BeautifulSoup(response.text, 'html.parser')
    
    
    def split_data_scrap(self):
        url = "https://kingsleague.pro/partidos/"
        soup = self.make_request(url)
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
        
        def filter_player_div(tag):
            if not tag.has_attr('class'):
                return False
            if 'el-item' not in tag['class'] or 'uk-panel' not in tag['class']:
                return False
            if not tag.find('div', class_='el-content uk-panel uk-text-large'):
                return False
            return True
        
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
            soup = self.make_request(url)


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
        soup = self.make_request(url)
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
        soup = self.make_request(url)
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
        soup = self.make_request(url)
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
        soup = self.make_request(url)
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
        soup = self.make_request(url)
        
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
        soup = self.make_request(url)
        
        
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
        soup = self.make_request(url)
        
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