
import requests

url_base='https://sturgeon-boss-regularly.ngrok-free.app'

data_fila = requests.get(url_base + '/fila').json()
requests.get(url_base + '/fila').text

lista=[{'nome':"Rodrigo",'projeto':'brognili','args':{'a':1}}]*3
lista={'lista':lista}
b=requests.post(url_base+'/batch-start-projeto',json=lista)
uids= {'uids':[e['uid'] for e in b.json()]}


c=requests.post(url_base+'/status-batch',json=uids)
c.josn()
