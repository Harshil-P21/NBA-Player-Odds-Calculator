import requests
from bs4 import BeautifulSoup

url = 'https://www.basketball-reference.com/players/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

player_names = []
for letter in soup.find_all('div', {'class': 'section_content'}):
    for link in letter.find_all('a'):
        letter_url = 'https://www.basketball-reference.com' + link.get('href')
        letter_response = requests.get(letter_url)
        letter_soup = BeautifulSoup(letter_response.content, 'html.parser')
        for player in letter_soup.find_all('tr', {'class': 'full_table'}):
            name = player.find('td', {'data-stat': 'player'}).text
            player_names.append(name)

print(player_names)