from scrapers import eecs16a, cs61a
import sys

def main():
    sel_scraper = sys.argv[1].lower()
    try:
        eval(f'{sel_scraper}.scrape()')
    except NameError:
        print(f'ERROR: No matching class scraper for \"{sel_scraper}\"')

if __name__ == "__main__":
    main()
