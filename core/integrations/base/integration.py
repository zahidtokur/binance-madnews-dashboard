class BaseIntegration():
    def __init__(self, exchange, conf):
        self.exchange = exchange
        self.conf = conf

    def run_command(self, command_key):
        raise NotImplementedError
