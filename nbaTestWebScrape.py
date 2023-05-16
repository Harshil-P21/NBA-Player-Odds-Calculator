from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import sys

count = 1
playerPage = '0'+str(count)
playerInfo = str(input("Please enter players first and last name as follows'LeBron James': "))
while playerInfo != 'n':
    playerName = playerInfo
    playerInfo = playerInfo.replace(".","")
    playerInfo = playerInfo.replace("'","")
    playerInfoList = (playerInfo.lower()).split()

    if (len(playerInfo[1]) >= 5):
        url = f"https://www.basketball-reference.com/players/{playerInfoList[1][0]}/{playerInfoList[1][:5]+playerInfoList[0][:2]+playerPage}.html"
    else:
        url = f"https://www.basketball-reference.com/players/{playerInfoList[1][0]}/{playerInfoList[1][:]+playerInfoList[0][:2]+playerPage}.html"
    html = urlopen(url)
    soup = BeautifulSoup(html,'html.parser')

    # use findALL() to get the column headers
    soup.findAll('tr', limit=2)
    # use getText()to extract the text we need into a list
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
    #headers.remove('Date')

    # exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
    rows = soup.findAll('tr')[1:6]

    player_stats = [[td.getText() for td in rows[i].findAll('td')]
                for i in range(len(rows))]

    dates = [[th.getText() for th in rows[i].findAll('th')] for i in range(len(rows))]


    for i in range(len(player_stats)):
        player_stats[i].insert(0,dates[i])


    stats = pd.DataFrame(player_stats, columns = headers)

    print (stats)

    nextPlayer = str(input("If this isn't the correct player but has the same name type 'y', if it is the correct player enter 'n': "))
    while (nextPlayer != 'y'):
        rawStatsWanted = (str(input("What stat would you like to see the average of for the past 5 games the player has played (enter 'q' to stop or 'n' for new player): ")))
        while (rawStatsWanted != 'q' and rawStatsWanted != 'n'):
            statsWanted = (rawStatsWanted).lower()
            for col in stats.columns:
                if ((str(col)).lower() == statsWanted):
                    stats = stats.astype({col:'float'})
                    print (f"The average {rawStatsWanted} for {playerName} is {round(stats[col].mean(),1)}")
            rawStatsWanted = (str(input("What stat would you like to see the average of for the past 5 games the player has played (enter 'q' to stop or 'n' for new player): ")))
        if (rawStatsWanted == 'q'):
            sys.exit()
        else:
            playerInfo = str(input("Please enter players first and last name as follows'LeBron James': "))
    if (nextPlayer =='y'):
        count+= 1
        playerPage = '0'+str(count)
    