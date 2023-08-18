
def tela_analise():
    import streamlit as st
    from previsor import PrevisorAtivo
    import pandas as pd
    st.set_option('deprecation.showPyplotGlobalUse', False)

    st.header('Previsor de preços futuros de ativos')
    st.write('By João Marcos da Silva')

    # sidebar (barra ao lado esquerdo da tela)
    st.sidebar.success('OPÇÕES DE ANÁLISE')
    ativo = st.sidebar.text_input('Digite o código do ativo:', 'PETR4', help='Digite o código de ativo da B3, ex: PETR4')

    anos = st.sidebar.slider('Selecione a quantidade de anos:', 2, 15, 9, help='O valor recomendado é 9 anos, mas vc pode selecionar quanto quiser, porém não foi testados valores superiores ao padrão')


    # instancia do módulo previsor
    dados = PrevisorAtivo(ticket_do_ativo=ativo, periodo_de_analise=anos)

    # Análise e dindicadores
    st.sidebar.success('Marque para ver os dados:')

    # dataFrame
    btn_df = st.sidebar.checkbox('Plotar Data Frame', False, help='Marque para ver os dados temporais e desmarque para sumir')
    if btn_df:
        df = st.dataframe(dados.baixar_dados())

    # indicadores de preço e volume
    st.sidebar.success('Indicadores:')

    # check indicador
    check_indicador = st.sidebar.selectbox('Selecione o indicador para analisar:', ('Cruzamento de Médias Móveis', 'Bandas de Bollinger', 'MACD'),
                                            True, help='Selecione qual indicador quer que plote o gráfico com as análises')

    # cruzamento de médias
    if check_indicador == 'Cruzamento de Médias Móveis':
        st.pyplot(dados.plotar_grafico('cruzamento_medias'))
    # bandas de bollinger

    elif check_indicador == 'Bandas de Bollinger':
        st.pyplot(dados.plotar_grafico('bandas_bollinger'))

    # MACD
    elif check_indicador == 'MACD':
        st.pyplot(dados.plotar_grafico('macd'))

    st.sidebar.success('Previsor de Preço D+1:')

    # check previsor
    select_previsor = st.sidebar.selectbox('Selecione o algorítimo para prever o preço:', (
                                        'Regressão Linear', 'Selecione um algorítimo','Rede Neural', ),
                                            True, help='Selecione qual algorítimo será usado para prever o preço do ativo')


    if select_previsor == 'Selecione um algorítimo':
        st.success('Selecione um algorítimo para saber o preço futuro do ativo selecionado!')


    elif select_previsor == 'Regressão Linear':
        st.write('Prevendo com Regressão Linear...')
        st.warning('Por favor aguarde alguns segundos para o processamento...')
        st.pyplot(dados.rodar_regressao())
        st.subheader('Tabela com as previsões e erros:')
        st.dataframe(dados.dados)
        st.error("""
        Atenção!
        Essa base de dados é gratuida, Yahoo Finance, e frequentemente apresenta erros de dados de algumas variáveis faltantes geralmente
        do dia anterior, porém eles corrigem próximo a abertura do pregão, às 10:00 da manhã.
        Caso o gráfico abaixo, figura C, esteja muito diferente do de címa, figura B, tente novamente mais tarde.
        """)
        st.pyplot(dados.prever_preco_de_amanha())

    if select_previsor == 'Rede Neural':
        st.write('Prevendo com Rede Neural')
        st.warning('Atenção! Esse algorítimo pode demorar até, em média,  6 minutos devido às camadas de neurônios...')

def tela_secundaria():
    pass

def tela_cadastro():
    pass
tela_analise()


