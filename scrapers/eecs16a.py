import util

invalid_url_keywords = [
    ".html", "forms.gle", "datahub", "youtu.be", "youtube", 
    "google.com", "zoom", "accessengineeringlibrary"
]

class EECS16AScraper(util.AbstractCourseScraper):
    def __init__(self):
        super().__init__("eecs16a", invalid_url_keywords)

    def scrape(self):
        hrefs, texts = util.get_a_href_elems("https://eecs16a.org/")

        for i in range(len(hrefs)):
            href = hrefs[i]
            text = texts[i]
            print(href, text)

            if text == "Slides":
                self.dl_course_file(href, "slides/")
            elif "Note " in text:
                self.dl_course_file(href, "notes/")
            elif text == "Anusha's Notes":
                self.dl_course_file(href, "discussion/")
            elif text == "Prob PDF" or text == "Ans PDF" or text == "iPython Sol":
                if "homework" in href:
                    self.dl_course_file(href, "homework/")
                else:
                    self.dl_course_file(href, "discussion/")
            elif text == "Presentation" or text == "In-Person Zip File":
                self.dl_course_file(href, "lab/")
            elif "student-resources/exams" in href:
                self.dl_course_file(href, "exams/")
            elif self.valid_url(href):
                if "discussion" in href:
                    self.dl_course_file(href, "discussion/")
                elif "homework" in href:
                    self.dl_course_file(href, "homework/")
                else:
                    self.dl_course_file(href, "misc/")

scraper = EECS16AScraper()