import requests
from pprint import pprint

days = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

def get_current_weather(city):
    r = requests.Session()
    url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=a0aeb5e2a1e05410e935e61896282b56&lang=fr'
    res = r.get(url)
    condition = res.json()['weather'][0]['description']
    temp = int(round((res.json()['main']['temp'])-273.15, 0))
    return condition, temp
def get_daily_weather(city, day):
    r = requests.Session()
    url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=a0aeb5e2a1e05410e935e61896282b56&lang=fr'
    res = r.get(url)
    lon = res.json()['coord']['lon']
    lat = res.json()['coord']['lat']
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat=' + str(lat) + '&lon=' + str(lon) + '&exclude=current,minutely,hourly,alerts&appid=a0aeb5e2a1e05410e935e61896282b56&lang=fr'
    res = r.get(url)
    condition = res.json()['daily'][day]['weather'][0]['description']
    min_temp = int(round((res.json()['daily'][day]['temp']['min']) - 273.15, 0))
    max_temp = int(round((res.json()['daily'][day]['temp']['max']) - 273.15, 0))
    return condition, min_temp, max_temp