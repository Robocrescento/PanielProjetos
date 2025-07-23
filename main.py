import requests
import pandas as pd
import streamlit as st
from numpy import random
from streamlit_autorefresh import st_autorefresh
url_base='https://sturgeon-boss-regularly.ngrok-free.app'

st_autorefresh(interval=10000, key="autorefresh")

st.header("Encaminhador de pedidos")



if not 'key' in st.session_state:
    st.session_state['key']=random.random()


def pega_dados(estado=None):
    data_fila = requests.get(url_base + '/fila').json()
    #data_solic = requests.get(url_base + '/solicitacoes').json()
    data_fila=pd.read_json(data_fila,orient='split')
    #data_solic=pd.read_json(data_solic, orient='split')
    return data_fila#,data_solic

try:
    df_fila=pega_dados(st.session_state['key'])
except:
    st.warning("Erro no sistema. Contate o desenvolvedor")
    st.stop()
df_fila=df_fila.loc[df_fila['Status']!='finished']
df_fila['Data_Hora']=pd.to_datetime(df_fila['Data_Hora'])
df_fila=df_fila.sort_values('Data_Hora')

params=st.query_params.to_dict()


criar_tarefa=st.button("Pedir para tarefa ser atualizada")

if criar_tarefa:
    resp=requests.get(url_base+'/brognoli').json()
    st.query_params['uid']=resp['uid']
    st.rerun()

mapper_respostas={
    'ongoing':"Atualização rodando",
    'pending':"Atualização na fila",
    'finished':"Atualização na finalizada"
}

if 'uid' in st.query_params.to_dict():
    resp=requests.get(url_base+'/status/'+st.query_params['uid']).json()
    st.subheader(f"Esperando pedido de código:")
    st.write(resp['UID'])
    st.subheader(f"Status")

    st.write(resp['Status']+':'+str(mapper_respostas.get(resp['Status'])))
    st.write(f"Solicitado por {resp['Solicitou']} sobre o projeto {resp['Projeto']}.")
    st.write(f"Tal pedido foi feito ás {resp['Data_Hora']}.")

    uid=st.query_params['uid']

    if uid in df_fila.UID.tolist():
        n_project=len(df_fila.set_index('UID').loc[uid:])-1
        st.subheader(f"Ainda temos {n_project} projetos na sua frente na fila.")

    else:
        n_project=len(df_fila)
        st.subheader(f"Ainda temos {n_project} projetos na sua frente na fila.")


    if st.button('Limpar pedidos'):
        st.query_params.clear()
        st.rerun()


with st.expander("Ver Fila"): st.write(df_fila)