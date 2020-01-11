from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from configparser import ConfigParser
import os
import requests
import pandas as pd
import pymysql
import pymysql.cursors


def read_db_config(filename='config.ini', section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    print("Reading DB config...")
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db


def fetch_btc():
    """Obtain API key from environment var. Obtain and package data received from CryptoCompare
    :param: None
    :return: dataframe with API data
    """
    print("Fetching BTC data from CryptoCompare...")

    url = 'https://min-api.cryptocompare.com/data/v2/histoday'

    CRYPTOCOMPARE_KEY = os.environ.get('CRYPTOCOMPARE_KEY', 'YOUR-KEY-HERE')

    assert CRYPTOCOMPARE_KEY != 'YOUR-KEY-HERE'

    parameters = {
        'fsym': 'BTC',
        'tsym': 'USDT',
        'allData': 'true',
        'limit': 2000
    }
    headers = {
        'authorization': f'Apikey {CRYPTOCOMPARE_KEY}'
    }

    try:
        response = requests.get(url, headers=headers, params=parameters)
        data = response.json()
        print(data)
        df = pd.DataFrame(data['Data']['Data'])
        df = df[['time', 'open', 'high', 'low', 'close', 'volumeto']]
        df = df.rename(
            columns={"time": "Time", "open": "Open", "high": "High", "low": "Low", "close": "Close",
                     "volumeto": "Volume"})
        df['Date'] = pd.to_datetime(df['Time'], unit='s').dt.normalize()
        print(df.tail())
        return df
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def fetch_fg():
    """Obtain and package data received from Fear & Greed API
    :param: None
    :return: dataframe with API data
    """

    print("Fetching FearGreed data from Alternative.Me...")

    url = 'https://api.alternative.me/fng/'

    parameters = {
        'limit': 0
    }

    try:
        response = requests.get(url, params=parameters)
        data = response.json()
        print(data)
        df = pd.DataFrame(data['data'])
        df = df[['value', 'value_classification', 'timestamp']]
        df['date'] = pd.to_datetime(df['timestamp'], unit='s').dt.normalize()
        print(df.tail())
        return df
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def is_empty(df):
    """Obtain and package data received from Fear & Greed API
    :param df: dataframe object or None
    :return: True if empty, False if exists
    """

    if df is None:
        print("None\n")
        return True
    else:
        print("Not empty\n")
        return df.empty


def update_db(btc=None, fg=None):
    """Read config & connect to MySQL database.
        If param(s) is/are specified then it will take the dataframe object and add data to the respective table.
    :param (optional) btc: accepts 'btc=[dataframe object]'
    :param (optional)  fg: accepts 'fg=[dataframe object]'
    :return: Exception e if there is an error writing to the db
    """

    print('Connecting to MySQL database...')
    db_config = read_db_config()
    connection = pymysql.connect(**db_config)

    try:

        if not is_empty(btc):
            print("Updating BTC data...")
            with connection.cursor() as cursor:
                dump = "TRUNCATE btc_data"
                cursor.execute(dump)
                for i, j in btc.iterrows():
                    sql = "INSERT INTO `btc_data` (`index`,`timestamp`,`date`,`open`,`high`,`low`,`close`,`volume`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
                    cursor.execute(sql,
                                   (i, j.Time, str(j.Date), j.Open, j.High, j.Low, j.Close, j.Volume))
                    # connection is not autocommit by default. So you must commit to save your changes.
                    connection.commit()

        if not is_empty(fg):
            print("Updating FearGreed data...")
            with connection.cursor() as cursor:
                dump = "TRUNCATE feargreed"
                cursor.execute(dump)
                for i, j in fg.iterrows():
                    sql = "INSERT INTO `feargreed` (`index`,`timestamp`,`date`,`classification`,`value`) VALUES (%s,%s,%s,%s,%s);"
                    cursor.execute(sql,
                                   (i, j.timestamp, str(j.date), j.value_classification, j.value))
                    # connection is not autocommit by default. So you must commit to save your changes.
                    connection.commit()
    except Exception as e:
        print(e)
    finally:
        connection.close()


if __name__ == '__main__':
    '''Contains necessary functions to maintain DB'''
    # from data.models import create_table
    # create_table()

    btc_data = fetch_btc()
    fg_data = fetch_fg()

    update_db(btc_data, fg_data)
