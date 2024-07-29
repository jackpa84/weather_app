import random
import requests
from transformers import pipeline
import torch
from deep_translator import GoogleTranslator
from decouple import config

class WeatherService:
    def __init__(self):
        self.device = 0 if torch.cuda.is_available() else -1
        self.text_generator = pipeline("text-generation", model="gpt2", device=self.device)
        self.translator = GoogleTranslator(source='en', target='pt')
        self.api_key = config('API_KEY')

    def get_weather(self, city):
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric&lang=pt_br"
        response = requests.get(base_url)
        return response.json()

    def generate_funny_text(self, city, weather_description):
        example_phrases = [
            f"Today it's {weather_description} in {city}.",
            f"In {city}, the weather today is {weather_description}.",
            f"The weather in {city} today can be described as {weather_description}.",
            f"{city} is experiencing {weather_description} weather today.",
            f"{weather_description} conditions are observed in {city} today."
        ]
        example_phrase = random.choice(example_phrases)
        prompt = f"Write a sentence about the weather using the city {city} and the description '{weather_description}'. Here are some examples: {example_phrase}"
        generated_text = self.text_generator(prompt, max_length=50, num_return_sequences=1, truncation=True)
        generated_text = generated_text[0]['generated_text']
        if generated_text.startswith(prompt):
            generated_text = generated_text[len(prompt):].strip()
        if city not in generated_text or weather_description not in generated_text:
            generated_text = example_phrase
        return generated_text

    def translate_to_portuguese(self, text):
        translated = self.translator.translate(text)
        return translated