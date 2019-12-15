from conf.config import config
import requests
from datetime import datetime, timedelta


class OWM:

    def __init__(self, url, id, app_id, units, proxies=None):
        self.url = url
        self.id = id
        self.app_id = app_id
        self.units = units
        self.proxies = proxies if proxies is not None else {}

    def get_owm(self):
        r = requests.get(
            url=self.url,
            params={
                'id': self.id,
                'appid': self.app_id,
                'units': self.units
            }
        ).json()

        r.update({
            'timestamp': r['dt'],
            'weather_main': r['weather'][0]['main'],
            'weather_description': r['weather'][0]['description'],
            'lon': r['coord']['lon'],
            'lat': r['coord']['lat'],
            'wind_speed': r['wind']['speed'],
            'wind_deg': r['wind']['deg'],
            'country': r['sys']['country'],
            'sunrise': r['sys']['sunrise'],
            'sunset': r['sys']['sunset'],
            'clouds_all': r['clouds']['all'],
            'temp': r['main']['temp'],
            'feels_like': r['main']['feels_like'],
            'temp_min': r['main']['temp_min'],
            'temp_max': r['main']['temp_max'],
            'pressure': r['main']['pressure'],
            'humidity': r['main']['humidity']
        })

        r.pop('cod')
        r.pop('weather')
        r.pop('dt')
        r.pop('coord')
        r.pop('base')
        r.pop('wind')
        r.pop('sys')
        r.pop('main')
        r.pop('clouds')
        r.pop('id')

        return r
