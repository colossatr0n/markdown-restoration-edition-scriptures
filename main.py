import argparse
import os
import shutil
import sys

from cached_content_downloader import CachedContentDownloader
from content_downloader import ContentDownloader
from file_io import CACHE_DIR
from html_loader import HtmlLoader
from html_parsers import get_chapter_title, get_breadcrumb_path
from md_generators import material_html_to_md, toc_html_to_md
from predicates import is_toc, is_volume_toc, is_book_toc
from scriptures_client import ScripturesClient

TOC_PATHS = ['/scriptures/oc', '/scriptures/nc', '/scriptures/tc']


def main(args):
    args.output_dir = os.path.join(args.output_dir, 'Scriptures')

    content_loader = CachedContentDownloader(
        CACHE_DIR, HtmlLoader(), ContentDownloader(ScripturesClient())
    )

    material_paths = []
    material_paths = content_loader.recursive_retrieve_html(TOC_PATHS)

    material_paths.extend(TOC_PATHS)
    obsidian_link_by_path = {}
    obsidian_img_link_by_path = {}

    # Load saved HTML for each path, convert to .md and save.
    for path in material_paths:
        soup = content_loader.retrieve_html(path)
        # Note: / replacement is due to a glossary entry titled "Call/ed/ing"
        chap_title = get_chapter_title(soup).replace("/", "-")
        obsidian_link_by_path[path] = chap_title
        images = [img for img in soup.select('div.scriptureText img')]
        for img in images:
            if not img.has_attr('src'):
                continue
            content_loader.retrieve_asset(img['src'])
            name = ".".join(img['src'].split("/")[1:])
            obsidian_img_link_by_path[img['src']] = name

    for path in material_paths:
        # Convert path to filename to retrieve the downloaded file
        soup = content_loader.retrieve_html(path)

        # Convert to markdown and save.
        if not is_toc(soup):
            breadcrumb_path = get_breadcrumb_path(soup)
            md = material_html_to_md(soup, obsidian_link_by_path, obsidian_img_link_by_path)
        elif is_volume_toc(soup):
            breadcrumb_path = get_chapter_title(soup)
            md = toc_html_to_md(soup, obsidian_link_by_path, obsidian_img_link_by_path)
        elif is_book_toc(soup):
            breadcrumb_path = get_breadcrumb_path(soup) + "/" + get_chapter_title(soup)
            md = toc_html_to_md(soup, obsidian_link_by_path, obsidian_img_link_by_path)

        # Gather metadata
        book_dir = os.path.join(args.output_dir, breadcrumb_path).replace("The ", "")
        if not os.path.exists(book_dir):
            os.makedirs(book_dir)

        with open(os.path.join(str(book_dir), obsidian_link_by_path[path] + '.md'), "w+") as f:
            f.write(md)

    assets_dir = os.path.join(args.output_dir, 'assets')
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    for cache_file_path, obsidian_link in obsidian_img_link_by_path.items():
        shutil.copyfile(
            os.path.join(CACHE_DIR, ".".join(cache_file_path.split("/")[1:])),
            os.path.join(assets_dir, obsidian_link)
        )


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", nargs="+")
    parser.add_argument("-u", "--url", nargs="+")
    parser.add_argument("-o", "--output-dir", default="output")
    parser.add_argument("-c", "--use-cache", action="store_true")
    return parser


def parse_args(args):
    return create_parser().parse_args(args)


if __name__ == "__main__":
    main(parse_args(sys.argv[1:]))
