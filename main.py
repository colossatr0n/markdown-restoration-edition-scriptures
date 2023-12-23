import os
import re
import shutil

import markdownify
from bs4 import BeautifulSoup
import requests
import argparse

FRONT_BACK_MATTER = ["foreword", "canonization", "preface", "appendix", "introduction", "epigraph"]
BASE_URL = "https://scriptures.info"
# TOC_PATHS = ['/scriptures/tc']
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
    args.output_dir = os.path.join(args.output_dir, 'Scriptures')

    material_paths = []
    asset_paths = []
    if not args.use_cache:
        print("Downloading HTML for TOCs...")
        # Download HTML for each TOC page
        for toc_path in TOC_PATHS:
            response = download_html(toc_path, CACHE_DIR)
            htmls.append(response.text)

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

    material_paths.extend(TOC_PATHS)
    obsidian_link_by_path = {}
    obsidian_img_link_by_path = {}
    # Load saved HTML for each path, convert to .md and save.
    for path in material_paths:
        soup = load_soup(path)
        # Note: / replacement is due to a glossary entry titled "Call/ed/ing"
        chap_title = get_chapter_title(soup).replace("/", "-")
        obsidian_link_by_path[path] = chap_title
        images = [img for img in soup.select('div.scriptureText img')]
        for img in images:
            if not img.has_attr('src'):
                continue
            download_asset(img['src'], CACHE_DIR)
            name = ".".join(img['src'].split("/")[1:])
            obsidian_img_link_by_path[img['src']] = name

    for path in material_paths:
        # Convert path to filename to retrieve the downloaded file
        soup = load_soup(path)

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


def download_material(paths, i=0, use_cache=False):
    i += 1
    if i > 10:
        return []
    # Download HTML for all materials
    verified_paths = []
    for path in paths:
        if not use_cache:
            print("Downloading HTML for all material...")
            response = download_html(path, CACHE_DIR)
            # # TODO test this on OC TOC for the book of esther. TOC path will be different than response.url path.
            # path = re.sub(".*?info", "", response.url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
        else:
            print("Loading HTML from cache for all material...")
            soup = load_soup(path)
        # if not is_toc(soup):
        verified_paths.append(path)
        if is_toc(soup):
            verified_paths.extend(download_material(get_material_paths(soup), i=i, use_cache=use_cache))
    return verified_paths


def download_assets(paths, use_cache=False):
    for path in paths:
        if not use_cache:
            print("Downloading images...")
            download_asset(path)

        exit()


def download_asset(path, dirr):
    basename = ".".join(path.split("/")[1:])
    if basename in os.listdir(dirr):
        return True

    response = requests.get(BASE_URL + path, stream=True)
    if not response.ok:
        return False
    with open(os.path.join(dirr, basename), 'wb+') as f:
        for chunk in response:
            f.write(chunk)
    return True


def is_toc(soup):
    return len(get_book_links(soup)) > 0 or len(get_chapter_paths(soup)) > 0


def is_volume_toc(soup):
    return len(get_book_links(soup)) > 0


def is_book_toc(soup):
    return len(get_chapter_paths(soup)) > 0


def get_book_links(soup):
    return [book_link for book_link in soup.find_all(class_='bookLink') if book_link]

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


def general_html_to_md(soup, obsidian_link_by_path, obsidian_img_link_by_path):
    for sup in soup.find_all('sup', text="*"):
        sup.insert(0, '\\')

    # Replace anchor text with obsidian links
    for a in soup.find_all('a'):
        if a and a.has_attr('href'):
            # Assures chapter link instead of chapter + verse link
            href = re.sub("/$", "", a['href'].split('.')[0])
            new_tag = soup.new_tag("div")
            text = a.text
            pipe = "\\|" if a.find_parent("td") else "|"

            # Book TOCs use digits for the anchor text. Use the obsidian link instead by removing the alias.
            if a.parent.has_attr('class') and 'chapter' in a.parent['class']:
                pipe = ''
                text = ''

            if href in obsidian_link_by_path:
                new_tag.string = f"[[{obsidian_link_by_path[href]}{pipe}{text}]]"
                a.replace_with(new_tag)
            elif href.startswith("#"):
                if a.has_attr('class') and 'accordion-toggle' in a['class']:
                    continue
                new_tag.string = f"[[{href}{pipe}{text}]]"
                a.replace_with(new_tag)

    for img in soup.find_all('img'):
        if not img.has_attr('src') or not img['src'] in obsidian_img_link_by_path:
            continue
        div = soup.new_tag('div')
        div.string = "![[" + obsidian_img_link_by_path[img['src']] + "]]"
        img.insert_after(div)

    # Convert headers
    for i in range(1, 7):
        for h in soup.find_all(f'h{i}'):
            if h.parent.name != 'a':
                remove_newlines_and_space(h)
                h.insert(0, "#" * i + " ")

    for p in soup.find_all('p'):
        sibling = p.find_next_sibling()
        if p.text.isspace() or p.text.endswith("\n") or not sibling or (sibling.name == 'p' and sibling.text.isspace()):
            continue
        p.append('\n')

    for i in soup.find_all("i"):
        i.insert(0, "*")
        i.append("*")

    for b in soup.find_all("b"):
        b.insert(0, "**")
        b.append("**")

    for table in soup.find_all('table'):
        md_table = markdownify.MarkdownConverter().convert_soup(table)
        table.replace_with(md_table)

    for blockquote in soup.find_all('blockquote'):
        bq = markdownify.MarkdownConverter().process_tag(blockquote, False, False)
        blockquote.replace_with(bq)

    return soup



def material_html_to_md(soup, obsidian_link_by_path, obsidian_img_link_by_path):
    print("Converting HTML to MD...")
    text_soup = soup.find('div', class_='scriptureText')
    strip(text_soup)
    # Add controls to top of page.
    controls = soup.find(class_='prevNextSection')
    if controls:
        remove_newlines_and_space(controls)
        anchors = controls.find_all('a')
        for a in anchors:
            if a.has_attr("class") and a.has_attr('href'):
                href = a['href']
                span = soup.new_tag('span')
                span.append("  |  ")
                if 'prevBtn' in a['class']:
                    a.string = '<< '
                    a.insert_after(span)
                if 'nextBtn' in a['class']:
                    a.string = ' >>'
                    a.insert_before(span)
                # there was a path that was
                if href not in obsidian_link_by_path:
                    continue
                    # href = "/".join(href.split("/")[:-1])
                    # if href[-1].isalpha():
                    #     href = href + "/1"
                    # elif href[-1].endswith("/"):
                    #     href = href + "1"
                    # elif href[-1].isdigit():
                    #     href = href[:-2]
                obsidian_link = obsidian_link_by_path[href]
                if 'prevBtn' in a['class']:
                    a.append(obsidian_link)
                if 'nextBtn' in a['class']:
                    a.insert(0, obsidian_link)
        for i, span in enumerate(controls.find_all('span', text="  |  ")):
            if i == 1:
                span.decompose()

        text_soup.insert(0, controls)

    for li in text_soup.find_all('li'):
        if not li.has_attr('id'):
            continue
        verse_num = li['id']
        li.insert(0, f'###### {verse_num}\n')
        li.append('\n')

    general_html_to_md(soup, obsidian_link_by_path, obsidian_img_link_by_path)

    return text_soup.get_text().strip()


def remove_newlines_and_space(tag):
    for child in tag.children:
        if child == '\n':
            child.replace_with('')
        elif '\n' in child and child.string:
            child.replace_with(" ".join(child.string.split()))


def strip(tag):
    children = list(tag.children)
    for child in [children[0], children[-1]]:
        if child == '\n':
            child.replace_with('')
        return

def toc_html_to_md(soup, obsidian_link_by_path, obsidian_img_link_by_path):
    main_soup = soup.find(class_="mainContent")
    for a in main_soup.find_all('a'):
        remove_newlines_and_space(a)
    for preview in main_soup.find_all(id='sectionPreviewList'):
        preview.decompose()
    for preview in main_soup.find_all(id='sectionPreviewHeading'):
        preview.decompose()
    for preview in main_soup.find_all(class_='chapterSummaryPanelGroup'):
        preview.decompose()
    for scripture_text in main_soup.find_all(id='scriptureText'):
        title = get_chapter_title(soup)
        scripture_text.replace_with("# " + title)
    for scripture_text in main_soup.select('.scriptureText.breadcrumbSpacer'):
        title = get_chapter_title(soup)
        scripture_text.replace_with("# " + title)
    for scripture_text in main_soup.find_all(class_='scriptureText'):
        scripture_text.decompose()
    for breadcrumb in main_soup.find_all(class_='navBreadcrumb'):
        breadcrumb.decompose()
    for book_link in main_soup.select('a > .bookLink'):
        remove_newlines_and_space(book_link)
        li = soup.new_tag('li')
        book_link.parent.insert_before(li)
    for li in main_soup.find_all('li'):
        li.insert(0, '- ')
        remove_newlines_and_space(li)

    general_html_to_md(soup, obsidian_link_by_path, obsidian_img_link_by_path)
    text = main_soup.get_text().strip()
    return condense_newlines(text, 2)


def condense_newlines(text, n_newlines):
    return re.sub(r'\n\s*\n', '\n'*n_newlines, text)


def download_html(material_path, dirr):
    response = requests.get(BASE_URL + material_path)
    if not response.ok:
        return None
    with open(os.path.join(dirr, ".".join(material_path.split("/")[1:])) + ".html", "w+") as f:
        f.write(response.text)
    return response


def get_chapter_paths(toc_soup):
    return [li.a['href'] for li in toc_soup.find_all('li', class_='chapter') if li]


def get_info_paths(toc_soup):
    return [a['href'] for a in toc_soup.select("div.navigationText.multicolumn")[0].find_all('a')]


def get_material_paths(toc_soup: BeautifulSoup):
    paths = []
    for a in toc_soup.find_all('a', href=True):
        href = a['href']
        # Get front matter, back matter, and books (OT, NT, BoM)
        if len(a.select('.bookLink')):
            paths.append(href)
        # Get sections/chapters
        elif a.parent and a.parent.has_attr('class') and 'chapter' in a.parent.attrs['class']:
            paths.append(href)

        # if len(paths) > 0:
        #     last_path = paths[-1]
        #     if last_path[-1].isalpha():
        #         paths.append(last_path + "/1")
        #     if last_path[-1].endswith("/"):
        #         paths.append(last_path + "1")
    return paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", nargs="+")
    parser.add_argument("-u", "--url", nargs="+")
    parser.add_argument("-o", "--output-dir", default="output")
    parser.add_argument("-c", "--use-cache", action="store_true")

    args = parser.parse_args()
    main(args)
