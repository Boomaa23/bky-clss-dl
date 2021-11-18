from scrapers import eecs16a, cs61a
import sys

def main():
    sel_course = sys.argv[1].lower()
    try:
        eval(f'{sel_course}.scraper.scrape()')
    except NameError:
        print(f'ERROR: No matching course scraper for \"{sel_course}\"')

if __name__ == "__main__":
    main()
