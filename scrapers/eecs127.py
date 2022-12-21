import common
import main


class EECS127Scraper(common.AbstractCourseScraper):
    def __init__(self):
        super().__init__("eecs127", ("fa22",), override_url="https://eecs127.github.io")

    def do_scrape(self, page):
        all_hrefs = page.find_all("a", href=True)
        init_num_hrefs = len(all_hrefs)
        print(f"Found {init_num_hrefs} URLs to parse")
        main_table = page.find("div", {"id": "main-content"})
        if not main_table:
            return
        if main.ARGS.debug:
            print("\n\nPARSING\n-------------")

        content_hrefs = main_table.find_all("a", href=True)
        for elem in content_hrefs:
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
            if href == self.get_course_url():
                continue
            
            if 'dis' in href:
                super().queue_course_file(href, "discussion", common.DLType.REGULAR)
                all_hrefs.remove(elem)
            elif 'lectures' in href:
                super().queue_course_file(href, "slides", common.DLType.REGULAR)
                all_hrefs.remove(elem)
            elif 'youtube' in href or 'youtu.be' in href:
                super().queue_course_file(href, "lecture", common.DLType.YOUTUBE)
                all_hrefs.remove(elem)
            elif 'hw' in href:
                super().queue_course_file(href, "homework", common.DLType.YOUTUBE)
                all_hrefs.remove(elem)

        resources_page = common.get_page(self.get_course_url() + "/resources/")
        res_page_hrefs = resources_page.find_all("a", href=True)
        all_hrefs.extend(res_page_hrefs)
        init_num_hrefs += len(res_page_hrefs)
        
        for elem in all_hrefs:
            href = elem['href']
            if super().is_direct_download(href):
                if 'past_exams' in href or 'exam' in href:
                    super().queue_course_file(href, "exams")
                else:
                    super().queue_course_file(href, "misc")

        url_pct = round((len(self.href_dl_queue) / init_num_hrefs) * 100, 2)
        print(f'Now downloading {len(self.href_dl_queue)} files ({url_pct}%)')
        if main.ARGS.debug:
            print("\n\nDOWNLOADING\n-------------")


scraper = EECS127Scraper()
