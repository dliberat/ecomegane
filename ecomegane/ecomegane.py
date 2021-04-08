import requests
from datetime import date, datetime

from bs4 import BeautifulSoup


def try_parse_kwh(val):
    try:
        return float(val)
    except ValueError:
        return None


class EcoMeganeClient():
    """Downloads data from the Eco Megane monitoring platform.

    Example usage:
    ```
    import datetime
    from ecomegane import EcoMeganeClient

    today = datetime.date.today()
    site_id = '00035322534'

    with EcoMeganeClient(user, password) as client:
        kwh = client.get_hourly_kwh(site_id, today)
        
        for timestamp, energy in kwh.items():
            print(timestamp, energy)
    ```
    """

    TIMEOUT = (6, 9.05)

    def __init__(self, user, pw):
        self.user = user
        self.password = pw
        self.sess = requests.Session()
        self.uri = 'https://eco-megane.jp/index.php'

        headers = {
            'accept': 'application/xml, text/xml, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,ja;q=0.8',
            'cache-control':   'no-cache',
            'dnt': '1',
            'origin': 'https://eco-megane.jp',
            'pragma': 'no-cache',
            'referer': 'https://eco-megane.jp/index.php',
            'sec-ch-ua':          '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile':   '?0',
            'sec-fetch-dest':     'empty',
            'sec-fetch-mode':     'cors',
            'sec-fetch-site':     'same-origin',
            'user-agent':         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        }
        self.sess.headers.update(headers)

    def __enter__(self):
        # get session cookies
        self._get(self.uri)
        self._login()
        return self

    def __exit__(self, a, b, c):
        return

    def _get(self, *args, **kwargs):
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.TIMEOUT
        return self.sess.get(*args, **kwargs)

    def _post(self, *args, **kwargs):
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.TIMEOUT
        return self.sess.post(*args, **kwargs)

    def _login(self):
        params = {
            'mailaddress': self.user,
            'password': self.password,
            'omission': 'on',
            'fnc': 'login',
            'act': 'login',
        }
        return self._post(self.uri, params=params)

    def get_hourly_kwh(self, site_id: str, target_date: date):
        """Download hourly energy generation for a single day in kWh.

        Args:
            site_id (str) - Unique identifier for a PV system
            target_date (datetime.date) - Date for which to download data.
        
        Returns:
            dict. Keys are timestamps in ISO format.
            Values are energy generation in kWh.
        """
        params = {
            'fnc': 'ecograph',
            'act': 'hourdispScreen',
            'dispDay': target_date.strftime('%Y%m%d'),
            'searchid': site_id,
        }
        res = self._post(self.uri, params=params)
        soup = BeautifulSoup(res.text, 'xml')
        hatsuden = soup.hatsuden
        time_tags = hatsuden.find_all('time')
        hour = 0
        energy_series = dict()
        for time in time_tags:
            ts = datetime(target_date.year,
                          target_date.month,
                          target_date.day,
                          hour)
            val = try_parse_kwh(time.text)
            energy_series[ts.isoformat()] = val
            hour += 1
        return energy_series

    def get_daily_kwh(self, site_id: str, target_month: date):
        """Download daily energy generation for 1 month in kWh.

        Args:
            site_id (str) - Unique identifier for a PV system
            target_date (datetime.date) - Date for which to download data.
                The date portion of this object is ignored.
                Only the year and month are used.
        
        Returns:
            dict. Keys are timestamps in ISO format.
            Values are energy generation in kWh.
        """
        params = {
            'fnc': 'ecograph',
            'act': 'daydispScreen',
            'dispMonth': target_month.strftime('%Y%m'),
            'searchid': site_id,
        }
        res = self._post(self.uri, params=params)
        soup = BeautifulSoup(res.text, 'xml')
        hatsuden = soup.hatsuden
        time_tags = hatsuden.find_all('day')
        day = 1
        energy_series = dict()
        for time in time_tags:
            ts = date(target_month.year,
                      target_month.month,
                      day)
            val = try_parse_kwh(time.text)
            energy_series[ts.isoformat()] = val
            day += 1
        return energy_series
