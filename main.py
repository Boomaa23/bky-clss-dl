from scrapers import eecs16a
import sys


def main():
    try:
        course = sys.argv[1].lower()
        semester = sys.argv[2].lower()
    except IndexError:
        print("ERROR: Not enough arguments passed")
        return

    try:
        debug = sys.argv[3]
    except IndexError:
        debug = False

    try:
        print(f'Downloading {semester} {course} files...')
        eval(f'{course}.scraper.scrape(\"{semester}\", {str(debug)})')
    except NameError:
        print(f'ERROR: No matching course scraper for \"{course} {semester}\"')


if __name__ == "__main__":
    main()
