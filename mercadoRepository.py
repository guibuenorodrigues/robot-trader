import logging
import requests
from ticker import Ticker


class MercadoRepository():

    def __init__(self, base_url: str, request_path: str) -> None:
        self.logger = logging.getLogger(__name__)
        self.base_url = base_url
        self.request_path = request_path

    def get_ticker_cotation(self, coin: str) -> Ticker:

        try:
            url = "/".join((self.base_url, self.request_path, coin, 'ticker'))
            response = requests.get(url)

            if response.status_code not in range(200, 299):
                self.logger.error(
                    "Ticker request not in range between 200 and 299")
                raise Exception(
                    "Ticker request not in range between 200 and 299")

            results = response.json()['ticker']

            return Ticker(results)

        except Exception as e:
            self.logger.error(e)
            raise
