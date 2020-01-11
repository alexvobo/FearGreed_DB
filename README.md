# FearGreed DB

This is a program that will populate a MySQL database with data from the following sources:

- [Crypto Fear & Greed Index](https://alternative.me/crypto/fear-and-greed-index/)
- [BTC Historical Data](https://min-api.cryptocompare.com/) - *API Key Required*

## Instructions
- Obtain API Key from Cryptocompare
  - Set the CRYPTOCOMPARE_KEY variable to your API key or add CRYPTOCOMPARE_KEY to system env variables
  - #### populate_db.py
    ```python
    def fetch_btc():
    ...
    ...
    url = 'https://min-api.cryptocompare.com/data/v2/histoday'

    # Change to your key here or set the key as an environment variable
    CRYPTOCOMPARE_KEY = os.environ.get('CRYPTOCOMPARE_KEY')

    
run populate_db.py in data folder. Fill config accordingly.
