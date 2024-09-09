import requests
from bs4 import BeautifulSoup
import pandas as pd

DATE_REFERENCE = '2024-09-01'

url_base = "https://limitlesstcg.com/tournaments/jp?show=50"

response = requests.get(url_base)
soup = BeautifulSoup(response.content, "html.parser")

table_rows = soup.select("tr")

for row in range(1, len(table_rows)):

    tournament_date = table_rows[row].get('data-date')

    if tournament_date >= DATE_REFERENCE:

        tournament_url = table_rows[row].select("a")[0].get('href')

        tournament_code = tournament_url.split('/')[-1]

        response_aux = requests.get(tournament_url)
        soup_aux = BeautifulSoup(response_aux.content, "html.parser")

        tournament_rows = soup_aux.select("tr")

        decks = []

        for row in range(1, len(tournament_rows)):
            pokemon1 = ''
            pokemon2 = ''
            try:
                pokemon1 = tournament_rows[row].select('a')[1].select('img')[0].get('alt')
            except:
                pokemon1 = ''
            try:
                pokemon2 = tournament_rows[row].select('a')[1].select('img')[1].get('alt')
            except:
                pokemon2 = ''
            
            deck = pokemon1 + ' ' + pokemon2
            decks.append(deck)

        range_list = list(range(1, len(decks) + 1))

        df_tournament = pd.DataFrame(columns=['position', 'deck'])
        df_tournament['position'] = range_list
        df_tournament['deck'] = decks

        df_tournament.to_csv('./torneios/tournament_{id}.csv'.format(id=tournament_code))