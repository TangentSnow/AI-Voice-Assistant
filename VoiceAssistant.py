import speech_recognition as sr
from playsound import playsound
from TextClassification.nn_text_class import TextClassifier
from tts.piper_tts import PiperTTS
from services.services import services
from languageModel.lm_service import LMService
from Response_presets.load_presets import ResponsePresets

class VoiceAssistant():
    def __init__(self):
        self.tts = PiperTTS()
        self.services = services()
        self.lm_service = LMService()
        self.response_presets = ResponsePresets()
        self.text_classifier = TextClassifier()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.commad_map = {
            'greetings': self.response_presets.greetings,
            'goodbye': lambda: playsound(self.response_presets.goodbye()),
            'weather': lambda: self.tts.text_to_speech(self.services.handle_weather()),
        }
        
    # def calibrate_microphone(self):
    #     with self.microphone as source:
    #         self.recognizer.adjust_for_ambient_noise(source)
        
    def listen_for_keyword(self, source, wake_word=["hey laura", "hello laura"]):
        while True:
            try:
                print("Wake Word...")
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=5)
                command = self.recognizer.recognize_google(audio).lower()
                print(f"Heard: {command}")
                if any(word in command for word in wake_word):
                    # self.command_queue.put("wake_word_detected")
                    playsound(self.response_presets.intro())    # Play an intro from the intro presets
                    return True
            except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
                pass
                
    def listen_for_command(self, source):
        print("Listening for commands...")

        try:
            audio = self.recognizer.listen(source)
            command = self.recognizer.recognize_google(audio).lower()
            print(f"Heard: {command}")
            return command
        except sr.UnknownValueError:
            playsound(self.response_presets.not_understand())
            return None
        except sr.RequestError as e:
            self.tts.text_to_speech("Could not request results")
            return None
        
    
    def run(self):
        with self.microphone as source:
        # self.calibrate_microphone()
        
            while True:
                if self.listen_for_keyword(source):
                    command = self.listen_for_command(source)
                        
                    if command:
                        classify_command = self.text_classifier.predict(command)
                        command_function = self.commad_map.get(classify_command)
                            
                        if command_function:
                            command_function()
                        else:
                            self.tts.text_to_speech(self.lm_service.lm_response(command))
                                
assistant = VoiceAssistant()
assistant.run()