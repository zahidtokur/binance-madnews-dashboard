import time
import urllib.parse
import hmac
import hashlib
import requests

from core.integrations.base.commands import BaseCommand
from core.service import PairService, AccountService


class GetPairs(BaseCommand):
    def __init__(self, integration, **kwargs):
        super().__init__(integration, **kwargs)
        self.request_method = "GET"
        self.pair_service = PairService()

    def get_url(self):
        return self.integration.base_url + "/fapi/v1/exchangeInfo"

    def send_request(self):
        response = requests.request(
            self.request_method, url=self.get_url())
        return response

    def process_response(self, response):
        response_data = response.json()
        pairs = response_data.get("symbols")
        if not pairs:
            return False

        pair_names = []
        for pair_data in pairs:
            name = pair_data.get("symbol")
            if name.endswith("USDT"):
                pair_names.append(name)
                qty_precision = pair_data.get("quantityPrecision")
                self.pair_service.update_or_create_pair(
                    self.integration.account, name, qty_precision)
        self.pair_service.delete_pairs(exclude_names=pair_names)
        return True


class UpdateBalance(BaseCommand):
    def __init__(self, integration, **kwargs):
        super().__init__(integration, **kwargs)
        self.request_method = "GET"
        self.account_service = AccountService()

    def get_url(self):
        return self.integration.base_url + "/fapi/v2/balance"

    def get_request_params(self):
        timestamp = int(round(time.time() * 1000)) - 1000
        params = {"timestamp": timestamp}
        message = urllib.parse.urlencode(params)
        secret_key = self.integration.conf.get('secret_key')
        signature = hmac.new(
            secret_key.encode(), msg=message.encode(),
            digestmod=hashlib.sha256).hexdigest()
        params.update({"signature": signature})
        return params

    def get_headers(self):
        return {
            "X-MBX-APIKEY": self.integration.conf["api_key"]
        }

    def send_request(self):
        response = requests.request(
            self.request_method, url=self.get_url(),
            params=self.get_request_params(),
            headers=self.get_headers())
        return response

    def process_response(self, response):
        response_data = response.json()
        if not isinstance(response_data, list):
            return False

        denominator = "USDT"
        asset_data = next(
            (r for r in response_data if r["asset"] == denominator), None)
        if not asset_data:
            return False

        self.account_service.update_balance(
            self.integration.account, asset_data.get("balance"))
        return True
