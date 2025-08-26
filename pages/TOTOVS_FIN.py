import numpy as np
import streamlit as st
from datetime import datetime
import pandas as pd
import os
import json
import requests
from streamlit_autorefresh import st_autorefresh
from time import sleep
path=fr'Caminhos.xlsx'
url_base='https://sturgeon-boss-regularly.ngrok-free.app'

opções_totvs=pd.read_excel(path,sheet_name=1).columns.tolist()
st.header("Relatório Financeiro")

st.header("Controle de pedidos do relatório TOTVS")


nome=st.text_input("Me diga seu nome")
if nome.strip() == '':
    st.stop()






if not 'df' in st.session_state.keys() :
    df=pd.DataFrame(columns=['relatorio','mes','ano','hora','codigo','status'])

ano_at=datetime.today().year
mes_at=datetime.today().month



tabs=st.tabs(['Fazer pedido','Ver pedidos'])
with tabs[0]:
    escolhidos = st.multiselect("Selecionar Relatórios", opções_totvs, opções_totvs)
    ano = st.selectbox('Ano', [2025, 2024], 0)
    meses = st.multiselect('Mês', list(range(1, 13)), [mes_at])


    # escolhidos=opções_totvs[:10]

    def coloca_na_fila(escolhidos,mes,ano):
        projeto = 'totvs_fin'

        args = [{"relatorio": e, "mes": mes, "ano": ano} for e in escolhidos]
        jargs = [json.dumps(e) for e in args]

        lista = {'lista': [{'nome': nome, 'projeto': projeto, 'argumentos': e} for e in jargs]}
        resposta = requests.post(url_base + '/batch-start-projeto', json=lista).json()
        hora = datetime.now().strftime('%d/%m %H:%M')

        uids = [e['uid'] for e in resposta]
        df = pd.DataFrame(args)
        df.loc[:, 'codigo'] = uids
        df.loc[:, 'status'] = 'Nao está na fila'
        df.loc[:, 'hora'] = hora
        st.session_state['Hora_Pedido'] = hora

        return df
    if st.button('Fazer pedido'):
        with st.status("Carregando"):
            for mes in meses:
                df=coloca_na_fila(escolhidos,mes,ano)
                sleep(3)
            st.session_state['df']=df


with tabs[1]:

    resposta_fila = requests.get(url_base + '/fila').json()
    resposta_fila = pd.read_json(resposta_fila,orient='split')
    if len(resposta_fila)==0:
        st.write("Nenhum projeto na fila")
        st.stop()

    resposta_fila=resposta_fila.loc[resposta_fila.Projeto.str.lower()=='totvs_fin']

    if len(resposta_fila)==0:
        st.write("Nenhum projeto na fila")
        st.stop()


    for g in ['relatorio','mes','ano']:
        resposta_fila.loc[:,g]=resposta_fila.ARGS.apply(lambda x:json.loads(x)[g])
    limite=max(pd.to_datetime(resposta_fila['Data_Hora']).dt.date.unique())
    data=st.date_input("Filtro de dia",value=limite)

    filtro_=resposta_fila['Data_Hora'].str.slice(stop=10)==str(data)


    resposta_fila=resposta_fila[filtro_]

    resposta_fila['Data_Hora']=pd.to_datetime(resposta_fila['Data_Hora'])
    resposta_fila['Hora']=resposta_fila.Data_Hora.dt.strftime('%H:%m')
    resposta_fila=resposta_fila[['Solicitou','Hora','relatorio','mes','ano','Status']].rename(columns={'Solicitou':'Quem'})

    resposta_fila.Status=resposta_fila.Status.replace('finished','Finalizado').replace('ongoing','Processando').replace('pending','Na Fila')
    resposta_fila.columns=resposta_fila.columns.str.title()

    st_autorefresh(interval=60000, key="autorefresh")

    st.dataframe(resposta_fila,hide_index=True)
