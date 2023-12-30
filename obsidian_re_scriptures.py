import argparse
import os
import re
import shutil
import sys

from cached_content_downloader import CachedContentDownloader
from content_downloader import ContentDownloader
from file_io import CACHE_DIR
from html_loader import HtmlLoader
from html_parsers import get_chapter_title, get_breadcrumb_path
from md_generators import html_to_md
from predicates import is_toc, is_volume_toc, is_book_toc
from scriptures_client import ScripturesClient

TOC_PATHS = ['/scriptures/oc', '/scriptures/nc', '/scriptures/tc']


def main(args):
    args.output_dir = os.path.join(args.output_dir, 'Scriptures')

    content_loader = CachedContentDownloader(CACHE_DIR, HtmlLoader(), ContentDownloader(ScripturesClient()))

    material_paths = []
    for path in TOC_PATHS:
        material_paths.extend(content_loader.recursive_retrieve_html([path]))

    obsidian_link_by_path = {}
    obsidian_img_link_by_path = {}

    for path in material_paths:
        # Convert path to filename to retrieve the downloaded file
        soup = content_loader.retrieve_html(path)

        for img in soup.select('div.scriptureText img'):
            if not img.has_attr('src'):
                continue
            content_loader.retrieve_asset(img['src'])
            name = ".".join(img['src'].split("/")[1:])
            obsidian_img_link_by_path[img['src']] = os.path.join(args.output_dir, "assets", name)

        # Convert to markdown and save.
        if not is_toc(soup):
            breadcrumb_path = get_breadcrumb_path(soup)
            book_dir = os.path.join(args.output_dir, breadcrumb_path).replace("The ", "")
        elif is_volume_toc(soup):
            breadcrumb_path = get_chapter_title(soup)
            book_dir = os.path.join(args.output_dir, breadcrumb_path).replace("The ", "")
        elif is_book_toc(soup):
            breadcrumb_path = get_breadcrumb_path(soup) + "/" + get_chapter_title(soup)
            book_dir = os.path.join(args.output_dir, breadcrumb_path).replace("The ", "")
        else:
            raise SystemExit(f"Unknown HTML category for {path}.")

        if not os.path.exists(book_dir):
            os.makedirs(book_dir)

        # Note: / replacement is due to a glossary entry titled "Call/ed/ing"
        chap_title = get_chapter_title(soup).replace("/", "-")
        filepath = os.path.join(str(book_dir), chap_title + '.md')

        obsidian_link_by_path[path] = filepath
        if not path.strip()[-1].isdigit():
            obsidian_link_by_path[os.path.join(path, '/')] = filepath

    for path in material_paths:
        soup = content_loader.retrieve_html(path)
        filepath = obsidian_link_by_path[path]
        md = html_to_md(filepath, soup, obsidian_link_by_path, obsidian_img_link_by_path, args.rel_links, args.link_type)

        with open(filepath, "w+") as f:
            f.write(md)

    assets_dir = os.path.join(args.output_dir, 'assets')
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    for cache_file_path, obsidian_link in obsidian_img_link_by_path.items():
        shutil.copyfile(
            os.path.join(CACHE_DIR, ".".join(cache_file_path.split("/")[1:])),
            obsidian_link
        )

    if args.reading_list:
        reading_list = ""
        bullets = set()
        for path in material_paths:
            obsidian_link_wo_ext = ".".join(obsidian_link_by_path[path].split(".")[:-1])
            starting_path = re.sub(".*?Scriptures/", "", obsidian_link_wo_ext)
            for i, part in enumerate(starting_path.split("/")):
                indent = "    "*i
                bullet = indent + "- [ ] " + part + "\n"
                if bullet not in bullets:
                    bullets.add(bullet)
                    reading_list += bullet
        with open(os.path.join(args.output_dir, "Reading List.md"), "w+") as f:
            f.write(reading_list)



def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output-dir", default="output")
    parser.add_argument("--rel-links", action='store_true', default=False)
    parser.add_argument("--link-type", choices=('wikilinks', 'markdown'), default='wikilinks')
    parser.add_argument("--reading-list", action='store_true', default=False)
    return parser


def parse_args(args):
    return create_parser().parse_args(args)


if __name__ == "__main__":
    main(parse_args(sys.argv[1:]))
