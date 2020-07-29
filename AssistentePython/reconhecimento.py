from vosk import Model, KaldiRecognizer
import pyaudio
import re

class Reconhecimento:

    @staticmethod
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