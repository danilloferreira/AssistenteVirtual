import socket
from chatbot import Bot
from reconhecimento import Reconhecimento

assistente = Bot()
assistente.listar_vozes()
assistente.falar('Iniciando Assistente')
comando_voz = Reconhecimento()

def enviar_wifi(texto):
    mensagem = (texto).encode()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('192.168.2.106', 555)
    sock.connect(server_address)
    sock.sendall(mensagem)
    sock.close()
    print("ENVIANDO ", mensagem)

while True:
    comando_voz.meu_comando()
    enviar_wifi(comando_voz.meu_comando())


