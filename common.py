import bs4
import os
import re
import requests

import gutil
import main


class DLType:
    REGULAR = 0
    GOOGLE = 1
    YOUTUBE = 2


class AbstractCourseScraper:
    direct_ext = ["pdf", "ipynb", "zip"]

    def __init__(self, name, valid_semesters, override_url=None):
        self.name = name
        self.override_url = override_url
        self.base_url = f"https://inst.eecs.berkeley.edu/~{name}/"
        self.valid_semesters = valid_semesters
        self.semester = None
        self.href_dl_queue = []

    def get_course_url(self):
        return self.override_url if self.override_url else self.base_url + self.semester + "/"

    def scrape(self, semester):
        if semester not in self.valid_semesters:
            raise NotImplementedError(f"\"{semester}\" is not a valid semester for \"{self.name}\"")
        self.semester = semester
        self.do_scrape(get_page(self.get_course_url()))
        self.dl_course_queue()

    def do_scrape(self, page):
        raise NotImplementedError(f"\"{self.name}\" scraper not implemented")

    def add_course_file(self, url, folder, file_type=DLType.GOOGLE):
        url = self.fully_qualify_url(url)
        path = self.name + "/" + folder
        self.href_dl_queue.append((url, path, file_type))

    def fully_qualify_url(self, url):
        if not url.startswith("http"):
            url = self.get_course_url() + "/" + url
        return url

    def dl_course_queue(self):
        for idx, href in enumerate(self.href_dl_queue):
            print(idx, *href)
            if href[2] == DLType.REGULAR:
                download_file(*href)
            elif href[2] == DLType.GOOGLE and not main.ARGS.no_gdrive:
                gutil.download_drive_file(gutil.fileid_from_url(href[0]), href[1])
            elif href[2] == DLType.YOUTUBE and not main.ARGS.no_yt:
                gutil.download_youtube_video(href)

    def can_direct_dl(self, href):
        return href[href.rindex(".") + 1:] in self.direct_ext


def get_page(url):
    req = requests.get(url)
    if req.status_code != 200:
        return bs4.BeautifulSoup("")
    meta_match = re.findall(r"url='(.*)'", req.text)
    if 'http-equiv="Refresh"' in req.text and meta_match:
        return get_page(meta_match[0])
    return bs4.BeautifulSoup(req.content, features="html.parser")


def get_final_url(init_url):
    name_req = requests.head(init_url, allow_redirects=True)
    return name_req.url if name_req.history else init_url


def download_file(url, path=None, filename=None):
    if not filename:
        filename = url.split('/')[-1]
    if path:
        filename = path + "/" + filename
        os.makedirs(path, exist_ok=True)
    if os.path.exists(filename):
        return

    with requests.get(url, stream=True) as stream:
        stream.raise_for_status()
        with open(filename, 'wb') as file:
            for chunk in stream.iter_content(chunk_size=4096):
                file.write(chunk)
