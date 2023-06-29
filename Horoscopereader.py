import csv
import random
import pyttsx3
from flask import Flask, render_template, request

app = Flask(__name__)

class TodayHoroscope:
    def __init__(self, sign, horoscope):
        self.sign = sign
        self.horoscope_for_today = horoscope

def select_random_horoscope(horoscopes, sign):
    horoscopes_for_sign = [horoscope for horoscope in horoscopes if horoscope.sign.lower() == sign]
    if horoscopes_for_sign:
        return random.choice(horoscopes_for_sign).horoscope_for_today
    else:
        return "No horoscope available for your sign."

def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  # Adjust the speech rate (words per minute)
    engine.say(text)
    engine.runAndWait()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sign = request.form.get('sign')
        if sign.strip().lower() in ('aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'):
            with open("horoscope.csv", "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                all_horoscopes = [TodayHoroscope(sign=row[0], horoscope=row[1]) for row in reader]
                selected_horoscope = select_random_horoscope(all_horoscopes, sign)
                speak_text(selected_horoscope)
                return render_template('index.html', horoscope=selected_horoscope)
        else:
            error_message = "Invalid sign. Please enter a valid sign."
            return render_template('index.html', error_message=error_message)
    return render_template('index.html')

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)