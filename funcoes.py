import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.gridspec as grid
import streamlit as st

import explicacoes
from explicacoes import *

def baixar_ativos(ativo, periodo):
    """Baixa os ativos e retorna um df com o ativos selecionados por ativo e período (em anos)"""
    papel, periodo = f'{ativo.upper()}.SA', f'{periodo}y'
    papel = yf.Ticker(papel)
    df = papel.history(periodo)
    df = df.drop(['Dividends', 'Stock Splits'], axis=1)

    return df

def calcular_dados_estatisticos(ativo, periodo, grafico=True):
    """Calcula indicadores estatísticos para tomada de decisão e retorna ou não um gráfico"""
    df = baixar_ativos(ativo, periodo)
    df['close_change'] = df['Close'].pct_change()
    df = df.dropna()
    p25, p75 = df['close_change'].describe()[['25%', '75%']]
    pmin = max(min(df['close_change']), p25 - 1.5 * (p75 - p25))
    pmax = min(max(df['close_change']), p75 + 1.5 * (p75 - p25))

    if grafico:
        st.subheader(explicacoes.explicacoes_estatisticas(ativo, periodo))
        fig = plt.figure(figsize=(16, 8))
        gs = grid.GridSpec(2, 2)

        ax = fig.add_subplot(gs[0, :])
        ax.plot(df.index, df['Close'], label='Fechamento')
        ax.set_title(f'Cotação de {ativo.upper()} por {periodo} ano(s)', fontsize=24)
        ax.set_ylabel('Preço em R$', fontsize=16)

        ax = fig.add_subplot(gs[1, 0])
        ax.plot(df.index, df['close_change'], label='Variação %')
        ax.axhline(pmin, linestyle='--')
        ax.axhline(pmax, linestyle='--', color='red')
        ax.set_title(f'Variação de {ativo.upper()} por {periodo} ano(s)', fontsize=14)
        ax.set_ylabel('Variação %', fontsize=16)

        ax = fig.add_subplot(gs[1, 1])
        ax.boxplot(df['close_change'])
        ax.axhline(pmin, linestyle='--')
        ax.axhline(pmax, linestyle='--', color='red')
        ax.set_title(f'Variação de {ativo.upper()} por {periodo} ano(s)', fontsize=14)
        ax.set_ylabel('Variação %', fontsize=16)
        st.pyplot(fig)

    return df, pmin, pmax

def previsao_regressao_linear(acao, anos):
    pass

def plotar_pontos_de_compra(ativo, periodo, corte=1000, plotar_grafico=True):
    """Plota o gráfico com pontos de compra dos ultimos 1000 período"""
    df, pmin, pmax = calcular_dados_estatisticos(ativo, periodo, grafico=False)

    data = df[-corte:]
    gatilhos = data[data['close_change'] < pmin]

    if plotar_grafico:
        st.subheader(explicacoes_ponto_compra())
        fig, ax = plt.subplots(figsize=(16, 8))

        ax.plot(data['Close'])
        ax.set_title(f'Ponto de compra de {ativo.upper()} dos ultimos {corte} períodos', fontsize=24)
        ax.set_ylabel('Preço em R$', fontsize=18)

        for i, c in gatilhos.iterrows():
            ax.annotate('Compra', xy=(i, c.Close), xytext=(i, c.Close - 0.6),
                        arrowprops=dict(facecolor='black', shrink=0.05))

        st.pyplot(fig)

def bandas_bollinger(ativo, periodo):
    df = baixar_ativos(ativo, periodo)
    df = df[['Close']]

    mm = df.rolling(window=20).mean()
    std = df.rolling(window=20).std()

    superior = mm + 2 * std
    inferior = mm - 2 * std

    superior = superior.rename(columns={'Close': "Banda Superior"})
    inferior = inferior.rename(columns={'Close': "Banda Inferior"})
    mm = mm.rename(columns={'Close': 'Media'})

    df = df.join(mm).join(superior).join(inferior)
    gatilhos = df[df['Close'] < df['Banda Inferior']]

    st.subheader(explicacoes_bandas_bollinger())

    fig, ax = plt.subplots(figsize=(16, 8))

    ax.plot(df.index, df['Close'], color='k', label='Fechamento')
    ax.plot(df.index, df['Banda Superior'], color='green', label='Banda Superior')
    ax.plot(df.index, df['Banda Inferior'], color='green', label='Banda Inferior')
    ax.plot(df.index, df['Media'], color='orange', label='Média 20 P')
    ax.scatter(gatilhos.index, gatilhos['Banda Inferior'], color='purple')
    ax.set_title(f'Bandas de Bollinger de {ativo} pelo período de {periodo} ano(s).', fontsize=24)
    ax.set_ylabel('Preço em R$', fontsize=14)

    plt.legend()
    st.pyplot(fig)
