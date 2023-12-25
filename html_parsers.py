from bs4 import BeautifulSoup


def get_book_links(soup):
    return [book_link for book_link in soup.find_all(class_='bookLink') if book_link]


def get_chapter_title(soup: BeautifulSoup):
    breadcrumb = soup.find("div", class_="navBreadcrumb")
    return breadcrumb.find_all("li")[-1].get_text(" ", strip=True)


def get_breadcrumb_path(soup: BeautifulSoup):
    breadcrumb = soup.find("div", class_="navBreadcrumb")
    return "/".join([a.get_text(" ", strip=True) for a in breadcrumb.find_all("a")][1:])


def get_chapter_paths(toc_soup):
    return [li.a['href'] for li in toc_soup.find_all('li', class_='chapter') if li]


def get_info_paths(toc_soup):
    return [a['href'] for a in toc_soup.select("div.navigationText.multicolumn")[0].find_all('a')]


def get_paths(toc_soup: BeautifulSoup):
    paths = []
    for a in toc_soup.find_all('a', href=True):
        href = a['href']
        # Get front matter, back matter, and books (OT, NT, BoM)
        if len(a.select('.bookLink')):
            paths.append(href)
        # Get sections/chapters
        elif a.parent and a.parent.has_attr('class') and 'chapter' in a.parent.attrs['class']:
            paths.append(href)

    return paths
