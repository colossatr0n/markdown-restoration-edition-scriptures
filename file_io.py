import os

CACHE_DIR = "cache"


def save_image(stream, path, dir):
    filepath = html_path_to_filename(path)
    with open(os.path.join(dir, filepath), 'wb+') as f:
        for chunk in stream:
            f.write(chunk)


def save_html(html, path, dir):
    with open(os.path.join(dir, html_path_to_filename(path)) + ".html", "w+") as f:
        f.write(html)

def open_html(path, dir):
    filename = html_path_to_filename(path)
    return open(os.path.join(dir, filename + '.html'), "r")


def html_path_to_filename(path):
    return ".".join(path.split("/")[1:])
