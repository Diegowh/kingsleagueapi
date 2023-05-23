# 👑 KingsLeague API 👑

**This website is created solely for educational purposes. Kosmos Holdings owns all the logos of the Kings League. This projects is non-profit and is not responsible for any use that may be made of it.**


> KingsLeague API provides data about Kings League leaderboard, teams, presidents, coaches, players, etc. by scrapping [kingsleague.pro](https://kingsleague.pro). 
> Built with **Flask** and **BeautifulSoup** and utilizes **PostgreSQL** to storage all the scraped data. The API performs weekly updates to ensure the data is up do date, as the website itself is updates on a weekly basis.

## Table of contents
* 1
* 2
* 3
* 4
* 5

## ✨ API
Live instance: https://kingsleague-api.onrender.com/

### Endpoints
* GET `/leaderboard`: Return the leaderboard of the Kings League.
* GET `/leadeboard/:team_name`: Return the information of a team from the Kings League leaderboard by Team Name.
* GET `/leaderboard/:team_name/bonus-players`: Return the information of players 12 and 13 from a team on the Kings League leaderboard by Team Name.
* GET `/matchdays`: Return the information of all match days of the current split of the Kings League.
* GET `/matchdays/:matchday_id`: Return the information of a matchday of the current split of the Kings League by Matchday Id.
* GET `/presidents`: Return the presidents of the Kings League.
* GET `/coaches`: Return the coaches of the Kings League.
* GET `/rankings`: Return the players' statistics tables of the Kings League.
* GET `/rankings/mvps`: Return the MVPs table of the Kings League.
* GET `/rankings/top-scorers`: Return the Goals table of the Kings League.
* GET `/rankings/top-assists`: Return the Assists table of the Kings League.


## 💽 Dev enviroment

### Requirements
* 🐍 Python 3.11.2
* 🦄 gunicorn 20.1.0

### Install

* Clone the project.
* Rename the file `.env.example` to `.env`, and edit the configuration according to your needs.
* Make sure you have pip installed:

```
python -m ensurepip --upgrade
```
* Ensure you have the correct Python version (3.11.2). You can check your Python version with the command:

```
python --version
```
* In the project directory, install the dependencies from the `requirements.txt`
```
pip install -r requirements.txt
```

### Launch
```
gunicorn run:app --reload
```
