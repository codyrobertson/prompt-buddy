import langchain

class LangchainClient:
    def __init__(self):
        self.client = langchain.LanguageClient()

    def analyze(self, prompt):
        response = self.client.analyze(prompt)
        return response

    def suggest(self, prompt):
        response = self.client.suggest(prompt)
        return response