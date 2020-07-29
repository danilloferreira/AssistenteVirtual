import serial
import threading
import socket
class Arduino:

    def __init__(self, porta, velocidade, arduino_funcionando=True):
        self.porta = porta
        self.velocidade = velocidade
        self.arduino_funcionando = arduino_funcionando



    def verificar_porta(self):
        try:
            SerialArduino = serial.Serial(self.porta, self.velocidade, timeout=0.2)
            return SerialArduino

        except:
            print("Verificar porta serial ou reiniar o arduino")
            self.arduino_funcionando = False

    #enviar mensagem por Serial.
    def enviar_msg(self, texto):
        SerialArduino = self.verificar_porta()
        SerialArduino.write(str.encode(texto + '\n'))
        print(texto)

    #Realiza a leitura do Serial
    def ler_serial(self):
        SerialArduino = self.verificar_porta()
        lerSerial= SerialArduino.read()
        print('vc disse', lerSerial)
        return

    def enviar_wifi(self, texto):
        mensagem = (texto).encode()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('192.168.4.1', 1234)
        sock.connect(server_address)
        sock.sendall(mensagem)
        sock.close()
        print("ENVIANDO NORMALMENTE WIFI")



