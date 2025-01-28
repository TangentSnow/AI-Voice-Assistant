import requests
import json
import geocoder
from dotenv import load_dotenv
import os

class services():
    def __init__(self):
        load_dotenv()
        self.weather_url = 'http://api.weatherapi.com/v1/current.json'
        self.location = (geocoder.ip('me')).latlng
        self.WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
        self.payload = {
            "key": self.WEATHER_API_KEY,
            "q": self.location
        }
        
    def handle_weather(self):
        response = requests.post(self.weather_url, self.payload)
        data = json.loads(response.text)
        weather_location = data['location']['name']
        temp_f = data['current']['temp_f']
        condition = data['current']['condition']['text']
        feelslike_f = data['current']['feelslike_f']
        to_voice = f"Currently, in {weather_location}, the temprature is {temp_f} degrees Fahrenheit, but it feels like {feelslike_f} degrees Fahrenheit. The weather condition is {condition}"
        
        return to_voice