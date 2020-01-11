# FearGreed DB

This is a program that will populate a MySQL database with data from the following sources:

- [Crypto Fear & Greed Index](https://alternative.me/crypto/fear-and-greed-index/)
- [BTC Historical Data](https://min-api.cryptocompare.com/) - *API Key Required*

## Instructions
- Install MySQL (hosted DB coming soon...)
  - #### config.ini - Add DB info
- Obtain API Key from Cryptocompare
  - Set the CRYPTOCOMPARE_KEY variable to your API key or add CRYPTOCOMPARE_KEY to system env variables
  - #### populate_db.py
    ```python
    def fetch_btc():
    ...
    ...
    url = 'https://min-api.cryptocompare.com/data/v2/histoday'

    # Change 'YOUR-KEY-HERE' to your API key
    CRYPTOCOMPARE_KEY = os.environ.get('CRYPTOCOMPARE_KEY', 'YOUR-KEY-HERE')
- Run `populate_db.py`
 - #### populate_db.py - Comment out code after first run
  ```python
  if __name__ == '__main__':
    '''Contains necessary functions to maintain DB'''

    from data.models import create_tables <--- add # to beginning of line

    create_tables() <--- add # to beginning of line

