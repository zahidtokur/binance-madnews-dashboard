import os
import requests_mock
import json
from decimal import Decimal

from django.test import TestCase

from core.models import Account, Pair
from core.integrations.binance_futures.integration import Integration


class BinanceTestCase(TestCase):
    def setUp(self):
        self.conf = {"secret_key": "ZSkpmbCakXGfZX9VlpiXsDEuEVtSWq7bz2Knc6WSt83qZ1QXmItAZ3cf1eZXBP9q",
                     "api_key": "CckRDAh2RUTrBWnOZt1NLJI0ck9j1YT3B9hr4W4X6JUgPIFDZ9M2pzbD2ORqyPfT"}
        self.account = Account.objects.create(
            name='Binance Test', conf=self.conf)

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
        i = Integration(self.account, self.conf)
        m.register_uri("GET", requests_mock.ANY,
                       json=self.load_response_file("get_pairs_response"))

        self.assertEqual(Pair.objects.count(), 0)
        i.run_command("get_pairs")
        self.assertEqual(Pair.objects.filter(
            account=self.account).count(), 154)

    @requests_mock.mock()
    def test_update_balance(self, m):
        i = Integration(self.account, self.conf)
        m.register_uri("GET", requests_mock.ANY,
                       json=self.load_response_file("update_balance_response"))

        self.assertEqual(self.account.balance, 0)
        i.run_command("update_balance")
        self.assertEqual(self.account.balance, Decimal("200.07"))
