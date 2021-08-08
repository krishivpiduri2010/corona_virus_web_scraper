import requests
import json
import pyttsx3
import speech_recognition as sr
import re
import threading
import time

API_KEY = "{PUT-YOURS-HERE}"
PROJECT_TOKEN = "{PUT-YOURS-HERE}"
RUN_TOKEN = "{PUT-YOURS-HERE}"


class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }
        self.get_data()

    def get_data(self):
        self.data = json.load(open('run_results.json'))

    def get_total_cases(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Coronavirus Cases:":
                return content['value']

    def get_total_deaths(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Deaths:":
                return content['value']

        return "0"

    def get_total_recovered(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Recovered:":
                return content['value']

        return "0"

    def get_country_data(self, country: str) -> dict:
        data = self.data["country"]

        for content in data:
            if content['name'].lower() == country.lower():
                return content

        return "0"

    def get_list_of_countries(self):
        countries = []
        for country in self.data['country']:
            countries.append(country['name'])
        return countries


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print("Exception:", str(e))

    return said.lower()


def main():
    print('Started')
    END_PHRASE = 'stop'
    TOTAL_PATTERNS = {
        re.compile("[\w\s]+ total [\w\s]+ cases"): data.get_total_cases,
        re.compile("[\w\s]+ total cases"): data.get_total_cases,
        re.compile("[\w\s]+ total [\w\s]+ deaths"): data.get_total_deaths,
        re.compile("[\w\s]+ total deaths"): data.get_total_deaths,
        re.compile("[\w\s]+ total recovered"): data.get_total_recovered,
        re.compile("[\w\s]+ recovered"): data.get_total_recovered,
    }
    COUNTRY_PATTERNS = {
        re.compile("[\w\s]+ cases [\w\s]+"): lambda countri: data.get_country_data(countri)['total_cases'],
        re.compile("[\w\s]+ deaths [\w\s]+"): lambda countri: data.get_country_data(countri)['total_deaths'],
        re.compile("[\w\s]+ population [\w\s]+"): lambda countri: data.get_country_data(countri)['popu'],
        re.compile("[\w\s]+ tests [\w\s]+"): lambda countri: data.get_country_data(countri)['total_tests'],
        re.compile("[\w\s]+ total tests [\w\s]+"): lambda countri: data.get_country_data(countri)['total_tests'],
        re.compile("[\w\s]+ activate cases [\w\s]+"): lambda countri: data.get_country_data(countri)[
            'activation_cases'],
    }
    country_list = data.get_list_of_countries()

    while True:
        print('Listening')
        text = get_audio()
        result = ''
        for pattern, func in COUNTRY_PATTERNS.items():
            if pattern.match(text):
                words = text.split(" ")
                for country in country_list:
                    for word in words:
                        if country.lower() == word.lower():
                            result = func(country)
                            break
        for pattern, func in TOTAL_PATTERNS.items():
            if pattern.match(text):
                result = func()
                break
        print(f'You said:{text}')

        if result:
            print(result)
            speak(result)
        if text.find(END_PHRASE) != -1:
            print('end')
            break


data = Data(API_KEY, PROJECT_TOKEN)
main()
