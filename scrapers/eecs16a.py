import util


class EECS16AScraper(util.AbstractCourseScraper):
    def __init__(self):
        super().__init__("ee16a", ("fa21",), override_url="https://eecs16a.org")
        self.course_name = "eecs16a"
        self.course_base_url = "https://eecs16a.org"

    def do_scrape(self, page):
        all_hrefs = page.find_all("a", href=True)
        init_num_hrefs = len(all_hrefs)
        print(f"Found {init_num_hrefs} URLs to parse")
        content_tables = page.find_all("table")
        if not content_tables:
            return
        if self.debug:
            print("\n\nPARSING\n-------------")

        schedule_table = content_tables[0].find_all("tr")
        for row in schedule_table:
            cells = row.find_all("td")
            for col_num, cell in enumerate(cells):
                href_elems = cell.find_all("a", href=True)
                for elem in href_elems:
                    href = elem['href']
                    href = super().fully_qualify_url(href)
                    if not super().direct_dl(href):
                        print("NOT DIRECT")
                        href = util.get_final_url(href)
                    try:
                        href = href[:href.rindex("#")]
                    except ValueError:
                        pass
                    text = elem.text
                    if self.debug:
                        print(len(self.href_dl_queue), text, href)

                    if col_num == 0:
                        super().add_course_file(href, "misc")
                        all_hrefs.remove(elem)
                    elif col_num == 2:
                        if 'Slides' in href:
                            super().add_course_file(href, "slides")
                            all_hrefs.remove(elem)
                        elif 'Note' in href:
                            super().add_course_file(href, "notes")
                            all_hrefs.remove(elem)
                        elif 'youtu.be' in href:
                            # youtube lecture video
                            pass
                    elif col_num == 3:
                        if 'drive.google.com' in href:
                            # discussion notes
                            pass
                        elif 'youtu.be' in href:
                            # recorded discussion
                            pass
                        elif 'discussion' in href:
                            super().add_course_file(href, "discussion")
                            all_hrefs.remove(elem)
                    elif col_num == 4:
                        if text and ('Presentation' in text or "In-Person Zip File" in text) \
                                and 'datahub' not in href:
                            if 'drive.google.com' in href:
                                # special gdrive lab worksheet handling
                                pass
                            else:
                                super().add_course_file(href, "lab")
                            all_hrefs.remove(elem)
                    elif col_num == 5:
                        if 'homework' in href:
                            super().add_course_file(href, "lab")
                            all_hrefs.remove(elem)

        exam_hrefs = content_tables[2].find_all("a", href=True)
        for elem in exam_hrefs:
            super().add_course_file(elem['href'], "exams")
            all_hrefs.remove(elem)

        for elem in all_hrefs:
            if '.pdf' in elem['href'].lower():
                super().add_course_file(elem['href'], "misc")

        url_pct = round((len(self.href_dl_queue) / init_num_hrefs) * 100, 2)
        print(f'Now downloading {len(self.href_dl_queue)} files ({url_pct}%)')
        if self.debug:
            print("\n\nDOWNLOADING\n-------------")



scraper = EECS16AScraper()
