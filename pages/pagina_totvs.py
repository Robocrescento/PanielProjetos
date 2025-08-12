import numpy as np
import streamlit as st
from datetime import datetime
import pandas as pd
import os
import json
import requests
from streamlit_autorefresh import st_autorefresh
path=fr'C:\Users\{os.getlogin()}\Crescento Consultoria Financeira\Hub dados - DadosBPO\Robos_v2\Codigos\ROBO_TOTVS\utils\Caminhos.xlsx'
url_base='https://sturgeon-boss-regularly.ngrok-free.app'

opções_totvs=pd.read_excel(path,sheet_name=1).columns.tolist()


if not 'df' in st.session_state.keys() :
    df=pd.DataFrame(columns=['relatorio','mes','ano','hora','codigo','status'])

ano_at=datetime.today().year
mes_at=datetime.today().month

escolhidos=st.multiselect("Selecionar Relatórios",opções_totvs,opções_totvs)
ano=st.selectbox('Ano',[2025,2024],0)
mes=st.selectbox('Mês',list(range(1,13)),mes_at)
#escolhidos=opções_totvs[:10]


def coloca_na_fila(relatorio,mes,ano):
    projeto = 'totvs'
    nome = 'Dani'
    args = {'relatorio': relatorio, 'mes': mes, 'ano': ano}
    jargs = json.dumps(args)
    fila = requests.get(url_base + f'/start-projeto?&nome={nome}&projeto={projeto}&argumentos={jargs}').json()
    uid=fila.get('uid')
    hora=datetime.now().strftime('%d/%m %H:%M')
    args['hora']=hora
    args['codigo']=uid
    args['status']='Nao está na fila'
    st.session_state['Hora_Pedido']=hora
    return args

if st.button('Fazer pedido'):
    dicts = []
    for e in escolhidos:
        dicts.append(coloca_na_fila(e,mes_at,ano_at))
    df = pd.DataFrame(dicts)

    st.session_state['df']=df

@st.cache_data
def checkout(df,state=None):
    for id, row in df.iterrows():
        status = row.status
        codigo = row.codigo
        if not status in ('finished'):
            status = requests.get(url_base + '/status/' + codigo).json().get('Status')
        df.loc[id, 'status'] = status
    st.session_state['df'] = df

    return df

if st.session_state.get('Hora_Pedido') is None:
    st.stop()
st.info(f"Mostrando encomenda de {st.session_state['Hora_Pedido']}.")

st_autorefresh(interval=20000, key="autorefresh")


state=np.random.random()
df=checkout(st.session_state['df'],state )
df