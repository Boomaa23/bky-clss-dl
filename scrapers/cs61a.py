import util

invalid_url_keywords = [
    ".html", "forms.gle", "youtu.be", "youtube", "piazza"
    "google.com", "zoom", "code.cs61a.org", "composingprograms"
]

class CS61AScraper(util.AbstractCourseScraper):
    def __init__(self):
        super().__init__("cs61a", invalid_url_keywords)
    
    def scrape(self):
        hrefs, texts = util.get_a_href_elems("https://cs61a.org")

        for i in range(len(hrefs)):
            href = hrefs[i]
            text = texts[i]
            print(href, text)
            if not self.valid_url(href):
                continue
            
            if "/disc/" in href:
                self.dl_num_assign(href, "disc", "pdf", "discussion/")
            elif "/hw/" in href:
                self.dl_num_assign(href, "hw", "zip", "homework/")
            elif "/lab/" in href:
                self.dl_num_assign(href, "lab", "zip")
            elif "/proj/" in href:
                proj_name = href[href.rindex("proj/") + len("proj/"):href.rindex("/")]
                href += proj_name + ".zip"
                self.dl_course_file(href, "projects/")
            elif "/slides/" in href:
                self.dl_course_file(href, "slides/")
            else:
                self.dl_course_file(href, "misc/")

        hrefs, texts = util.get_a_href_elems("https://cs61a.org/resources/")

        for i in range(len(hrefs)):
            href = hrefs[i]
            text = texts[i]
            print(href, text)
            if not self.valid_url(href):
                continue

            if "/exam/" in href:
                self.dl_course_file(href, "exams/")
            elif "/mock-exams/" in href:
                self.dl_course_file(href, "mockexams/")
            else:
                self.dl_course_file(href, "misc/")
    
    def dl_num_assign(self, href, category, ext, path=None):
        if not path:
            path = category + "/"
        num = href[href.rindex(category) + len(category):href.rindex("/")]
        href += category + num + "." + ext
        self.dl_course_file(href, path)
            
scraper = CS61AScraper()