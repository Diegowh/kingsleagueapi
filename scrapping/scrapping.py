import requests
from bs4 import BeautifulSoup

url = "https://kingsleague.pro/equipos/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# nombres de equipos
h3_tags = soup.find_all('h3', class_='el-title')
nombres_equipos = [h3.get_text().strip() for h3 in h3_tags]

