import requests

from core.integrations.base.commands import BaseCommand
from core.service import PairService


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
                    self.integration.exchange, name, qty_precision)
        self.pair_service.delete_pairs(exclude_names=pair_names)
        return True
