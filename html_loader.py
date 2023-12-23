from bs4 import BeautifulSoup

from file_io import open_html


class HtmlLoader(object):
    def retrieve_html(self, path, dir):
        with open_html(path, dir) as f:
            return BeautifulSoup(f, "html.parser")
