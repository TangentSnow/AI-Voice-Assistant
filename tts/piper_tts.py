from piper.voice import PiperVoice
import wave
from playsound import playsound

class PiperTTS():
    def __init__(self):
        self.model = '/Users/adityamakineni/Desktop/Personal ML/AI Voice Assistant/tts/models/en_US-hfc_female-medium.onnx'
        self.voice = PiperVoice.load(self.model)
        
    def text_to_speech(self, text):
        # print(response_text)
        wav_file = wave.open("va_audio.wav", 'w')
        self.voice.synthesize(text, wav_file)
        playsound('va_audio.wav')