# import joblib

# text_classifier = joblib.load('TextClassification/naive_bayes_txt_class_pipeline.pkl')

# text = "how hot is it right now?"

# preds = text_classifier.predict([text])

# print(preds[0])

from piper.voice import PiperVoice
import wave
from playsound import playsound

model = 'TTS_models/en_US-hfc_female-medium.onnx'
voice = PiperVoice.load(model)
text = "Bye. Take care!"
wav_file = wave.open("test.wav", 'w')
audio = voice.synthesize(text, wav_file)
playsound('test.wav')

# import joblib
# from TextClassification.nn_text_class import TextClassificationModel
# import torch

# vectorizer = joblib.load('TextClassification/models/tfidf_vectorizer.pkl')
# label_encoder = joblib.load('TextClassification/models/label_encoder.pkl')
# model = TextClassificationModel(input_dim=3809, output_dim=81)
# model.load_state_dict(torch.load('TextClassification/models/nn_text_class.pth', weights_only=True))
# model.eval()

# new_text = "How hot is it outside"
# new_vec = vectorizer.transform([new_text])
# input = torch.tensor(new_vec.toarray(), dtype=torch.float32)

# with torch.no_grad():
#     outputs = model(input)
#     preds = torch.argmax(outputs, dim=1)
    
    
# decod_pred = label_encoder.inverse_transform(preds.numpy())
# print(decod_pred)

# from TextClassification.nn_text_class import TextClassifier

# new_text = "How hot is it outside?"

# classifier = TextClassifier()

# cla = classifier.predict(new_text)

# print(cla[0])

# import geocoder
# from dotenv import load_dotenv
# import os
# import requests
# import json

# load_dotenv()

# WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# def get_current_lat_lang():
#     g = geocoder.ip('me')
#     return g.latlng

# location = get_current_lat_lang()

# weather_url = f'http://api.weatherapi.com/v1/current.json'
# # headers = {'Content-Type': 'application/json'}

# payload = {
#     "key": WEATHER_API_KEY,
#     "q": location
    
# }

# response = requests.post(weather_url, payload)

# data = json.loads(response.text)

# location = data['location']['name']
# temp_f = data['current']['temp_f']
# condition = data['current']['condition']['text']
# feelslike_f = data['current']['feelslike_f']

# print(location)
# print(temp_f)
# print(condition)
# print(feelslike_f)

# import spacy

# nlp = spacy.load("en_core_web_sm")

# def extract_location(command):
#     doc = nlp(command)
#     for ent in doc.ents:
#         if ent.label_ == "GPE":
#             return ent.text
#     return None

# text = "Hey what's the weather?"

# print(extract_location(text))