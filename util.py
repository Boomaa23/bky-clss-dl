from html.parser import HTMLParser
import os
import urllib3
from urllib3.exceptions import MaxRetryError

def get_page(url):
    connection = urllib3.connection_from_url(url)
    response = connection.urlopen('GET', url)
    return response.data.decode('utf-8')

def get_a_href_elems(url):
    href_parser = HREFParser()
    href_parser.feed(get_page(url))
    return href_parser.get_ahrefs()

class AbstractCourseScraper:
    def __init__(self, course_name, invalid_url_keywords, course_url=None):
        self.course_name = course_name
        self.invalid_url_keywords = invalid_url_keywords
        self.base_course_url = f'https://{course_name}.org' if not course_url else course_url

    def scrape(self):
        raise NotImplementedError("Scraper method not implemented")

    def dl_course_file(self, url, path):
        if not url.startswith("https://") \
                and not url.startswith("http://"):
            url = self.base_course_url + url
        path = self.course_name + "/" + path
        if self.valid_url(url):
            print(path, url)
            download_file(url, path)

    def valid_url(self, url):
        for term in self.invalid_url_keywords:
            if term in url:
                return False
        return True

class HREFParser(HTMLParser):
    def __init__(self):
        self.parsing_ahref = False
        self.href = []
        self.text = []
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.href.append(attr[1])
                    self.parsing_ahref = True
                    return

    def handle_endtag(self, tag):
        if self.parsing_ahref and tag == "a":
            self.parsing_ahref = False

    def handle_data(self, data):
        if self.parsing_ahref:
            self.text.append(data)
            self.parsing_ahref = False
    
    def get_ahrefs(self):
        return (self.href, self.text)


def download_file(url, path, new_fn=None):
    if (new_fn and os.path.exists(os.path.join(new_fn))) \
            or os.path.exists(os.path.join(get_url_filename(url))):
        return
        
    user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) ..'}
    http = urllib3.PoolManager(10, headers=user_agent)
    try:
        response = http.urlopen('GET', url, assert_same_host=False, retries=10)
    except MaxRetryError:
        return
    if response.geturl() and response.geturl() != url:
        url = response.geturl()
    if not new_fn:
        new_fn = get_url_filename(url)
    file_path = os.path.join(path, new_fn)

    if not os.path.exists(file_path):
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
        with open(file_path, "wb") as file:
            file.write(response.data)

def get_url_filename(url):
    try:
        end = url.rindex("#")
    except ValueError:
        try:
            end = url.index("?")
        except ValueError:
            end = len(url)
    return url[url.rindex("/") + 1:end]

def download_yt(url, path):
    pass

def download_gdrive(url, path):
    pass