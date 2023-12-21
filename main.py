import os
import re

import markdownify
from bs4 import BeautifulSoup
import requests
import argparse

FRONT_BACK_MATTER = ["foreword", "canonization", "preface", "appendix", "introduction", "epigraph"]
BASE_URL = "https://scriptures.info"
TOC_PATHS = ['/scriptures/oc', '/scriptures/nc', '/scriptures/tc']
CACHE_DIR = "cache"
title_by_abv = {
    "oc": "Old Covenants",
    "nc": "New Covenants",
    "nt": "New Testament",
    "bofm": "Book of Mormon",
    "tc": "Teachings and Commandments",
}


def main(args):
    htmls = []

    material_paths = []
    if not args.use_cache:
        print("Downloading HTML for TOCs...")
        # Download HTML for each TOC page
        for toc_path in TOC_PATHS:
            htmls.append(download_html(toc_path, CACHE_DIR))

        # Extract paths to the material listed in each TOC
        for html in htmls:
            toc_soup = BeautifulSoup(html, "html.parser")
            material_paths.extend(get_material_paths(toc_soup))

        material_paths = download_material(material_paths, use_cache=False)
    else:
        for toc_path in TOC_PATHS:
            material_paths.extend(
                download_material(
                    get_material_paths(load_soup(toc_path)), use_cache=True))

    obsidian_link_by_path = {}
    # Load saved HTML for each path, convert to .md and save.
    for path in material_paths:
        soup = load_soup(path)
        # Note: / replacement is due to a glossary entry titled "Call/ed/ing"
        chap_title = get_chapter_title(soup).replace("/", "-")
        obsidian_link_by_path[path] = chap_title

    for path in material_paths:
        # Convert path to filename to retrieve the downloaded file
        soup = load_soup(path)

        # Gather metadata
        book_abv = path.split("/")[1:][1]
        book_dir = os.path.join(args.output_dir, get_breadcrumb_path(soup)).replace("The ", "")
        if not os.path.exists(book_dir):
            os.makedirs(book_dir)

        # Convert to markdown and save.
        md = html_to_md(soup, obsidian_link_by_path)
        with open(os.path.join(str(book_dir), obsidian_link_by_path[path] + '.md'), "w+") as f:
            f.write(md)


def download_material(paths, i=0, use_cache=False):
    i += 1
    if i > 10:
        return []
    # Download HTML for all materials
    verified_paths = []
    for path in paths:
        if not use_cache:
            print("Downloading HTML for all material...")
            html = download_html(path, CACHE_DIR)
            soup = BeautifulSoup(html, 'html.parser')
        else:
            print("Loading HTML from cache for all material...")
            soup = load_soup(path)
        if not is_toc(soup):
            verified_paths.append(path)
        if is_toc(soup):
            verified_paths.extend(download_material(get_material_paths(soup), i=i, use_cache=use_cache))
    return verified_paths

def is_toc(soup):
    chapter_paths = get_chapter_paths(soup)
    return len(chapter_paths) > 0


def load_soup(path):
    # Convert path to filename to retrieve the downloaded file
    basename = ".".join(path.split("/")[1:])
    with open(os.path.join(CACHE_DIR, basename + '.html'), "r") as f:
        return BeautifulSoup(f, "html.parser")


def get_chapter_title(soup: BeautifulSoup):
    breadcrumb = soup.find("div", class_="navBreadcrumb")
    return breadcrumb.find_all("li")[-1].get_text(" ", strip=True)


def get_breadcrumb_path(soup: BeautifulSoup):
    breadcrumb = soup.find("div", class_="navBreadcrumb")
    return "/".join([a.get_text(" ", strip=True) for a in breadcrumb.find_all("a")][1:])


def html_to_md(soup, obsidian_link_by_path):
    print("Converting HTML to MD...")
    text_soup = soup.find('div', id='scriptureText')

    for sup in text_soup.find_all('sup', text="*"):
        sup.insert(0, '\\')

    # Replace anchor text with obsidian links
    for a in text_soup.find_all('a'):
        if a and a.has_attr('href'):
            # Assures chapter link instead of chapter + verse link
            href = re.sub("/$", "", a['href'].split('.')[0])
            if href in obsidian_link_by_path:
                new_tag = soup.new_tag("div")
                pipe = "\\|" if a.find_parent("td") else "|"
                new_tag.string = f"[[{obsidian_link_by_path[href]}{pipe}{a.text}]]"
                a.replace_with(new_tag)

    for i in range(1, 7):
        for h in text_soup.find_all(f'h{i}'):
            h.insert(0, "#"*i + " ")

    for p in text_soup.find_all('p'):
        sibling = p.find_next_sibling()
        if p.text.isspace() or p.text.endswith("\n") or not sibling or (sibling.name == 'p' and sibling.text.isspace()):
            continue
        p.append('\n')

    for i in text_soup.find_all("i"):
        i.insert(0, "**")
        i.append("**")

    for b in text_soup.find_all("b"):
        b.insert(0, "*")
        b.append("*")

    for li in text_soup.find_all('li'):
        if not li.has_attr('id'):
            continue
        verse_num = li['id']
        li.insert(0, f'###### {verse_num}\n')
        li.append('\n')

    for table in text_soup.find_all('table'):
        md_table = markdownify.MarkdownConverter().convert_soup(table)
        table.replace_with(md_table)

    return text_soup.get_text().strip()

def download_html(material_path, dirr):
    response = requests.get(BASE_URL + material_path)
    if not response.ok:
        return None
    with open(os.path.join(dirr, ".".join(material_path.split("/")[1:])) + ".html", "w+") as f:
        f.write(response.text)
    return response.text


def get_chapter_paths(toc_soup):
    return [li.a['href'] for li in toc_soup.find_all('li', class_='chapter') if li]


def get_info_paths(toc_soup):
    return [a['href'] for a in toc_soup.select("div.navigationText.multicolumn")[0].find_all('a')]


def get_material_paths(toc_soup: BeautifulSoup):
    paths = []
    for a in toc_soup.find_all('a', href=True):
        # Get front matter, back matter, and books (OT, NT, BoM)
        if len(a.select('.bookLink')):
            paths.append(a['href'])
        # Get sections/chapters
        elif a.parent and a.parent.has_attr('class') and 'chapter' in a.parent.attrs['class']:
            paths.append(a['href'])
    return paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", nargs="+")
    parser.add_argument("-u", "--url", nargs="+")
    parser.add_argument("-o", "--output-dir", default="output")
    parser.add_argument("-c", "--use-cache", action="store_true")

    args = parser.parse_args()
    main(args)
