
import requests

url='https://sturgeon-boss-regularly.ngrok-free.app'
url_base=url
lista=[{'nome':"Rodrigo",'projeto':'brognili','args':{'a':1}}]*3
lista={'lista':lista}
b=requests.post(url+'/batch-start-projeto',json=lista)
uids= {'uids':[e['uid'] for e in b.json()]}


c=requests.post(url+'/status-batch',json=uids)
c.josn()
