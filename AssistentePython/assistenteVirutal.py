# -*- coding: utf-8 -*-
import serial  # pip install pyserial
import threading
import time
import pyttsx3  # pip install pyttsx3
from vosk import Model, KaldiRecognizer
import pyaudio
import re

# chatbot
from chatterbot.trainers import ListTrainer

from chatterbot import ChatBot

AMGbot = ChatBot("Assistente")

# texto inicial, com o trino o bot vai ficando mais inteligente
conversa1 = ['oi', 'olá', 'olá bom dia', 'bom dia', 'como vai?', 'estou bem']
conversa2 = ['tente ', 'tente de novo', 'nao desista','fale novamente']

treinar = ListTrainer(AMGbot)
treinar.train(conversa1)
treinar.train(conversa2)


engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('rate', 150)  # velocidade 120 = lento
contar = 0;
for vozes in voices:  # listar vozes
    print(contar, vozes.name)
    contar += 1

voz = 53
engine.setProperty('voice', voices[voz].id)


conectado = False
porta = '/dev/ttyUSB0'
velocidadeBaud = 9600

mensagensRecebidas = 1;
desligarArduinoThread = False

falarTexto = False;
textoRecebido = ""
textoFalado = ""

arduinoFuncionando = True

try:
    SerialArduino = serial.Serial(porta, velocidadeBaud, timeout=0.2)
except:
    print("Verificar porta serial ou religar arduino")
    arduinoFuncionando = False


def handle_data(data):
    global mensagensRecebidas, engine, falarTexto, textoRecebido
    print("Recebi " + str(mensagensRecebidas) + ": " + data)

    mensagensRecebidas += 1
    textoRecebido = data
    falarTexto = True


def read_from_port(ser):
    global conectado, desligarArduinoThread

    while not conectado:
        conectado = True

        while True:
            reading = ser.readline().decode()
            if reading != "":
                handle_data(reading)
            if desligarArduinoThread:
                print("Desligando Arduino")
                break


if arduinoFuncionando:
    try:
        lerSerialThread = threading.Thread(target=read_from_port, args=(SerialArduino,))
        lerSerialThread.start()
    except:
        print("Verificar porta serial")
        arduinoFuncionando = False
    print("Preparando Arduino")
    time.sleep(2)
    print("Arduino Pronto")
else:
    time.sleep(2)
    print("Arduino não conectou")

while True:
    if falarTexto:
        if textoRecebido != "":
            engine.say(textoRecebido)
            engine.runAndWait()
            textoRecebido = ""
        elif textoFalado != "":
            resposta = AMGbot.get_response(textoFalado)
            engine.say(resposta)
            engine.runAndWait()
            textoFalado = ""

        falarTexto = False


    def meu_comando():  #função que retorna o que foi falado em forma de string
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        stream.start_stream()

        model = Model("vosk-model-small-pt-0.3")    #localiza o arquivo de reconhecimento de voz
        rec = KaldiRecognizer(model, 16000)
        print("Fale algo")

        while True:

            data = stream.read(2000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                meuResultado = rec.Result()
                minhaLista = meuResultado.split("text") #o que foi falado na posição text é retornado em lista
                comando = minhaLista[1] #
                stream.stop_stream()
                stream.close()
                p.terminate()
                resultado = re.findall(r'\w+', comando) #expressão regular parar pegar todas as letras
                resultadofinal = " ".join(resultado) #transforma a lista em string limpa
                return resultadofinal
    try:
        try:
            texto = meu_comando()

            if arduinoFuncionando:  #se o arduino estiver concetado a comunicação serial se inicia
                SerialArduino.write(str.encode(texto+'\n')) #manda o que foi dito em forma
                # de string para o serial do arduino
                print(texto)

            if texto != "":
                textoFalado = texto
                falarTexto = True

            print("Dado enviado")
            if (texto == "desativar"):
                print("Saindo")

                desativando = "Assistente desativando"

                engine.say(desativando)
                engine.runAndWait()
                engine.stop()
                desligarArduinoThread = True
                if arduinoFuncionando:
                    SerialArduino.close()
                    lerSerialThread.join()
                break

        except:
            print("Não entendi o que você disse\n")
            engine.say("que você disse?")
            engine.runAndWait()

        time.sleep(0.5)  # aguarda resposta do arduino
    except (KeyboardInterrupt, SystemExit):
        print("Apertou Ctrl+C")
        engine.stop()
        desligarArduinoThread = True
        if arduinoFuncionando:
            SerialArduino.close()
            lerSerialThread.join()
        break