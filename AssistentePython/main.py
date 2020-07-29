from chatbot import Bot
from arduino import Arduino
from reconhecimento import Reconhecimento


assistente = Bot()
assistente.listar_vozes()

assistente.falar('Iniciando Assistente')

arduino = Arduino('/dev/ttyUSB0', 9600)
arduino.verificar_porta()

comando_voz = Reconhecimento()

while True:
    comando_voz.meu_comando()
    #arduino.enviar_msg(comando_voz.meu_comando())
    arduino.enviar_wifi(comando_voz.meu_comando())
    assistente.falar(arduino.ler_serial())




