
import requests
import pandas as pd


url_base='https://sturgeon-boss-regularly.ngrok-free.app'
resposta_fila = requests.get(url_base + '/fila').json()
resposta_fila = pd.read_json(resposta_fila, orient='split')
resposta_fila.iloc[-1]