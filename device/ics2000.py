from conf.config import config
import requests
from datetime import datetime, timedelta


class ICS2000:

    def __init__(self, mac_address, email_address, password, proxies=None):
        self.mac_address = mac_address
        self.email_address = email_address
        self.password = password
        self.proxies = proxies if proxies is not None else {}

    def get_response(self, start_date, end_date):
        return requests.get(
            'https://trustsmartcloud2.com/ics2000_api/p1.php',
            allow_redirects=False,
            proxies=self.proxies,
            params={
                'start_date': start_date.strftime("%Y-%m-%d %H:00:00"),
                'end_date': end_date.strftime("%Y-%m-%d %H:00:00"),
                'precision': 'hour',
                'password_hash': self.password,
                'action': 'aggregated_reports',
                'differential': 'false',
                'mac': self.mac_address,
                'interpolate': 'true',
                'email': self.email_address
            }
        ).json()

    def get_info(self):
        end = datetime.now()
        start = end - timedelta(days=1)
        prev_kwh_high = -1
        prev_kwh_low = -1
        prev_m3_gass = -1
        first = True

        for x in self.get_response(start, end):
            if x[0] is not None and x[1] is not None and x[4] is not None:
                kwh_high = x[0] / 1000
                kwh_low = x[1] / 1000
                m3_gass = x[4] / 1000
                if not first:
                    reading = {
                        'timestamp': start.strftime("%Y-%m-%d %H:00:00"),
                        'kWhHighReading': kwh_high,
                        'kWhLowReading': kwh_low,
                        'm3GassReading': m3_gass,
                        'kWhHighUsage': kwh_high - prev_kwh_high,
                        'kWhLowUsage': kwh_low - prev_kwh_low,
                        'm3GassUsage': m3_gass - prev_m3_gass
                    }
                    reading.update({
                        'kWhHighCost': reading['kWhHighUsage'] * config['ics2000']['kWhHighPrice'],
                        'kWhLowCost': reading['kWhLowUsage'] * config['ics2000']['kWhLowPrice'],
                        'm3GassCost': reading['m3GassUsage'] * config['ics2000']['gassM3Price']
                    })

                    yield reading

                start = start + timedelta(hours=1)
                prev_kwh_high = kwh_high
                prev_kwh_low = kwh_low
                prev_m3_gass = m3_gass
                first = False
