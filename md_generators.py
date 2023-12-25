import re

import markdownify

from html_modifiers import remove_newlines_and_space, strip
from html_parsers import get_chapter_title


def general_html_to_md(soup, obsidian_link_by_path, obsidian_img_link_by_path):
    for sup in soup.find_all('sup', string="*"):
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
                if href not in obsidian_link_by_path:
                    continue
                obsidian_link = obsidian_link_by_path[href]
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

    general_html_to_md(soup, obsidian_link_by_path, obsidian_img_link_by_path)

    return text_soup.get_text().strip()


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
    return re.sub(r'\n\s*\n', '\n' * n_newlines, text)
