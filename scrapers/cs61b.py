import common
import main


class CS61BScraper(common.AbstractCourseScraper):
    def __init__(self):
        super().__init__("cs61b", ("sp22",))

    def do_scrape(self, page):
        all_hrefs = page.find_all("a", href=True)
        init_num_hrefs = len(all_hrefs)
        print(f"Found {init_num_hrefs} URLs to parse")
        content_tables = page.find_all("table")
        if not content_tables:
            return
        if main.ARGS.debug:
            print("\n\nPARSING\n-------------")

        schedule_table = content_tables[1].find_all("tr")
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

                    if col_num == 3:
                        if 'slides' in text:
                            super().queue_course_file(href, "slides", common.DLType.REGULAR)
                            all_hrefs.remove(elem)
                    elif col_num == 4:
                        if 'youtube.com' not in href:
                            super().queue_course_file(href, "dis", common.DLType.REGULAR)
                            all_hrefs.remove(elem)
                    elif col_num == 5:
                        if 'gradescope.com' not in href:
                            super().queue_course_file(href, "lab", common.DLType.REGULAR)
                            all_hrefs.remove(elem)
                    elif col_num == 6:
                        if 'gradescope.com' not in href:
                            super().queue_course_file(href, "homework", common.DLType.REGULAR)
                            all_hrefs.remove(elem)


        for elem in all_hrefs:
            href = elem['href']
            if super().is_direct_download(href):
                fn = href[href.rindex("/") + 1:]
                if fn.startswith('dis') or fn.startswith('ans') or fn.startswith('gavin'):
                    super().queue_course_file(href, "discussion")
                elif fn.startswith('Note'):
                    super().queue_course_file(href, "notes")
                elif fn.startswith('Written'):
                    super().queue_course_file(href, "slides")
                else:
                    super().queue_course_file(href, "misc")

        url_pct = round((len(self.href_dl_queue) / init_num_hrefs) * 100, 2)
        print(f'Now downloading {len(self.href_dl_queue)} files ({url_pct}%)')
        if main.ARGS.debug:
            print("\n\nDOWNLOADING\n-------------")


scraper = CS61BScraper()
