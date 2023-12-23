from bs4 import BeautifulSoup

from file_io import save_html, save_image
from scriptures_client import ScripturesClient


class ContentDownloader(object):
    def __init__(self, client: ScripturesClient):
        self.scriptures_client = client

    def retrieve_asset(self, path, dirr):
        response_stream = self.scriptures_client.stream(path)
        if not response_stream.ok:
            return False
        save_image(response_stream, path, dirr)
        return True

    def retrieve_html(self, material_path, dir):
        response = self.scriptures_client.request(material_path)
        if not response.ok:
            return None
        save_html(response.text, material_path, dir)
        return BeautifulSoup(response.text, 'html.parser')


