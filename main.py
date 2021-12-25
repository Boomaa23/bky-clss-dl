from scrapers import eecs16a
import argparse


def main():
    try:
        print(f"Downloading {ARGS.semester} {ARGS.course} files...")
        eval(f"{ARGS.course}.scraper.scrape(\"{ARGS.semester}\")")
    except NameError:
        print(f"ERROR: No matching course scraper for \"{ARGS.course} {ARGS.semester}\"")


def parse_args():
    parser = argparse.ArgumentParser(description="Downloads files from supported UCB course websites automatically")
    parser.add_argument("course", help="course abbreviation to download")
    parser.add_argument("semester", help="semester abbreviation to download: [SP/SU/FA + YY]")
    parser.add_argument("--debug", action="store_true", help="verbose debugging to stdout")
    parser.add_argument("--no-yt", action="store_true", help="do not auth & download Youtube videos")
    parser.add_argument("--no-gdrive", action="store_true", help="do not auth & download Google Drive files")
    return parser.parse_args()


ARGS = parse_args()

if __name__ == "__main__":
    main()
