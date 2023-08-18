class PrevisorAtivo:
    """Cria a classe Previsor de ativos e define os parâmetros de ticket e o período análisado"""
    def __init__(self, ticket_do_ativo='ITSA4', periodo_de_analise='9'):
        self.ticket_do_ativo = ticket_do_ativo
        self.periodo_de_analise = periodo_de_analise

    def buscar_arquivo_ibov(self):
        site_bovespa = 'https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-ibovespa-ibovespa-composicao-da-carteira.htm'
        botao_dowload = '/html/body/app-root/app-day-portfolio/div/div/div[1]/form/div[2]/div/div[2]/div/div/div[1]/div[2]/p/a'
        pass

    def tratar_arquivo_ibov(self):
        pass


    def baixar_dados(self):
        """Baixa dados do Yahoo Finance de acordo com o código do ativo passado e o período"""
        import yfinance as yf
        yf.pdr_override()

        try:
            self.df = yf.Ticker(f'{self.ticket_do_ativo}.SA').history(f'{self.periodo_de_analise}y')
        except:
            return 'Ocorreu algum erro na busca dos dados'

        return self.df

    def indicador_cruzamento_de_medias_moveis(self):
        """Baixa os dados e Cria as médias móveis de 5, 15 e 25 aritimética, aritimética e exponencial respectivamente"""
        self.baixar_dados()
        self.df['mm5'] = self.df['Close'].rolling(window=5).mean()
        self.df['mm15'] = self.df['Close'].rolling(window=15).mean()
        self.df['mme25'] = self.df['Close'].ewm(span=25).mean()

        return self.df

    def indicador_MACD(self):
        """Baixa os dados e cria o indicador MACD e plota no gráfico"""
        self.baixar_dados()
        lenta = self.df['Close'].ewm(span=12).mean()
        rapida = self.df['Close'].ewm(span=26).mean()
        self.df['MACD'] = lenta - rapida
        self.df['Sinal'] = self.df['MACD'].ewm(span=9).mean()

        return self.df

    def indicador_bandas_de_bollinger(self):
        """Baixa os dados e cria o indicador Bandas de Bollinger"""
        self.baixar_dados()
        df = self.df[['Close']]

        self.media = df.rolling(window=20).mean()
        desvio = df.rolling(window=20).std()

        banda_superior = self.media + 2 * desvio
        banda_inferior = self.media - 2 * desvio
        banda_inferior = banda_inferior.rename(columns={'Close': 'inferior'})
        banda_superior = banda_superior.rename(columns={'Close': 'superior'})


        self.df_band = df.join(banda_superior).join(banda_inferior)
        self.ponto_compra = self.df_band[self.df_band['Close'] <= self.df_band['inferior']]
        self.ponto_venda = self.df_band[self.df_band['Close'] >= self.df_band['superior']]



        return self.df_band

    def rodar_regressao(self):
        """Trata os dados e roda a regressão linear"""
        import pandas as pd
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from sklearn.linear_model import LinearRegression
        from sklearn.metrics import r2_score

        self.baixar_dados()
        # tratamento dos dados e criação de média
        self.df['mm9'] = self.df['Close'].rolling(window=9).mean()
        self.df['mm21'] = self.df['Close'].rolling(window=21).mean()
        self.df['Close'] = self.df['Close'].shift(-1)
        self.df.reset_index(inplace=True)
        self.ultimo_dado = self.df.iloc[-1:]
        self.df.dropna(inplace=True)

        # tamanho dos dados
        total = len(self.df)
        treino = len(self.df) - 700
        teste = len(self.df) - 15

        # definindo features e labels
        x_features = self.df.drop(['Date', 'Close', 'Volume', 'Dividends', 'Stock Splits'], axis=1)
        self.x_features_list = list(x_features.columns)

        y_label = self.df['Close']

        # separando x e y de treino e teste
        x_train, x_test = x_features[:treino], x_features[treino:teste]
        y_train, y_test = y_label[:treino], y_label[treino:teste]

        # Rodar a regressão

        self.lr = LinearRegression()
        self.lr.fit(x_train, y_train)
        y_predito = self.lr.predict(x_test)
        coef = r2_score(y_test, y_predito)
        self.mensagem = f'O Coeficiente é de {coef * 100:.2f}% de expliação dos dados'

        # dados de validação:
        prever = x_features[teste:total]
        data = self.df['Date'][teste:total]
        fechamento = self.df['Close'][teste:total]

        y_previsto = self.lr.predict(prever)

        self.dados = pd.DataFrame({'Data': data, 'Fechamento': fechamento, 'Previsto': y_previsto})
        self.dados['Fechamento'] = self.dados['Fechamento'].shift(+1)
        self.dados['Erro'] = self.dados['Previsto'] - self.dados['Fechamento']
        self.dados = self.dados.round(2).dropna()

        fig, ax = plt.subplots(figsize=(16, 8))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.xaxis.set_tick_params(rotation=30)

        ax.set_title(f'\nDesempenho do modelo com o ativo {self.ticket_do_ativo} nos ultimos 15 pregões.\n', fontsize=24)
        ax.set_xlabel(f'\nPeríodo de {self.periodo_de_analise} anos. {self.mensagem}\nGRÁFICO FIGURA B', fontsize=16)
        ax.set_ylabel(f'Variação do preço do ativo', fontsize=16)
        ax.plot(self.dados['Data'], self.dados['Fechamento'], color='blue', label='Cotação Real', marker='o')
        ax.plot(self.dados['Data'], self.dados['Previsto'], color='red', label='Cotação Prevista', marker='o')

        plt.legend()
        plt.grid()

        return None

    def prever_preco_de_amanha(self):
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        """Preve o preço do dia posterior (Se os dados do Yahoo Finace estiverem válidos)"""
        self.rodar_regressao()

        data = self.ultimo_dado['Date']
        prever = self.ultimo_dado.drop(['Date', 'Close', 'Volume', 'Dividends', 'Stock Splits'], axis=1)

        y_amanha = self.lr.predict(prever)

        fig, ax = plt.subplots(figsize=(16, 8))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.xaxis.set_tick_params(rotation=30)
        ax.set_title(f'\nDesempenho do modelo de {self.ticket_do_ativo} nos ultimos 15 pregões e Previsão.\nPrevisão para o próximo fechamento: R$ {str(y_amanha.round(2)).replace("[", "").replace("]", "").replace(".", ",")}',
                     fontsize=24)
        ax.set_xlabel(f'\nPeríodo de {self.periodo_de_analise} anos. {self.mensagem}\nGRÁFICO FIGURA C', fontsize=16)
        ax.set_ylabel(f'Variação do preço do ativo', fontsize=16)
        ax.plot(self.dados['Data'], self.dados['Fechamento'], color='blue', label='Cotação Real', marker='o')
        ax.plot(self.dados['Data'], self.dados['Previsto'], color='red', label='Cotação Prevista', marker='o')

        ax.plot(data, y_amanha,
                color='green',
                label=f'Previsão para amanhã: R$ {str(y_amanha.round(2)).replace("[", "").replace("]", "").replace(".", ",")}',
                marker='X')

        plt.legend()
        plt.grid()
        plt.show()

    def plotar_grafico(self, indicador='cruzamento_medias'):
        """Cria um gráfico interativo com o Plotly  a partir da seleção do indicador"""
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        plt.rcdefaults()

        if indicador == 'cruzamento_medias':
            self.indicador_cruzamento_de_medias_moveis()
            fig, ax = plt.subplots(figsize=(16,8))

            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=180))
            ax.xaxis.set_tick_params(rotation=30)
            ax.set_title(f'\nAnálise do ativo {self.ticket_do_ativo} com base em cotações diárias filtrada por {self.periodo_de_analise} anos\n', fontsize=24)
            ax.set_xlabel('Período de anos analisado', fontsize=16)
            ax.set_xlabel(f'Período de {self.periodo_de_analise} anos analisado\nGRÁFICO FIGURA A', fontsize=16)
            ax.plot(self.df.index, self.df['Close'], label='Fechamento',)
            ax.plot(self.df.index, self.df['mm5'], label='Média Móvel Aritimética de 5 períodos',)
            ax.plot(self.df.index, self.df['mm15'], label='Média Móvel Aritimética de 15 períodos',)
            ax.plot(self.df.index, self.df['mme25'], label='Média Móvel Exponencial de 25 períodos',)
            plt.grid(); plt.legend()

        if indicador == 'bandas_bollinger':
            self.indicador_bandas_de_bollinger()
            fig, ax = plt.subplots(figsize=(16, 8))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=180))
            ax.xaxis.set_tick_params(rotation=30)
            ax.set_title(f'\nAnálise do ativo {self.ticket_do_ativo} com base em cotações diárias filtrada por {self.periodo_de_analise} anos\n', fontsize=24)
            ax.set_xlabel(f'Período de {self.periodo_de_analise} anos analisado\nGRÁFICO FIGURA A', fontsize=16)
            ax.set_ylabel('Variação de preço do ativo em Reais (R$)', fontsize=16)
            ax.plot(self.df_band.index, self.df_band['Close'], label='Preço de Fechamento', color='black')
            ax.plot(self.df_band.index, self.df_band['superior'], label='Bandas', color='green')
            ax.plot(self.df_band.index, self.df_band['inferior'], color='green')
            ax.plot(self.media.index, self.media['Close'], color='purple', label='Média Móvel')
            ax.scatter(self.ponto_compra.index, self.ponto_compra['Close'], color='blue', label='Ponto de Compra')
            ax.scatter(self.ponto_venda.index, self.ponto_venda['Close'], color='red', label='Ponto de Venda')


            plt.legend();plt.grid()



        if indicador == 'macd':
            self.indicador_MACD()
            import matplotlib.gridspec as gridspec

            fig = plt.figure(tight_layout=False, figsize=(16, 10))
            gs = gridspec.GridSpec(2, 1)


            ax = fig.add_subplot(gs[0,:])
            ax.set_title(f'\nAnálise do ativo {self.ticket_do_ativo} com base em cotações diárias filtrada por {self.periodo_de_analise} anos\n', fontsize=24)
            #ax.set_xlabel('Período de anos analisado', fontsize=16)

            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=180))
            ax.xaxis.set_tick_params(rotation=30)
            ax.grid(); ax.legend()
            ax.plot(self.df.index, self.df['Close'], label='Fechamento', color='blue')


            ax = fig.add_subplot(gs[1, :])

            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=180))
            ax.xaxis.set_tick_params(rotation=30)
            ax.set_ylabel('Variação MACD X Sinal', fontsize=16)

            ax.plot(self.df.index, self.df['MACD'], label='MACD', color='black')
            ax.plot(self.df.index, self.df['Sinal'], label='Sinal', color='red')
            ax.set_xlabel(f'Período de {self.periodo_de_analise} anos analisado\nGRÁFICO FIGURA A', fontsize=16)
            plt.tight_layout()
            plt.legend()
