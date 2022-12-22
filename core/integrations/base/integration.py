class BaseIntegration():
    def __init__(self, account, conf):
        self.account = account
        self.conf = conf

    def run_command(self, command_key):
        raise NotImplementedError
