from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

playerInfo = str(input("Please enter players first and last name as follows'LeBron James': "))
playerInfo = (playerInfo.lower()).split()

if (len(playerInfo[1]) >= 5):
    url = f"https://www.basketball-reference.com/players/{playerInfo[1][0]}/{playerInfo[1][:5]+playerInfo[0][:2]+'01'}.html"
else:
    url = f"https://www.basketball-reference.com/players/{playerInfo[1][0]}/{playerInfo[1][:]+playerInfo[0][:2]+'01'}.html"
html = urlopen(url)
soup = BeautifulSoup(html,'html.parser')

# use findALL() to get the column headers
soup.findAll('tr', limit=2)
# use getText()to extract the text we need into a list
headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
headers.remove('Date')

# exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
rows = soup.findAll('tr')[1:6]
player_stats = [[td.getText() for td in rows[i].findAll('td')]
            for i in range(len(rows))]

stats = pd.DataFrame(player_stats, columns = headers)
stats.head(10)

