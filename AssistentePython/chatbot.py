import pyttsx3

class Bot:

    def listar_vozes(self):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('rate', 120)  # velocidade 120 = lento
        contar = 0;
        for vozes in voices:  # listar vozes
            print(contar, vozes.name)
            contar += 1

    def falar(self, msg_recebida):
        self.msg_recebida = msg_recebida
        texto = self.msg_recebida
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[53].id)
        engine.setProperty('rate', 150)
        engine.say(texto)
        engine.runAndWait()
        return
