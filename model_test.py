# import requests
# import json

# url = "http://localhost:11434/api/chat"

# payload = {
#     "model": "hf.co/bartowski/granite-3.1-2b-instruct-GGUF:Q6_K",
#     "messages": [
#         {"role": "system", "content": "You are a helpful assistant. Be concise"},
#         {"role": "user", "content": "What is the capital of India?"}
#     ]
# }

# # Make the API request
# response = requests.post(url, json=payload, stream=True)

# if response.status_code == 200:
#     response_parts = response.text.split('\n')
#     content = ""
#     for part in response_parts:
#         try:
#             response_dict = json.loads(part)
#             message = response_dict.get('message', {})
#             content += message.get('content', '')
#         except json.JSONDecodeError as e:
#             print(e)
#     print(content.strip())
# else:
#     print(f"Error: {response.status_code}, {response.text}")

# import whisper

# model = whisper.load_model("tiny")
# audio = whisper.pad_or_trim(whisper.load_audio("response.wav"))

# mel = whisper.log_mel_spectrogram(audio)

# _, probs = model.detect_language(mel)

# print(max(probs, key=probs.get))

# options = whisper.DecodingOptions()
# result = whisper.decode(model, mel, options)
# print(result.text)

# from TTS.api import TTS

# tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
# tts.tts_to_file(text="This is a test.")

# from gtts import gTTS
# from playsound import playsound
# import tempfile

# tts = gTTS(text="Hey how can I help you today?", lang='en')

# with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_audio:
#     tts.save(temp_audio.name)
#     playsound(temp_audio.name)

# import json
# import pandas as pd

# df = pd.read_json('is_train.json')

# counts = df[1].value_counts()

# # pd.set_option('display.max_rows', None)
# # print(counts)

# not_needed = ['order_status', 'account_blocked', 'what_song', 'international_fees', 'last_maintenance', 'taxes', 
#               'min_payment', 'pin_change', 'accept_reservations', 'how_busy', 'bill_due', 'damaged_card', 'do_you_have_pets',
#               'gas_type', 'plug_type', 'tire_change', 'who_do_you_work_for', 'credit_limit', 'international_visa', 'transfer',
#               'gas', 'expiration_date', 'how_old_are_you', 'car_rental', 'jump_start', 'redeem_rewards', 'pto_balance', 'direct_deposit',
#               'credit_limit_change', 'bill_balance', 'w2', 'where_are_you_from', 'what_can_i_ask_you', 'maybe', 'oil_change_how', 'balance',
#               'confirm_reservation', 'freeze_account', 'rollover_401k', 'transactions', 'insurance_change', 'travel_alert', 'pto_request',
#               'improve_credit_score', 'change_language', 'payday', 'replacement_card_duration', 'application_status', 'flight_status',
#               'rewards_balance', 'pay_bill', 'spending_history', 'pto_request_status', 'carry_on', 'pto_used', 'schedule_maintenance',
#               'travel_notification', 'sync_device', 'report_lost_card', 'yes', 'credit_score', 'new_card', 'lost_luggage', 'mpg', 'oil_change_when',
#               'apr', 'change_speed', 'tire_pressure', 'card_declined']

# df_filtred = df[~df[1].isin(not_needed)]

# unique_labels = df_filtred[1].unique().tolist()

# print(unique_labels)

# import json
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
# from dotenv import load_dotenv
# import os

# load_dotenv()

# spotify_username = os.getenv("SPOTIFY_USERNAME")
# spotify_clientid = os.getenv("SPOTIFY_CLIENTID")
# spotify_clientsecret = os.getenv("SPOTIFY_CLIENTSECRET")
# redirect_uri = os.getenv("REDIRECT_URI")

# oauth_object = spotipy.SpotifyOAuth(spotify_clientid, spotify_clientsecret, redirect_uri)

# token_dict = oauth_object.get_access_token()
# token = token_dict['access_token']
# spotifyObject = spotipy.Spotify(auth=token)

# user = spotifyObject.current_user()

# # print(json.dumps(user, sort_keys=True, indent=4))
# devices = spotifyObject.devices()
# for idx, device in enumerate(devices['devices']):
#     print(f"{idx + 1}. {device['name']} (ID: {device['id']}, Type: {device['type']})")
# while True:
#     print("Welcome, "+ user['display_name'])
#     print("0 - Exit")
#     print("1 - Search for a Song")
#     choice = int(input("Your Choice: "))
#     if choice ==1:
#         searchQuery = input("Enter Song NAme: ")
#         searchResults = spotifyObject.search(searchQuery, 1, 0, "track")
#         tracks_items = searchResults['tracks']['items']
        
#         track = tracks_items[0]
#         track_name = track['name']
#         artist_name = track['artists'][0]['name']
#         track_uri = track['uri']
        
#         spotifyObject.start_playback(uris=[track_uri])
        
#     elif choice == 0:
#         print("bye")
#         break
    
#     else:
#         print("invalid")

import joblib

text_classifier = joblib.load('TextClassification/naive_bayes_txt_class_pipeline.pkl')

text = "if you don't mind tell me the weather two hours from now"

preds = text_classifier.predict([text])

print(preds[0])

# from piper.voice import PiperVoice
# import wave
# from playsound import playsound

# model = 'TTS_models/en_US-hfc_female-medium.onnx'
# voice = PiperVoice.load(model)
# text = "I'm sorry? I didn't understand"
# wav_file = wave.open("test.wav", 'w')
# audio = voice.synthesize(text, wav_file)

# # with open('test.wav', 'wb') as wav_file:
# #     voice.synthesize(text, wav_file)
# playsound('test.wav')