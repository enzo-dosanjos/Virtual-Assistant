import sys
import threading
import pyautogui
import os
from playsound import playsound
import speech_recognition as sr
import pyttsx3
import pywhatkit as wkit
import wikipedia
import pyjokes
from datetime import datetime
import time
from EcoleDirecte import new_messages
from colorama import Fore, Style
from Weather import *

r = sr.Recognizer()
mic = sr.Microphone(device_index=3)
engine = pyttsx3.init()
wikipedia.set_lang("fr")
firefox_loc = "C:/Program Files/Mozilla Firefox/firefox.exe"


def talk(text):
    text = text.replace('.', ',')
    nombres = [s for s in text.split() if s.isdigit()]
    unchanged_text = text
    if len(nombres) > 0:
        for i in range(len(nombres)):
            text = text.replace(str(nombres[i]), (Fore.BLUE + str(nombres[i]) + Fore.GREEN))
    print(Fore.GREEN + '->' + text + Style.RESET_ALL)
    engine.say(unchanged_text)
    engine.runAndWait()


def questions(text):
    print(Fore.RED + '->' + text + Style.RESET_ALL)
    engine.say(text)
    engine.runAndWait()


def alarm(alarm_time):
    while True:
        time.sleep(1)
        current_time = datetime.now()
        now = current_time.strftime('%H%M%S')
        date = current_time.strftime('%d%m%Y')
        if now == alarm_time:
            playsound('C:/Users/Enzo/PycharmProjects/Aina/Sounds/alarm_sound.mp3')
            time.sleep(0.1)
            morning_routine()
            break


def morning_routine():  # ajouter le jour
    timeh = datetime.now().strftime('%H')
    timemin = datetime.now().strftime('%M')
    city = 'Rillieux-La-Pape'
    current_weather = get_current_weather(city)
    day_weather = get_daily_weather(city, 'today')
    temp, min_temp, max_temp, condition, day_condition = str(current_weather[1]).replace('.', ','), str(
        day_weather[1]).replace('.', ','), str(day_weather[2]).replace('.', ','), str(
        current_weather[0]).replace('.', ','), str(day_weather[0]).replace('.', ',')
    talk('Bonjour Monsieur')
    talk('il est ' + timeh + ' heure ' + timemin)
    talk('Dehors, Il fait ' + temp + ' degr??e avec un ' + condition)
    talk("Aujourd'hui attendez-vous ?? un temps " + day_condition + ' avec une temp??rature minimale de ' + min_temp + ' degr?? et une temp??rature maximale de ' + max_temp + ' degr??')


def Aina():
    try:
        with mic as source:
            print(Fore.MAGENTA + 'listening...' + Style.RESET_ALL)
            r.adjust_for_ambient_noise(source, duration=1)
            voice = r.listen(source)
            command = r.recognize_google(voice, language='fr-FR')
            command = command.lower()
            if 'aina' in command or 'ayna' in command:
                command = command.replace('aina', '')
                command = command.replace('ayna', '')
                return command

    except:
        pass
    return command


def func_command():
    command = Aina()
    print(command)
    return command


def RunAina():
    command = func_command()
    # demander l'heure
    if 'heure' in command:
        timeh = datetime.now().strftime('%H')
        timemin = datetime.now().strftime('%M')
        talk('il est ' + timeh + ' heure ' + timemin)
    # jouer une musique sur youtube
    elif 'joue' in command:
        songname = command.replace('joue', '')
        if 'sur youtube' in command:
            songname = command.replace('sur youtube', '')
            talk('Je met' + songname + 'sur youtube')
            wkit.playonyt(songname)
        else:
            talk('Je met' + songname)
            os.startfile(firefox_loc)
            time.sleep(0.1)
            wkit.playonyt(songname)
            time.sleep(0.1)
            pyautogui.hotkey('alt', 'tab')
    # chercher sur wikip??dia
    elif 'cherche' in command or 'qui est' in command:
        search = command.replace('cherche', '')
        if 'sur google' in command:
            recherche = search.replace('sur google', '')
            wkit.search(recherche)
        else:
            info = wikipedia.summary(search, sentences=1)
            talk(info)
    # raconte une blague
    elif 'blague' in command:
        blague = pyjokes.get_joke(language='fr', category='all')
        talk(blague)
    # mettre une alarme
    elif 'alarme' in command:
        heure = [s for s in command if s.isdigit()]
        if len(heure) == 1:  # ?? optimiser
            hour = heure[0]
            min = 0
            talk('alarme programm?? pour ' + hour + ' heure')
        elif len(heure) == 2:
            hour = heure[0] + heure[1]
            min = 0
            talk('alarme programm?? pour ' + hour + ' heure')
        elif len(heure) == 3:
            hour = heure[0]
            min = heure[1] + heure[2]
            talk('alarme programm?? pour ' + hour + ' heure ' + min)
        elif len(heure) == 4:
            hour = heure[0] + heure[1]
            min = heure[2] + heure[3]
            talk('alarme programm?? pour ' + hour + ' heure ' + min)
        else:
            talk("le format de l'heure que vous avez donn?? est invalide")
            pass
        alarm_time = hour + min + '00'  # prendre en compte le jour
        t = threading.Timer(1, alarm, [alarm_time]) #impossible d'appeler les fonction venant d'autre .py
        t.start()
# ne peut pas ??tre r??p??t??
    # arr??ter le programme
    elif 'arr??te-toi' in command:
        talk('arr??t en cours')
        sys.exit()  # ne fonctionne pas
    # change le son du pc
    elif 'son de mon pc' in command or 'volume de mon pc' in command:
        asked_volume = 2
        if 'pc de' in command or 'pc ??' in command:
            asked_volume = [int(s) for s in command.split() if s.isdigit()]
            asked_volume = asked_volume[0]
            if asked_volume > 100 or asked_volume < 0:
                talk('valeur de volume invalide')
                asked_volume = 2
        if (asked_volume % 2) == 1:
            asked_volume = asked_volume + 1
        if 'met' in command:
            for i in range(50):
                pyautogui.press('volumedown')
            for i in range(int(asked_volume / 2)):
                pyautogui.press('volumeup')
            talk('le son de votre pc ?? ??t?? mis ?? ' + str(asked_volume))
        elif 'monte' in command:
            for i in range(int(asked_volume / 2)):
                pyautogui.press('volumeup')
            talk('le son de votre pc a ??t?? mont?? de ' + str(asked_volume))
        elif 'baisse' in command:
            for i in range(int(asked_volume / 2)):
                pyautogui.press('volumedown')  # baisse plus que ce qu'on demande
            talk('le son de votre pc ?? ??t?? baiss?? de ' + str(asked_volume))
        elif 'mute' in command or 'coupe' in command:
            pyautogui.press('volumemute')
            talk('le son de votre pc a ??t?? mut??')
        elif 'd??mute' in command or 'remet' in command:
            pyautogui.press('volumemute')
            talk('le son de votre pc a ??t?? d??mut??')
    # r??gler le son
    elif 'son' in command or 'volume' in command:
        asked_volume = [int(s) for s in command.split() if s.isdigit()]
        if len(asked_volume) >= 1:
            asked_volume = asked_volume[0] / 10
        else:
            asked_volume = 0.5
        if asked_volume > 1 or asked_volume < 0:
            talk('valeur de volume invalide')
        else:
            engine_volume = engine.getProperty('volume')
            if 'baisse' in command:
                if engine_volume == 0.1:
                    talk('le son est d??j?? au minimum')
                else:
                    new_volume = engine_volume - 0.1
                    engine.setProperty('volume', new_volume)
                    talk('le son a ??t?? baiss?? ?? ' + str(int(new_volume * 10)))
            elif 'monte' in command:
                if engine_volume == 1:
                    talk('le son est d??j?? au maximum')
                else:
                    new_volume = engine_volume + 0.1
                    engine.setProperty('volume', new_volume)
                    talk('le son a ??t?? mont?? ?? ' + str(
                        int(new_volume * 10)))  # probl??me : dit 7 alors que c'??tait d??j?? ?? 7 puis monte ?? 9 apr??s
            elif 'mets' in command:
                engine.setProperty('volume', asked_volume)
                talk('le son a ??t?? mis ?? ' + str(int(asked_volume * 10)))
            elif 'quel est' in command:
                talk('le son est ?? ' + str(int(engine_volume * 10)))
    # change de fen??tre
    elif 'change de fen??tre' in command:
        pyautogui.hotkey('alt', 'tab')
        talk('la fen??tre ?? ??t?? switch??')
    # ??crit ce qu'on lui dit
    elif '??cris' in command:
        command = command.replace('??cris', '')
        pyautogui.write(command)
    # appuie sur une touche
    elif 'appu' in command:
        if 'play' in command:
            pyautogui.hotkey('playpause')
        elif 'pause' in command:
            pyautogui.hotkey('playpause')
        elif 'entr??' in command:
            pyautogui.hotkey('enter')
    # retourne en avant ou en arri??re
    elif 'retourne' in command:
        if 'avant' in command:
            pyautogui.hotkey('browserforward')
            talk('je suis retourn?? en avant')
        elif 'arri??re' in command:
            pyautogui.hotkey('browserback')
            talk('je suis retourn?? en arri??re')
    # permet de fermer la fen??tre ou la page
    elif 'ferme' in command:
        if 'fen??tre' in command:
            pyautogui.hotkey('alt', 'f4')
        elif 'page' in command:
            pyautogui.hotkey('ctrl', 'w')
    # permet d'ouvrir une app
    elif 'ouvre' in command:
        if 'firefox' in command:
            os.startfile(firefox_loc)
    # refresh la page
    elif 'refresh' in command:
        pyautogui.hotkey('browserrefresh')
    # calcul
    elif 'combien fait' in command:
        command = command.replace('combien fait ', '')
        command = command.replace('x', '*')
        calcul = round(eval(command), 3)
        talk('Cela fait ' + str(calcul))
    # voir les nouveaux messages ??coles directe
    elif 'message' in command and '??cole' in command or 'ecoledirecte' in command:
        messages = new_messages('news', 0)
        talk('vous avez ' + str(messages[0]) + ' nouveaux messages ??cole directe')
        if messages[0] != 0:
            questions('Voulez-vous savoir leur sujet?')
            res = func_command()
            if 'oui' in res:
                talk('les sujets des messages sont:')
                for i in range(len(messages[1])):
                    talk(str(messages[1][i]))
            else:
                talk("d'accord")
            questions('Voulez-vous les marquer comme lu?')
            res = func_command()
            if 'oui' in res:
                new_messages('unseentoseen', 0)
                talk('les messages ont ??t?? marqu?? comme lu')
            else:
                talk("d'accord")
    #voir les devoirs sur ??coles directe
    elif 'devoir' in command:
        today = datetime.today()
        date = today.strftime('%y') + '-' + today.strftime('%m') + '-' + today.strftime('%d')
    # savoir le temps
    elif 'temps' in command: #ajouter la possibilit?? de simplement dire le jour
        city = 'Rillieux-La-Pape'
        weekday = datetime.today().weekday()
        day = days[weekday]
        for words in command.split():
            if words in days:
                if days.index(words) <= weekday:
                    day = 7 - weekday + days.index(words)
                else:
                    if 'prochain' in command:
                        talk("Je ne sais pas car je ne peux donner la m??t??o que pour 7 jours")
                    else:
                        day = days.index(words) - weekday
                day_weather = get_daily_weather(city, day)
                if day == 1:
                    talk("Demain, attendez-vous ?? un temps " + str(day_weather[0]) + ' avec une temp??rature minimale de ' + str(day_weather[1]) + ' degr?? et une temp??rature maximale de ' + str(day_weather[2]) + ' degr??')
                else:
                    talk(words + " attendez-vous ?? un temps " + str(day_weather[0]) + ' avec une temp??rature minimale de ' + str(day_weather[1]) + ' degr?? et une temp??rature maximale de ' + str(day_weather[2]) + ' degr??')
        if 'dans' in command and 'jours' in command:
            day = [s for s in command.split() if s.isdigit()]
            day_weather = get_daily_weather(city, int(day[0]))
            talk('Dans ' + day[0] + ' jours, attendez-vous ?? un temps ' + str(day_weather[0]) + ' avec une temp??rature minimale de ' + str(day_weather[1]) + ' degr?? et une temp??rature maximale de ' + str(day_weather[2]) + ' degr??')
        elif 'apr??s-demain' in command or 'apr??s demain' in command or 'dans 2 jours' in command:
            day_weather = get_daily_weather(city, 2)
            talk("Apr??s-demain, attendez-vous ?? un temps " + str(day_weather[0]) + ' avec une temp??rature minimale de ' + str(day_weather[1]) + ' degr?? et une temp??rature maximale de ' + str(day_weather[2]) + ' degr??')
        elif 'demain' in command or 'dans 1 jour' in command:
            day_weather = get_daily_weather(city, 1)
            talk("Demain, attendez-vous ?? un temps " + str(day_weather[0]) + ' avec une temp??rature minimale de ' + str(day_weather[1]) + ' degr?? et une temp??rature maximale de ' + str(day_weather[2]) + ' degr??')
        elif 'dans 7 jours' in command or 'dans une semaine' in command:
            day_weather = get_daily_weather(city, 7)
            talk("Dans une semaine, attendez-vous ?? un temps " + str(day_weather[0]) + ' avec une temp??rature minimale de ' + str(day_weather[1]) + ' degr?? et une temp??rature maximale de ' + str(day_weather[2]) + ' degr??')
        elif "aujourd'hui" in command or '' in command:
            current_weather = get_current_weather(city)
            day_weather = get_daily_weather(city, 0)
            talk("Actuellement ?? " + city + ' il fait ' + str(current_weather[1]) + ' degr??e avec un ' + str(current_weather[0]))
            talk("Aujourd'hui attendez-vous ?? un temps " + str(day_weather[0]) + ' avec une temp??rature minimale de ' + str(day_weather[1]) + ' degr?? et une temp??rature maximale de ' + str(day_weather[2]) + ' degr??')
    # phrase fonctionne
    elif 'cool' in command:
        talk('je suis content que vous arriviez ?? me faire fonctionner')
    else:
        talk("Je n'ai pas compris, pourriez vous r??p??ter")


while True:
    try:
        RunAina()
    except:
        pass
