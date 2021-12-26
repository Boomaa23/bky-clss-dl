import common
import main


class EECS16AScraper(common.AbstractCourseScraper):
    def __init__(self):
        super().__init__("ee16a", ("fa21",), override_url="https://eecs16a.org")
        self.name = "eecs16a"

    def do_scrape(self, page):
        all_hrefs = page.find_all("a", href=True)
        init_num_hrefs = len(all_hrefs)
        print(f"Found {init_num_hrefs} URLs to parse")
        content_tables = page.find_all("table")
        if not content_tables:
            return
        if main.ARGS.debug:
            print("\n\nPARSING\n-------------")

        schedule_table = content_tables[0].find_all("tr")
        for row in schedule_table:
            cells = row.find_all("td")
            for col_num, cell in enumerate(cells):
                href_elems = cell.find_all("a", href=True)
                for elem in href_elems:
                    href = elem['href']
                    href = super().fully_qualify_url(href)
                    if not super().is_direct_download(href) \
                            and "google" not in href \
                            and "datahub" not in href \
                            and "zoom" not in href:
                        href = common.get_final_url(href)
                    try:
                        href = href[:href.rindex("#")]
                    except ValueError:
                        pass
                    text = elem.text
                    if main.ARGS.debug:
                        print(len(self.href_dl_queue), text, href)

                    if col_num == 0:
                        super().queue_course_file(href, "misc")
                        all_hrefs.remove(elem)
                    elif col_num == 2:
                        if 'Slides' in href:
                            super().queue_course_file(href, "slides", common.DLType.REGULAR)
                            all_hrefs.remove(elem)
                        elif 'Note' in href:
                            super().queue_course_file(href, "notes", common.DLType.REGULAR)
                            all_hrefs.remove(elem)
                        elif 'youtu.be' in href:
                            super().queue_course_file(href, "lecture", common.DLType.YOUTUBE)
                            all_hrefs.remove(elem)
                    elif col_num == 3:
                        if 'drive.google.com' in href:
                            super().queue_course_file(href, "discussion", common.DLType.GOOGLE)
                            all_hrefs.remove(elem)
                        elif 'youtu.be' in href:
                            super().queue_course_file(href, "discussion", common.DLType.YOUTUBE)
                            all_hrefs.remove(elem)
                        elif 'discussion' in href:
                            super().queue_course_file(href, "discussion", common.DLType.REGULAR)
                            all_hrefs.remove(elem)
                    elif col_num == 4:
                        if text and 'datahub' not in href and \
                                ('Presentation' in text or "In-Person Zip File" in text):
                            if 'drive.google.com' in href:
                                super().queue_course_file(href, "lab", common.DLType.GOOGLE)
                            else:
                                super().queue_course_file(href, "lab", common.DLType.REGULAR)
                            all_hrefs.remove(elem)
                    elif col_num == 5:
                        if 'homework' in href:
                            super().queue_course_file(href, "lab", common.DLType.REGULAR)
                            all_hrefs.remove(elem)

        exam_hrefs = content_tables[2].find_all("a", href=True)
        for elem in exam_hrefs:
            super().queue_course_file(elem['href'], "exams", common.DLType.REGULAR)
            all_hrefs.remove(elem)

        for elem in all_hrefs:
            href = elem['href']
            if super().is_direct_download(href):
                fn = href[href.rindex("/") + 1:]
                if fn.startswith('dis') or fn.startswith('ans') or fn.startswith('anusha'):
                    super().queue_course_file(href, "discussion")
                elif fn.startswith('Note'):
                    super().queue_course_file(href, "notes")
                elif fn.startswith('Lecture'):
                    super().queue_course_file(href, "slides")
                else:
                    super().queue_course_file(href, "misc")

        url_pct = round((len(self.href_dl_queue) / init_num_hrefs) * 100, 2)
        print(f'Now downloading {len(self.href_dl_queue)} files ({url_pct}%)')
        if main.ARGS.debug:
            print("\n\nDOWNLOADING\n-------------")


scraper = EECS16AScraper()
