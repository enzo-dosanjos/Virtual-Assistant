from pprint import pprint
import requests
import datetime
import base64
from bs4 import BeautifulSoup
from colorama import Fore, Style

#Afin d'avoir le token obtenu lors de la connection
def login():
    r = requests.Session()
    url = "https://api.ecoledirecte.com/v3/login.awp"
    payload = "data={\n\t\"identifiant\": \"Enzo.DosAnjos\",\n\t\"motdepasse\": \"Enzo2909\"\n}"
    try:
        res = r.post(url, data=payload)
        return res.json()['token']
    except Exception as exception:
        if type(exception).__name__ == "ConnectionError":
            print(Fore.RED + "La connexion a échoué" + Style.RESET_ALL)
            print(Fore.RED + "Vérifiez votre connexion Internet." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Une erreur inconnue est survenue." + Style.RESET_ALL)

def get_marks():
    token = login()
    r = requests.Session()
    url = "https://api.ecoledirecte.com/v3/eleves/614/notes.awp?verbe=get"
    payload = "data={\n\t\"token\": \"" + token + "\"\n}"
    res = r.post(url, data=payload)
    for notes in res.json()['data']['notes']:
        if notes['codeMatiere'] == 'SPESP':
            pprint(notes)

def get_moyennes(asked_matiere):
    token = login()
    r = requests.Session()
    url = "https://api.ecoledirecte.com/v3/eleves/614/notes.awp?verbe=get"
    payload = "data={\n\t\"token\": \"" + token + "\"\n}"
    res = r.post(url, data=payload)
    if asked_matiere == 'general':
        moyenne = res.json()['data']['periodes'][0]['ensembleMatieres']['moyenneGenerale']
        moyenne_classe = res.json()['data']['periodes'][0]['ensembleMatieres']['moyenneClasse']
        moyenne_max = res.json()['data']['periodes'][0]['ensembleMatieres']['moyenneMax']
        return moyenne, moyenne_classe, moyenne_max
    for notes_matiere in res.json()['data']['periodes'][0]['ensembleMatieres']['disciplines']:
        matiere = notes_matiere['discipline']
        if matiere == asked_matiere:
            moyenne = notes_matiere['moyenne']
            moyenne_classe = notes_matiere['moyenneClasse']
            moyenne_max = notes_matiere['moyenneMax']
            return moyenne, moyenne_classe, moyenne_max

def get_homeworks(asked_date):
    date = datetime.date.today()
    token = login()
    r = requests.Session()
    url = 'https://api.ecoledirecte.com/v3/Eleves/614/cahierdetexte.awp?verbe=get'
    payload = "data={\n\t\"token\": \"" + token + "\"\n}"
    res = r.post(url, data=payload)
    if asked_date == 'None':
        for dates in res.json()['data']:
            for devoirs in res.json()['data'][dates]:
                if devoirs.get('effectue') == False:
                    pprint(devoirs)
                    matiere = devoirs[0]['matiere']
                    id = devoirs[0]['idDevoir']
                    return matiere, date, id
    elif asked_date == 'today':
        date = date.isoformat()
        for devoirs in res.json()['data'][date]:
            if devoirs.get('effectue') == False:
                pprint(devoirs)
                matiere = devoirs[0]['matiere']
                id = devoirs[0]['idDevoir']
                return matiere, date, id
    elif asked_date == 'tomorrow':
        date += datetime.timedelta(days=1)
        date = date.isoformat()
        for devoirs in res.json()['data'][date]:
            if devoirs.get('effectue') == False:
                pprint(devoirs)
                matiere = devoirs[0]['matiere']
                id = devoirs[0]['idDevoir']
                return matiere, date, id
    elif asked_date == 'nextweek':
        weekday = datetime.datetime.today().weekday()
        ttonextweek = 7 - weekday
        start_nextweek = date + datetime.timedelta(days=ttonextweek)
        end_nextweek = start_nextweek + datetime.timedelta(days=6)
        for dates in res.json()['data']:
            if date.fromisoformat(dates) >= start_nextweek and date.fromisoformat(dates) <= end_nextweek:
                for devoirs in res.json()['data'][dates]:
                    if devoirs.get('effectue') == False:
                        pprint(devoirs)
                        matiere = devoirs[0]['matiere']
                        id = devoirs[0]['idDevoir']
                        return matiere, date, id

def get_homeworks_content(date, devoir_id):
    token = login()
    r = requests.Session()
    url = 'https://api.ecoledirecte.com/v3/Eleves/614/cahierdetexte/' + date +'.awp?verbe=get'
    payload = "data={\n\t\"token\": \"" + token + "\"\n}"
    res = r.post(url, data=payload)
    content = res.json()['data']['matieres'][devoir_id]['aFaire']['contenu']
    text = BeautifulSoup(base64.b64decode(content), features="html.parser")
    text = text.get_text()
    return text

def set_homeworks_done(hw_id):
    token = login()
    r = requests.Session()
    url = 'https://api.ecoledirecte.com/v3/Eleves/614/cahierdetexte.awp?verbe=put'
    payload = "data={\n\t\"idDevoirsEffectues\": [\n        " + str(hw_id) + "\n    ],\n\t\"token\": \"" + token + "\"\n}"
    res = r.post(url, data=payload)

def new_messages(action, nb):
    token = login()
    r = requests.Session()
    url = "https://api.ecoledirecte.com/v3/eleves/614/messages.awp?verbe=getall&orderBy=date&order=desc"
    payload = "data={\n\t\"token\": \"" + token + "\"\n}"
    res = r.post(url, data=payload)
    new_messages = []
    if action == 'news':
        new_msg = []
        for messages in res.json()['data']['messages']['received']:
            if messages.get('read') == False:
                new_messages += [messages.get('subject')]
        nb_new_msg = (len(new_messages))
        for i in range(len(new_messages)):
            new_msg += [(new_messages[i])]
        return nb_new_msg, new_msg
    if action == 'unseentoseen':
        url = "https://api.ecoledirecte.com/v3/eleves/614/messages.awp?verbe=put"
        for messages in res.json()['data']['messages']['received']:
            if messages.get('read') == False:
                id = str(messages.get('id'))
                payload = "data={\n    \"action\": \"marquerCommeLu\",\n    \"ids\": [\n        " + id + "\n    ],\n    \"token\": \"" + token + "\"\n}"
                res = r.post(url, data=payload)

login()