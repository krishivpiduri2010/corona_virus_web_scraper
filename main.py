import pyttsx3
import speech_recognition as sr
import re
import requests

API_KEY = 'tzVkfqeibzHk'
PROJECT_TOKEN = 'tBDXkNqFykb3'
RUN_TOKEN = 'tktNJJD - JG - E'


class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {'api_key': self.api_key}
        self.get_data()

    def get_data(self):
        self.data = requests.get(f'https://parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data',
                                 params={'api_key': API_KEY}).json()

    def get_total_cases(self):
        data = self.data['total']
        for content in data:
            if content['name'] == 'Coronavirus Cases:':
                return content['value']

    def get_total_deaths(self):
        data = self.data['total']
        for content in data:
            if content['name'] == 'Deaths:':
                return content['value']

    def get_total_recovered(self):
        data = self.data['total']
        for content in data:
            if content['name'] == 'Recovered:':
                return content['value']

    def get_country_data(self, country):
        data = self.data['country']
        for content in data:
            if content['name'].lower() == country.lower():
                return content


data = Data(API_KEY, PROJECT_TOKEN)


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r=sr.Recognizer()
    with sr.Microphone as s:
        audio=r.listen(s)
        said=''
        try:
            source=r.recognize_google(audio)
        except Exception as e:
            print(str(e))

