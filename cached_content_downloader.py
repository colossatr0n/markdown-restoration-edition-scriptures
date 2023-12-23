import os

from content_downloader import ContentDownloader
from html_loader import HtmlLoader
from html_parsers import get_paths
from file_io import html_path_to_filename
from predicates import is_toc


class CachedContentDownloader(object):
    def __init__(self,
                 cache_dir,
                 html_loader: HtmlLoader,
                 content_downloader: ContentDownloader,
                 ):
        self.html_loader = html_loader
        self.content_downloader = content_downloader
        self.cache = set()
        self.cache_dir = cache_dir

        for rel_path in os.listdir(cache_dir):
            self.cache.add(rel_path)

    def retrieve_html(self, material_path):
        if self._is_cached(material_path, '.html'):
            print(f"Loading cached HTML for {material_path}...")
            return self.html_loader.retrieve_html(material_path, self.cache_dir)
        print(f"Downloading HTML for {material_path}...")
        soup = self.content_downloader.retrieve_html(material_path, self.cache_dir)
        self._add(material_path)
        return soup

    def retrieve_asset(self, path):
        if self._is_cached(path):
            print(f"Asset found in cache: {path}")
            return True
        print(f"Downloading asset: {path}")
        was_downloaded = self.content_downloader.retrieve_asset(path)
        self._add(path)
        return was_downloaded

    def recursive_retrieve_html(self, paths, i=0):
        i += 1
        if i > 10:
            return []
        # Download HTML for all materials
        all_paths = []
        all_paths.extend(paths)
        for path in paths:
            soup = self.retrieve_html(path)
            if is_toc(soup):
                additional_paths = self.recursive_retrieve_html(get_paths(soup), i=i)
                all_paths.extend(additional_paths)
        return all_paths

    def _is_cached(self, path, ext=""):
        return html_path_to_filename(path) + ext in self.cache

    def _add(self, path):
        self.cache.add(html_path_to_filename(path))
