from scrapers import eecs16a
import argparse


def main():
    try:
        print(f"Downloading {ARGS.semester} {ARGS.course} files...")
        eval(f"{ARGS.course}.scraper.scrape(\"{ARGS.semester}\")")
        print("\nCourse file download complete")
    except NameError:
        print(f"ERROR: No matching course scraper for \"{ARGS.course} {ARGS.semester}\"")


def parse_args():
    parser = argparse.ArgumentParser(description="Downloads files from supported UCB course websites automatically")
    parser.add_argument("course", help="course abbreviation to download")
    parser.add_argument("semester", help="semester abbreviation to download: [SP/SU/FA + YY]")
    parser.add_argument("--debug", "-v", action="store_true", help="verbose debugging to stdout")
    parser.add_argument("--include-yt", action="store_true", help="download Youtube videos")
    parser.add_argument("--no-gdrive", action="store_true", help="do not download Google Drive files")
    parser.add_argument("--max-size", type=check_positive, help="maximum single filesize (in MB)")
    return parser.parse_args()


def check_positive(value):
    try:
        value = int(value)
        if value <= 0:
            raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
    except ValueError:
        raise Exception(f"{value} is not an integer")
    return value


ARGS = parse_args()

if __name__ == "__main__":
    main()
