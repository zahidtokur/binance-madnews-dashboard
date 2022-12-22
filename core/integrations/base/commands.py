class BaseCommand():
    def __init__(self, integration, **kwargs):
        self.integration = integration

    def run(self):
        response = self.send_request()
        self.log_request(response)
        return self.process_response(response)

    def log_request(self, response):
        pass

    def send_request(self):
        raise NotImplementedError

    def process_response(self):
        raise NotImplementedError
