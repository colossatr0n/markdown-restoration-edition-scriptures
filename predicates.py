from html_parsers import get_book_links, get_chapter_paths


def is_toc(soup):
    return len(get_book_links(soup)) > 0 or len(get_chapter_paths(soup)) > 0


def is_volume_toc(soup):
    return len(get_book_links(soup)) > 0


def is_book_toc(soup):
    return len(get_chapter_paths(soup)) > 0
