import os
import re
import urllib3

def get_page(url):
    connection = urllib3.connection_from_url(url)
    response = connection.urlopen('GET', url)
    return response.data.decode('utf-8')

def get_a_href_elems(url):
    return re.findall(r'<a\s+(?:[^>]*?\s+)?href=(["\'])(.*?)\1', get_page(url))

def download_file(url, path, new_fn=None):
    connection = urllib3.connection_from_url(url)
    response = connection.urlopen('GET', url)
    if response.geturl() != url:
        url = response.geturl()
    if not new_fn:
        try:
            end = url.rindex("#")
        except ValueError:
            end = len(url)
        new_fn = url[url.rindex("/") + 1:end]
    file_path = os.path.join(path, new_fn)

    if not os.path.exists(file_path):
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
        with open(file_path, "wb") as file:
            file.write(response.content)

def download_yt(url, path):
    pass

def download_gdrive(url, path):
    pass