
def envia_email():
    """Funçãoi que envia uma mensagem todo dia"""
    from datetime import datetime
    from time import sleep

    ultimo_dia = None
    while True:
        hoje = datetime.today()
        if hoje != ultimo_dia:
            print('Sua mensagem diária')
            ultimo_dia = hoje
        sleep(86400)

envia_email()
