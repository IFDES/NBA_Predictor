import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO  # Import StringIO to wrap HTML strings

standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
data = requests.get(standings_url)
soup = BeautifulSoup(data.text, "lxml")
standings_table = soup.select('table.stats_table')[0]
links = standings_table.find_all('a')
links = [l.get("href") for l in links]
links = [l for l in links if '/squads/' in l]
team_urls = [f"https://fbref.com{l}" for l in links]

# Fetch team data
data = requests.get(team_urls[0])

# Wrap HTML in StringIO before passing to read_html
matches = pd.read_html(StringIO(data.text), match="Scores & Fixtures")[0]
soup = BeautifulSoup(data.text, "lxml")
links = soup.find_all('a')
links = [l.get("href") for l in links]
links = [l for l in links if l and 'all_comps/shooting/' in l]

# Fetch shooting stats
data = requests.get(f"https://fbref.com{links[0]}")
shooting = pd.read_html(StringIO(data.text), match="Shooting")[0]
print(shooting.head())
