from lista_ativos import lista_ativo
from funcoes import *
import streamlit as st
from time import sleep


#st.set_option('deprecation.showPyplotGlobalUse', False)

lista_de_acoes = lista_ativo()


################## página principal #####################################
st.title(f"Ganhe R$ com estatística com :blue[IBOV] ")
st.markdown("By J.Brutus :sunglasses:")

########################## Sidebar ######################################
st.sidebar.subheader('Selecione o ativo para análise:')
acao = st.sidebar.selectbox(f'Selecione uma ação da lista das {len(lista_de_acoes)} do IBOV:', (lista_de_acoes),
                            help="Foi buscada no site da B3 as ações atuais que compões o índice...")
anos = st.sidebar.slider("Tempo de análise em ano(s):", 0, 10, 5)

with st.spinner('Aguarde carregando...'):
    sleep(3)
########################################################################################################################
st.sidebar.success('Exibir estudo! :wave:')
estudo = st.sidebar.checkbox("Estudo Estatístico", value=True)
if estudo:
    st.success('Role a página até o final para ver o estudo!')
    calcular_dados_estatisticos(acao, anos)

pontos_compra = st.sidebar.checkbox("Pontos de Compra", value=False)
if pontos_compra:
    st.success('Role a página até o final para ver o estudo!')
    plotar_pontos_de_compra(acao, anos)

b_bollinger = st.sidebar.checkbox("Bandas Bollinger", value=False)
if b_bollinger:
    st.success('Role a página até o final para ver uma breve explicação sobre as bandas de bollinger!')
    bandas_bollinger(acao, anos)

ifr = st.sidebar.checkbox("Índice de Força Relativa (IFR)", value=False)
if ifr:
    st.success('Role a página até o final para ver uma breve explicação sobre IFR!')
    pass
####################################################################################################
st.sidebar.success('Área de previsões de preços :heart:')

reg_lin = st.sidebar.checkbox('Previsão com Regressão Linear')
if reg_lin:
    st.sidebar.info('Recomendo pelo menos 5 anos de análise')
    previsao_regressao_linear(acao, anos)
    st.error('Atenção: Se tiver muito divergente a previsão, significa que é erro na base de dados do Yfinance. '
             'Não atualizaram ainda e geralmente corrigem próximo ao iníncio do pregão!')

rn = st.sidebar.checkbox('Previsão com Redes Neurais')
if rn:
    st.sidebar.error('Aguenta só mais um pouquinho, Calabrezo, já faço o deploy')
#pprint