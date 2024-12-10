def explicacoes_estatisticas(ativo, periodo):
    return f"""
    Uma breve explicação sobre os estudos estatísticos:
    \nNo primeiro gráfico temos a cotação de {ativo} pelo período de {periodo} ano(s).
    \n No segundo tempo a variação percentual do preço pelo período sendo o ideal é comprar quando
     o preço estiver próximo a linha azul e evitar de comprar próximo a linha vermelha, onde devemos estar 
    desfazendo das nossas posições.
    \nO terceiro gráfico é um boxplot do comportamento das variações que é auto explicativo.
    
    *** RESUMINDO: VAMOS COMPRAR COM ALTA PROBABILIDADE DE ACERTO PRÓXIMO A LINHA AZUL ****
    """


def explicacoes_ponto_compra():
    return f"""
    Uma breve explicação sobre os pontos de compra:
    \nSe o papel for aprovado na nossa análise:
    \nVamos comprar próximo a setinha marcada e segurar o papel fazendo vendas parciais

    *** RESUMINDO: COMPRAR COM ALTA PROBABILIDADE DE ACERTO NA SETINHA PRETA ****
    """

def explicacoes_bandas_bollinger():
    return f"""
    Uma breve explicação sobre Bandas de Bollinger:
    \nUm dos indicadores mais usados por muitos especialistas são as bandas de bollinger que, basicamente,
    faz um canal onde o preço trabalha em 2 vezes os desvio da média aritimética de 20 períodos.
    \nVamos comprar próximo ao toque numa banda inferior e vender próximo a banda superior, mas é interessante
    estar acompanhando os vídeos que vou postar para poder entender o processo...

    *** RESUMINDO: COMPRAR COM ALTA PROBABILIDADE DE ACERTO NA PRÓXIMO A BANDA INFERIOR ****
    """