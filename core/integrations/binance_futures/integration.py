from collections import OrderedDict

from core.integrations.base.integration import BaseIntegration
from core.integrations.binance_futures.commands import GetPairs, UpdateBalance


class Integration(BaseIntegration):
    commands = OrderedDict([
        ('get_pairs', GetPairs),
        ('update_balance', UpdateBalance),
    ])

    @property
    def base_url(self):
        base_url = self.conf.get("base_url", None)
        return base_url or "https://fapi.binance.com"

    def run_command(self, command_key, **kwargs):
        command_class = self.commands.get(command_key, None)
        if not command_class:
            return False
        command = command_class(self, **kwargs)
        status = command.run()
        return status
