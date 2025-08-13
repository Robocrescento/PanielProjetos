import requests
import pandas as pd
from numpy import random
from streamlit_autorefresh import st_autorefresh
import streamlit as st
url_base='https://sturgeon-boss-regularly.ngrok-free.app'
nome='Rod'
args='asdf'
projeto='projeto'
st_autorefresh(interval=20000, key="autorefresh")

st.header("Encaminhador de pedidos")

nome=st.text_input("Me diga seu nome")
if nome.strip() is '':
    st.stop()


#if nome.strip().lower()=='daniel':


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
df_fila=df_fila.loc[df_fila['Status']=='pending']
df_fila['Data_Hora']=pd.to_datetime(df_fila['Data_Hora'])
df_fila=df_fila.sort_values('Data_Hora')


params=st.query_params.to_dict()


criar_tarefa_Omie=st.button("Download Extrato Omie Brognoli.")

if criar_tarefa_Omie:
    resp=requests.get(url_base+f'/start-projeto?&projeto={'brognoli'}&nome={nome}&argumentos={'args'}')
    resp.text
    resp=resp.json()
    st.query_params['uid']=resp['uid']
    st.rerun()

mapper_respostas={
    None:'Atualização ainda não está na fila',
    'ongoing':"Atualização rodando",
    'pending':"Atualização na fila",
    'finished':"Finalizada",
    'error':"Erro de execução",
}

if 'uid' in st.query_params.to_dict():
    resp=requests.get(url_base+'/status/'+st.query_params['uid'])
    resp=resp.json()
    st.subheader(f"Esperando pedido de código:")
    #st.write(resp['UID'])
    st.subheader(f"Pedido:")

    st.write(f"Solicitado por {resp['Solicitou']} sobre o projeto {resp['Projeto']}.")
    st.write(f"O pedido foi feito {resp['Data_Hora']}.")

    if resp['Status']=='finished':
        st.success("Status : "+str(mapper_respostas.get(resp['Status'])))
        st.success("OBS : "+str(resp['OBS']))
    elif resp['Status']=='error':
        st.warning("Status : "+str(mapper_respostas.get(resp['Status'])))
        st.warning("OBS : "+str(resp['OBS']))
    else:
        st.info("Status : "+str(mapper_respostas.get(resp['Status'])))

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