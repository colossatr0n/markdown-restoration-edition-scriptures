import os.path
import re

import markdownify

from html_modifiers import remove_newlines_and_space, strip
from html_parsers import get_chapter_title
from predicates import is_toc, is_volume_toc, is_book_toc


def html_to_md(path, soup, obsidian_link_by_path, obsidian_img_link_by_path, rel_path, link_type):
    if not is_toc(soup):
        md = material_html_to_md(path, soup, obsidian_link_by_path, obsidian_img_link_by_path, rel_path, link_type)
    elif is_volume_toc(soup):
        md = toc_html_to_md(path, soup, obsidian_link_by_path, obsidian_img_link_by_path, rel_path, link_type)
    elif is_book_toc(soup):
        md = toc_html_to_md(path, soup, obsidian_link_by_path, obsidian_img_link_by_path, rel_path, link_type)
    else:
        raise SystemExit(f"Unknown HTML category for: {soup}.")
    return md


def general_html_to_md(path, soup, obsidian_link_by_path, obsidian_img_link_by_path, rel_links, link_type):
    for sup in soup.find_all('sup', string="*"):
        sup.insert(0, '\\')

    # Replace anchor text with obsidian links
    for a in soup.find_all('a'):
        if a and a.has_attr('href'):
            href = a['href'].replace(' ', '')
            # Assures chapter link instead of chapter + verse link
            href = re.sub("(/\d+)[\-.]\d.*$", r"\1", href)
            href = re.sub("/$", "", href)
            new_tag = soup.new_tag("div")
            text = a.text
            pipe = "\\|" if a.find_parent("td") else "|"

            if href not in obsidian_link_by_path:
                # Remove trailing path part
                alt_href = "/".join(href.split("/")[:-1])
                if alt_href in obsidian_link_by_path:
                    obsidian_link_by_path[href] = obsidian_link_by_path[alt_href]

            if href in obsidian_link_by_path:
                # Book TOCs use digits for the anchor text. Use the obsidian link instead by removing the alias.
                if a.parent.has_attr('class') and 'chapter' in a.parent['class']:
                    text = os.path.basename(".".join(obsidian_link_by_path[href].split(".")[:-1]))

                if rel_links:
                    # Removes extra '../' from relpath
                    link_path = "/".join(os.path.relpath(obsidian_link_by_path[href], path).split("/")[1:])
                    if link_type == 'wikilinks':
                        # remove extension
                        link_path = '.'.join(link_path.split(".")[:-1])
                else:
                    link_path = ".".join(os.path.basename(obsidian_link_by_path[href]).split(".")[:-1])
            elif href.startswith("#"):
                if a.has_attr('class') and 'accordion-toggle' in a['class']:
                    continue
                link_path = href
            else:
                continue

            if link_path.strip() == text.strip():
                pipe = ""
                text = ""

            if link_type == "wikilinks":
                new_tag.string = f"[[{link_path}{pipe}{text}]]"
            else:
                new_tag.string = f"[{text if text else link_path}]({link_path.replace(' ', '%20')})"
            a.replace_with(new_tag)

    for img in soup.find_all('img'):
        if not img.has_attr('src') or not img['src'] in obsidian_img_link_by_path:
            continue
        div = soup.new_tag('div')
        href = img['src']
        if rel_links:
            # Removes extra '../' from relpath
            link_path = "/".join(os.path.relpath(obsidian_img_link_by_path[href], path).split("/")[1:])
        else:
            link_path = str(os.path.basename(obsidian_img_link_by_path[href]))

        if link_type == 'wikilinks':
            div.string = f"![[{link_path}|{'.'.join(os.path.basename(link_path).split('.')[:-1])}]]"
        else:
            div.string = f"![{'.'.join(os.path.basename(link_path).split('.')[:-1])}](" + link_path.replace(' ', '%20') + ")"
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


def material_html_to_md(path, soup, obsidian_link_by_path, obsidian_img_link_by_path, rel_path, link_type):
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
                if href not in obsidian_link_by_path:
                    # Remove trailing path part
                    alt_href = "/".join(href.split("/")[:-1])
                    if alt_href not in obsidian_link_by_path:
                        continue
                    obsidian_link_by_path[href] = obsidian_link_by_path[alt_href]
                obsidian_link = obsidian_link_by_path[href]
                alias = ".".join(os.path.basename(obsidian_link).split('.')[:-1])
                obsidian_link = alias if alias else obsidian_link
                if 'prevBtn' in a['class']:
                    a.append(obsidian_link)
                if 'nextBtn' in a['class']:
                    a.insert(0, obsidian_link)
        for i, span in enumerate(controls.find_all('span', string="  |  ")):
            if i == 1:
                span.decompose()

        text_soup.insert(0, controls)

    for li in text_soup.find_all('li'):
        if not li.has_attr('id'):
            continue
        verse_num = li['id']
        li.insert(0, f'###### {verse_num}\n')
        li.append('\n')

    general_html_to_md(path, soup, obsidian_link_by_path, obsidian_img_link_by_path, rel_path, link_type)

    return text_soup.get_text().strip()


def toc_html_to_md(path, soup, obsidian_link_by_path, obsidian_img_link_by_path, rel_path, link_type):
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

    general_html_to_md(path, soup, obsidian_link_by_path, obsidian_img_link_by_path, rel_path, link_type)
    text = main_soup.get_text().strip()
    return condense_newlines(text, 2)


def condense_newlines(text, n_newlines):
    return re.sub(r'\n\s*\n', '\n' * n_newlines, text)
