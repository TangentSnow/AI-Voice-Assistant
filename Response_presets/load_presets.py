import os
import random

class ResponsePresets():
    def __init__(self):
        self.intro_files = [os.path.join('/Users/adityamakineni/Desktop/Personal ML/AI Voice Assistant/Response_presets/introduction', f) 
                            for f in os.listdir('/Users/adityamakineni/Desktop/Personal ML/AI Voice Assistant/Response_presets/introduction')]
        self.greeting_files = [os.path.join('/Users/adityamakineni/Desktop/Personal ML/AI Voice Assistant/Response_presets/greetings', f)
                               for f in os.listdir('/Users/adityamakineni/Desktop/Personal ML/AI Voice Assistant/Response_presets/greetings')]
        self.not_understand_files = [os.path.join('/Users/adityamakineni/Desktop/Personal ML/AI Voice Assistant/Response_presets/Didnt_Understand', f)
                              for f in os.listdir('/Users/adityamakineni/Desktop/Personal ML/AI Voice Assistant/Response_presets/Didnt_Understand')]
        self.goodbye_files = [os.path.join('/Users/adityamakineni/Desktop/Personal ML/AI Voice Assistant/Response_presets/goodbye', f)
                        for f in os.listdir('/Users/adityamakineni/Desktop/Personal ML/AI Voice Assistant/Response_presets/goodbye')]
        
    def intro(self):
        return random.choice(self.intro_files)
    
    def greetings(self):
        return random.choice(self.greeting_files)
    
    def not_understand(self):
        return random.choice(self.not_understand_files)
    
    def goodbye(self):
        return random.choice(self.goodbye_files)