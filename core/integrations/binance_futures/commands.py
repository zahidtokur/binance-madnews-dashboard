import time
import urllib.parse
import hmac
import hashlib
import requests
from decimal import Decimal

from core.models import Pair
from core.integrations.base.commands import BaseCommand, BaseBulkCommand
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


class SetCrossMargin(BaseBulkCommand):
    def __init__(self, integration, objects, **kwargs):
        super().__init__(integration, **kwargs)
        self.request_method = "POST"
        self.objects = objects

    def get_url(self):
        return self.integration.base_url + "/fapi/v1/marginType"

    def get_headers(self):
        return {
            "X-MBX-APIKEY": self.integration.conf["api_key"]
        }

    def get_request_data(self, object):
        request_data = {
            "timestamp": int(round(time.time() * 1000)) - 1000,
            "recvWindow": 20000,
            "symbol": object.name,
            "marginType": "CROSSED"}

        message = urllib.parse.urlencode(request_data)
        secret_key = self.integration.conf.get('secret_key')
        signature = hmac.new(
            secret_key.encode(), msg=message.encode(),
            digestmod=hashlib.sha256).hexdigest()
        request_data.update({"signature": signature})
        return request_data

    def send_request(self, object):
        response = requests.request(
            self.request_method, url=self.get_url(),
            data=self.get_request_data(object), headers=self.get_headers())
        return response

    def process_response(self, response):
        return response.json()


class GetBrackets(BaseCommand):
    def __init__(self, integration, **kwargs):
        super().__init__(integration, **kwargs)
        self.request_method = "GET"

    def get_url(self):
        return self.integration.base_url + "/fapi/v1/leverageBracket"

    def get_headers(self):
        return {
            "X-MBX-APIKEY": self.integration.conf["api_key"]
        }

    def get_request_params(self):
        request_data = {
            "timestamp": int(round(time.time() * 1000)) - 1000,
            "recvWindow": 20000
        }

        message = urllib.parse.urlencode(request_data)
        secret_key = self.integration.conf.get('secret_key')
        signature = hmac.new(
            secret_key.encode(), msg=message.encode(),
            digestmod=hashlib.sha256).hexdigest()
        request_data.update({"signature": signature})
        return request_data

    def send_request(self):
        response = requests.request(
            self.request_method, url=self.get_url(),
            params=self.get_request_params(), headers=self.get_headers())
        return response

    def process_response(self, response):
        response_data = response.json()
        if isinstance(response_data, list):
            return response_data
        return []


class SetLeverage(BaseBulkCommand):
    def __init__(self, integration, objects, **kwargs):
        super().__init__(integration, **kwargs)
        self.request_method = "POST"
        self.objects = objects
        balance = self.integration.account.balance
        self.max_position_size = balance * 3

    def get_url(self):
        return self.integration.base_url + "/fapi/v1/leverage"

    def get_headers(self):
        return {
            "X-MBX-APIKEY": self.integration.conf["api_key"]
        }

    def get_request_data(self, object, leverage):
        request_data = {
            "timestamp": int(round(time.time() * 1000)) - 1000,
            "recvWindow": 20000,
            "symbol": object.name,
            "leverage": leverage}

        message = urllib.parse.urlencode(request_data)
        secret_key = self.integration.conf.get('secret_key')
        signature = hmac.new(
            secret_key.encode(), msg=message.encode(),
            digestmod=hashlib.sha256).hexdigest()
        request_data.update({"signature": signature})
        return request_data

    def send_request(self, object, leverage):
        response = requests.request(
            self.request_method, url=self.get_url(),
            data=self.get_request_data(object, leverage), headers=self.get_headers())
        return response

    def process_response(self, response):
        return response.json()

    def run(self):
        bracket_data = self.integration.run_command("get_brackets")
        for item in bracket_data:
            try:
                symbol = self.objects.get(name=item["symbol"])
                for bracket in item["brackets"]:
                    if Decimal(bracket["notionalCap"]) > self.max_position_size:
                        leverage = bracket["initialLeverage"]
                        break
            except Pair.DoesNotExist:
                continue

            response = self.send_request(symbol, leverage)
            self.log_request(response)
            self.process_response(response)

        return True


class GetPairPrice(BaseCommand):
    def __init__(self, integration, pair, **kwargs):
        super().__init__(integration, **kwargs)
        self.request_method = "GET"
        self.pair_service = PairService()
        self.pair = self.pair_service.get_pair_object(pair)

    def get_request_params(self):
        return {
            "symbol": self.pair.name
        }

    def get_url(self):
        return self.integration.base_url + "/fapi/v1/ticker/price"

    def send_request(self):
        response = requests.request(
            self.request_method, url=self.get_url(),
            params=self.get_request_params())
        return response

    def process_response(self, response):
        response_data = response.json()
        return Decimal(response_data.get("price"))


class CreateOrder(BaseCommand):
    def __init__(self, integration, order_params, **kwargs):
        super().__init__(integration, **kwargs)
        self.request_method = "POST"
        self.order_params = order_params

    def get_url(self):
        return self.integration.base_url + "/fapi/v1/order"

    def get_headers(self):
        return {
            "X-MBX-APIKEY": self.integration.conf["api_key"]
        }

    def get_request_data(self):
        request_data = {
            "timestamp": int(round(time.time() * 1000)) - 2000,
            "recvWindow": 20000,
            "symbol": self.order_params["pair"],
            "side": self.order_params.get("side") or "BUY",
            "type": self.order_params["type"],
            "newOrderRespType": "RESULT"}

        if self.order_params["type"] == "MARKET":
            request_data.update(
                {"quantity": str(self.order_params["quantity"])})

        message = urllib.parse.urlencode(request_data)
        secret_key = self.integration.conf.get('secret_key')
        signature = hmac.new(
            secret_key.encode(), msg=message.encode(),
            digestmod=hashlib.sha256).hexdigest()
        request_data.update({"signature": signature})
        return request_data

    def send_request(self):
        response = requests.request(
            self.request_method, url=self.get_url(),
            data=self.get_request_data(), headers=self.get_headers())
        return response

    def process_response(self, response):
        response_data = response.json()
        if not response_data.get("orderId"):
            return False
        return response_data
