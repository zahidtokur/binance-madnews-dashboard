from collections import OrderedDict

from core.integrations.base.integration import BaseIntegration


class Integration(BaseIntegration):
    commands = OrderedDict([
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
