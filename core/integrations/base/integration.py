class BaseIntegration():
    def __init__(self, account):
        self.account = account

    def run_command(self, command_key):
        raise NotImplementedError
