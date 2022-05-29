import fuzzywuzzy as fz
import fuzzywuzzy.fuzz
from fuzzywuzzy import process
import pyttsx3
import speech_recognition as sr #РАСПОЗНАВАНИЕ ГОЛОСА
from datetime import datetime
import wikipedia as wk
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
import googletrans
from googletrans import Translator
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import http.client

options={
    "name":['маргарита','марго','маргаритка','маргоша','маргарет','мормышка'],
    "hello": ['привет','приветик','доброе утро','добрый день','добрый вечер','доброго полудня','здравствуй','привяо','здравствуйте','приветствую','здраввья желаю'],
    "commands":
    {
    "wikipedia": ['википедия','википедии','найди определение',"произведи поиск определения","понятие","понятия"],
    "ToDo":["добавить","добавь задачу","добавь пункт","список дел","задача","список"],
    "weather":['определи погоду','какая температура','температура','сколько градусов','погода'],
    "time":['текущее время','время','часы','который час','сколько время'],
    "translate":['переведи','перевести','перевод','переведи предолженние с английского на русский'],
    "news": ['расскажи новости', 'какие на сегодня новости', 'новости', 'новостная лента'],
    "games_parser":['игры','новости игр','изумительно','лучшие игры','рейтинг игр','игровая статистика','топ игр']
    }
}
engine = pyttsx3.init()
engine.setProperty('rate',200)
engine.setProperty('volume',1)
for voice in engine.getProperty('voices'):
    if voice.name == 'Microsoft Irina Desktop - Russian':
            engine.setProperty('voice',voice.id)
wk.set_lang("ru")
r = sr.Recognizer()
def Listening():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        ToSpeak("Производится распознавание....")
        audio = r.listen(source)
        try:
            print("Обработка...")
            query = r.recognize_google(audio, language='ru-Ru')
            return query
        except sr.UnknownValueError:
            ToSpeak("Не распознано, повторите попытку")
        except sr.RequestError:
            ToSpeak("Проверьте подключение к интернету")
def ToSpeak(message):
    print(message)
    engine.say(message)
    engine.runAndWait()
    engine.stop()
def weather():
    try:
        translator = Translator()
        ToSpeak("Назовите место")
        place = Listening()
        owm = OWM("534324c556267d6b37c995f1505d8371")
        mgr = owm.weather_manager()
        obs = mgr.weather_at_place(place)
        w = obs.weather
        w_status=translator.translate(w.status,src='en',dest='ru').text
        if w_status=="Облака":
            w_status="Облачно"
        elif w_status=="Прозрачный":
            w_status="Ясно"
        current = w.temperature('celsius')['temp']
        feels_like = w.temperature('celsius')['feels_like']
        ToSpeak(f'Город: {place}. Статус погодного состояния: {w_status} Температура воздуха составляет {int(current)} градусов по цельсию. Ощущается как {int(feels_like)} градусов')

    except:
        ToSpeak("Я не понимаю вас, повторите попытку")
def wikipedia():
    try:
        ToSpeak("Произнесите запрос")
        mesg =Listening()
        ToSpeak("Произвожу поиск совпадений")
        message = wk.summary(mesg, sentences=2)
        ToSpeak(f'Результат найден\n{message}')
    except:
        ToSpeak("Запрос не произведен, повторите попытку")
def ToDo():
    try:
        myfile=open('../ToDo_list.txt', "a")
        ToSpeak("Скажите задачу")
        task=Listening()
        myfile.write(task+"\n")
    except:
        ToSpeak("Задача не добавлена, повторите попытку")
def time():
    date = datetime.now()
    ToSpeak(f'Московское время {date.strftime("%H:%M:%S")}')
def get_key(string):
    key=""
    amax=0
    for x,y in options["commands"].items():
        a=fuzzywuzzy.fuzz.WRatio(string,y)
        if (a>amax):
            amax=a
            key=x
    return key
def translate():
    translator = Translator()
    ToSpeak("Что желаете перевести?")
    message = Listening()
    result = translator.translate(message)
    ToSpeak(result.text)
def games_parser():
    try:
        gameslist=[]
        url = 'https://stopgame.ru/games/filter?year_start=1980&rating=izumitelno'
        r = requests.get(url)
        temp=0
        html=BeautifulSoup(r.content,'html.parser')
        for el in html.select("#w0 > div.items > div"):
            temp+=1
            result=''
            title = el.select("#w0 > div.items > div > div > div > div > div.caption.caption-bold")
            for i in range(len(title[0].text)):
                if title[0].text[i]!='\n' and title[0].text[i]!='\r':
                    result+=title[0].text[i]
            gameslist.append(str(temp)+"."+result+'\n')
        gameslist=garbage_cleaner(gameslist)
        ToSpeak("Топ изумительных игр согласно рейтингу stopgame.ru\n" + gameslist)
    except Exception as e:
        print(e)

def garbage_cleaner(mass):
    mass = ''.join([mass[i] for i in range(len(mass)) if (mass[i] != '\n' and mass[i] != '\r')])
    return mass
def news():
    newslist=[]
    url="https://news.mail.ru/"
    r=requests.get(url)
    html=BeautifulSoup(r.content,"html.parser")

    for el in html.select("#index_page > div.layout > div:nth-child(2) > div > div.block > div > div:nth-child(2) > div > ul"):
        title = el.select("#index_page > div.layout > div:nth-child(2) > div > div.block > div > div:nth-child(2) > div > ul > li")
        for i in range (len(title)):
            newslist.append(str(i+1)+'.'+title[i].text+'\n')
    newslist.append ("Подробнее на сайте источника https://news.mail.ru/")
    newslist=garbage_cleaner(newslist)
    ToSpeak(newslist)

