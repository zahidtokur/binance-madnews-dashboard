import os
import requests_mock
import json
from decimal import Decimal

from django.test import TestCase

from core.models import Account, Pair
from core.integrations.binance_futures.integration import Integration
from core.resources.service import OrderService


class BinanceTestCase(TestCase):
    def setUp(self):
        self.account = Account.objects.create(
            name='Binance Test', secret_key="secretkeyforbinancefutures", api_key="apikeyforbinancefutures")
        self.order_service = OrderService()

    def load_response_file(self, filename, extension="json"):
        dir_path = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(
                dir_path,
                'responses/{0}.{1}'.format(
                    filename, extension))) as f:
            if extension == 'json':
                return json.load(f)
            return f.read()

    @requests_mock.mock()
    def test_get_pairs(self, m):
        i = Integration(self.account)
        m.register_uri("GET", requests_mock.ANY,
                       json=self.load_response_file("get_pairs_response"))

        self.assertEqual(Pair.objects.count(), 0)
        i.run_command("get_pairs")
        self.assertEqual(Pair.objects.filter(
            account=self.account).count(), 154)

    @requests_mock.mock()
    def test_update_balance(self, m):
        i = Integration(self.account)
        m.register_uri("GET", requests_mock.ANY,
                       json=self.load_response_file("update_balance_response"))

        self.assertEqual(self.account.balance, 0)
        i.run_command("update_balance")
        self.assertEqual(self.account.balance, Decimal("200.07"))

    @requests_mock.mock()
    def test_get_pair_price(self, m):
        i = Integration(self.account)
        pair = Pair.objects.create(
            account=self.account, name='SOLUSDT', quantity_precision=0)
        m.register_uri("GET", requests_mock.ANY,
                       json=self.load_response_file("get_pair_price_response"))
        result = i.run_command("get_pair_price", pair=pair)
        self.assertEqual(result, Decimal("14.7180"))

    @requests_mock.mock()
    def test_create_order(self, m):
        i = Integration(self.account)
        pair = Pair.objects.create(
            account=self.account, name='SOLUSDT', quantity_precision=0)
        quantity = self.order_service.calculate_quantity(
            notional_size=Decimal("500"),
            price=Decimal("14.7180"),
            precision=pair.quantity_precision)
        order_params = {
            "pair": pair.name,
            "side": "BUY",
            "type": "MARKET",
            "quantity": quantity}
        m.register_uri("POST", requests_mock.ANY,
                       json=self.load_response_file("new_order_response"))
        result = i.run_command("create_order", order_params=order_params)
        self.assertNotEqual(result, False)
