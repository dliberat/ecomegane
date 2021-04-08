# Eco-Megane Python Client

## About

The Eco-Megane online platform provides monitoring data for photovoltaic systems.
However, they do not offer an API or any convenient way of programmatically accessing the data. This client allows you to download certain data from the site using Python.

## Installation

To install the client using `pip`:

```
pip install ecomegane
```

## Getting Started

To begin downloading data, you will need to find your power plant's ID number on the Eco Megane site.

![Site ID](https://github.com/dliberat/ecomegane/raw/master/docs/img/site_id.png)

## Example Usage

For a complete sample, see `docs/sample.py`.

**Downloading hourly data**

```python
import datetime
from ecomegane import EcoMeganeClient

site_id = '00031234567'
today = datetime.date.today()

with EcoMeganeClient('username', 'password') as client:
    kwh = client.get_hourly_kwh(site_id, today)
    for timestamp, energy in kwh.items():
        print(timestamp, energy)
```


**Downloading daily data**

```python
import datetime
from ecomegane import EcoMeganeClient

site_id = '00031234567'
today = datetime.date.today()

with EcoMeganeClient('username', 'password') as client:
    # Download daily data for the current month.
    kwh = client.get_daily_kwh(site_id, today)
    for timestamp, energy in kwh.items():
        print(timestamp, energy)
```

## Contributing

PRs are welcome. Feel free to fork the repo, make your changes, and submit a PR. It is recommended that you create an Issue before starting work on your features.
