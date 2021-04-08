import datetime
from ecomegane import EcoMeganeClient

site_id = '00031234567'
today = datetime.date.today()

with EcoMeganeClient('username', 'password') as client:
    # Download hourly data for the current day.
    kwh = client.get_hourly_kwh(site_id, today)
    for timestamp, energy in kwh.items():
        print(timestamp, energy)

    # Download daily data for the current month.
    kwh = client.get_daily_kwh(site_id, today)
    for timestamp, energy in kwh.items():
        print(timestamp, energy)
