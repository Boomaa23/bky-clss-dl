import util

def scrape():
    a_href_elems = util.get_a_href_elems("https://eecs16a.org/")
    print(a_href_elems)
    return

    for elem in a_href_elems:
        href = elem
        text = elem
        if not text:
            continue

        if text == "Slides":
            dl_16a_file(href, "slides/")
        elif "Note " in text:
            dl_16a_file(href, "notes/")
        elif text == "Anusha's Notes":
            dl_16a_file(href, "discussion/")
        elif text == "Prob PDF" or text == "Ans PDF" or text == "iPython Sol":
            if "homework" in href:
                dl_16a_file(href, "homework/")
            else:
                dl_16a_file(href, "discussion/")
        elif text == "Presentation" or text == "In-Person Zip File":
            dl_16a_file(href, "lab/")
        elif "student-resources/exams" in href:
            dl_16a_file(href, "exams/")
        elif valid_url(href):
            if "discussion" in href:
                dl_16a_file(href, "discussion/")
            elif "homework" in href:
                dl_16a_file(href, "homework/")
            else:
                dl_16a_file(href, "misc/")

invalid_terms = [
    ".html", "forms.gle", "datahub", "youtu.be", "youtube", 
    "google.com", "zoom", "accessengineeringlibrary"
]

def valid_url(href):
    for term in invalid_terms:
        if term in href:
            return False
    return True

def dl_16a_file(url, path):
    if not url.startswith("https://") \
            and not url.startswith("http://"):
        url = "https://eecs16a.org/" + url
    path = "eecs16a/" + path
    if valid_url(url):
        print(path, url)
        util.download_file(url, path)
