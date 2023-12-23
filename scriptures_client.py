import requests


class ScripturesClient(object):
    BASE_URL = "https://scriptures.info"

    def stream(self, path):
        return requests.get(ScripturesClient.BASE_URL + path, stream=True)

    def request(self, path):
        return requests.get(ScripturesClient.BASE_URL + path)
