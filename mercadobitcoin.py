import requests
import logging
import time
import pandas as pd

from requests.api import get
# from pandas.io.json import json_normalize

class Coin():

    def __init__(self) -> None:
        self.__coins = {
            "Bitcoin": "BTC",
            "BitcoinCash": "BCH",
            "Ethereum": "ETH",
            "XRP": "XRP"
        }

    @property
    def Bitcoin(self) -> str:
        return self.__coins['Bitcoin']

    @property
    def BitcoinCash(self) -> str:
        return self.__coins['BitcoinCash']

    @property
    def Ethereum(self) -> str:
        return self.__coins['Ethereum']

    @property
    def Xrp(self) -> str:
        return self.__coins['XRP']

    def get_all(self) -> dict:
        return self.__coins


class MercadoBitcoin():

    def __init__(self, coin: str = '') -> None:
        self._logger = logging.getLogger(__name__)
        self._coin = coin
        self._base_url_data = 'https://www.mercadobitcoin.net'
        self._request_path_data = 'api'
        self._methods = {"ticker": "ticker",
                         "orderbook": "orderbook",
                         "trades": "trades"}

    @property
    def coin(self) -> str:
        return self._coin

    @coin.setter
    def coin(self, coin):
        self._coin = coin

    @property
    def base_url_data(self) -> str:
        return self._base_url_data

    @base_url_data.setter
    def base_url_data(self, base_url_data):
        self._base_url_data = base_url_data

    @property
    def request_path_data(self) -> str:
        return self._request_path_data

    @request_path_data.setter
    def request_path_data(self, request_path_data):
        self._request_path_data = request_path_data


    @property
    def ticker(self) -> str:
        return self._methods['ticker']

    @property
    def orderbook(self) -> str:
        return self._methods['orderbook']

    @property
    def trades(self) -> str:
        return self._methods['trades']
    



    def get_ticker_cotation(self) -> dict:

        get_url = '/'.join((self.base_url_data,self.request_path_data,self.coin,self.ticker))
        response = requests.get(get_url)

        if response.status_code not in range(200, 299):
            self._logger.error("Ticker request not successfuly: {0}".format(response.status_code))

        results = response.json()['ticker']
        
        return results

    def dict_to_dataframe(self, data: dict) -> pd.DataFrame:
        
        df = pd.json_normalize(data)
        df.head()

        df = self.standardize_ticker_df(df)

        return df
        


    def standardize_ticker_df(self, df: pd.DataFrame) -> pd.DataFrame:

        # convert to numeric
        df['high'] = pd.to_numeric(df['high'])
        df['low'] = pd.to_numeric(df['low'])
        df['vol'] = pd.to_numeric(df['vol'])
        df['last'] = pd.to_numeric(df['last'])
        df['buy'] = pd.to_numeric(df['buy'])
        df['sell'] = pd.to_numeric(df['sell'])
        df['open'] = pd.to_numeric(df['open'])

        # convert to human date
        df['date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(df['date']))
        df['date'] = pd.to_datetime(df['date'])
        
        # add epoch date column
        df['date_epoch'] = df['date']

        return df


