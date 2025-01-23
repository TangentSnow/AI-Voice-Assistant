import speech_recognition as sr
import webbrowser
import requests
import json
from playsound import playsound
import threading
import joblib
from piper.voice import PiperVoice
import random
import os
import wave
from queue import Queue

wake_word_event = threading.Event()
command_queue = Queue()

recognizer = sr.Recognizer()

model = 'TTS_models/en_US-hfc_female-medium.onnx'
voice = PiperVoice.load(model)

intro_wav_files = [os.path.join('Response_presets/introduction', f)
                   for f in os.listdir('Response_presets/introduction')]

error_wav_files = [os.path.join('Response/Didnt_Understand', f)
                   for f in os.listdir('Response_presets/Didnt_Understand')]

llm_url = "http://localhost:11434/api/chat"
headers = {'Content-Type': 'application/json'}

# text classification model (naive bayes)
text_classifier = joblib.load('TextClassification/naive_bayes_txt_class_pipeline.pkl')

# command_map = {
#     'greetings': handle_greetings,
# }

# Continuously listen for wakee work in the background
def listen_for_keyword(wake_word=["hey laura", "hello laura"]):
    with sr.Microphone() as source:
        # print("wake word...")
        recognizer.adjust_for_ambient_noise(source)
        while True:
            # if wake_word_event.is_set():
            #     time.sleep(1)   # skip listening if the wake word is already detected
            #     continue
        
            try:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5) #Listen for up to 10 seconds
                command = recognizer.recognize_google(audio).lower()
                # print(f"heard: {command}")
                if any(word in command for word in wake_word):
                    command_queue.put("wake_word_detected")
                    # text_to_speech("yeeesss?")
                    wav_path = random.choice(intro_wav_files)
                    playsound(wav_path)
            except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
                pass

# Function to grab commands from the user
def listen_for_command():
    # Open the microphone for listening
    with sr.Microphone() as source:
        print('Listening for commands...')
                
        recognizer.adjust_for_ambient_noise(source) # adjust recognizer sensitivity to ambient noise   
        audio = recognizer.listen(source) # Listens for the first phrase and extracts the audio
                
    try:
        # Recognizes speech with Google's speech recognition
        command = recognizer.recognize_google(audio)
        # print(f"I think you said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        wav_path = random.choice(error_wav_files)
        playsound(wav_path)
        return None
    except sr.RequestError as e:
        text_to_speech("Could not request results")
        return None
    
# listen_for_command()

# This function converts text to speech
def text_to_speech(response_text):
    # print(response_text)
    wav_file = wave.open("va_audio.wav", 'w')
    voice.synthesize(response_text, wav_file)
    playsound('va_audio.wav')
    
# This function sends a prompt to local-ollama model and return a response
def chatGPT_response(prompt):
    payload = {
        "model": "hf.co/bartowski/granite-3.1-2b-instruct-GGUF:Q6_K",
        "messages": [
            {"role": "system", "content": "Act as a friendly and concise conversational assistant. Answer questions clearly, stay conversational, and keep responses short unless more detail is requested."},
            {"role": "user", "content": prompt}
        ]
    }

    # Make the API request
    response = requests.post(llm_url, json=payload, headers=headers, stream=True)

    if response.status_code == 200:
        response_parts = response.text.split('\n')
        content = ""
        for part in response_parts:
            part = part.strip()
            if not part:
                continue
            try:
                response_dict = json.loads(part)
                message = response_dict.get('message', {})
                content += message.get('content', '')
            except json.JSONDecodeError as e:
                print(e)
        return content.strip()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        
def command_classifier(command):
    prediction = text_classifier.predict([command])
    return prediction[0]


def main():
    gpt_commands = ["who", "what", "when", "where", "how", "should", 
                        "why", "will", "would", "could", "do", "does", 
                        "is", "are", "am", "was", "were", "have", "has", "had", "which"]
    exit_commands = ["goodbye", "bye", "exit", "stop"]
    
    wake_thread = threading.Thread(target=listen_for_keyword, daemon=True)
    wake_thread.start()
    
    while True:
        if not command_queue.empty():
            event = command_queue.get()
            
            if event == "wake_word_detected":
                command = listen_for_command() # Listen for command
                command_class = command_classifier(command)
            
                if command:
                    if any(word in command for word in gpt_commands):
                        response = chatGPT_response(command)    # get response from GPT-3
                        text_to_speech(response)    # play response
                        
                    # open chrome if user says open chrome
                    elif "open chrome" in command or "open google" in command:
                        text_to_speech("Okay opening now.")
                        webbrowser.open('http://google.com')    # Open chrome and goes to google.com
                        
                    elif any(word in command for word in exit_commands):
                        text_to_speech("Goodbye.")
                        
                        break
                    else:
                        text_to_speech("Sorry, I didn't get that")
                    
                wake_word_event.clear()

            # time.sleep(0.5)
        
if __name__ == '__main__':
    main()