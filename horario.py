import datetime
import time

def verificador_de_hora():
    while True:
        contador = 0
        # Obtém o horário atual
        now = datetime.datetime.now()
        # Verifica se a hora e minuto são 16:00
        if now.hour == 16 and now.minute == 0 and contador <= 0:
            print("Já são 16:00! Enviando a mensagem...")
            contador += 1
            # Para evitar enviar a mensagem repetidamente no minuto 16:00
            time.sleep(60)  # Aguardar 1 minuto para que não envie várias vezes

        # Espera 30 segundos antes de verificar novamente o horário
        time.sleep(30)

verificador_de_hora()
