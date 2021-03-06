import importlib
import test

import argparse


def main():
    try:
        print(f"Downloading {ARGS.semester} {ARGS.course} files...")
        scraper_module = importlib.import_module(f'scrapers.{ARGS.course}')
        eval(f"scraper_module.scraper.scrape(\"{ARGS.semester}\")")
        print("\nCourse file download complete")
    except NameError as e:
        print(e)
        print(f"ERROR: No matching course scraper for \"{ARGS.course} {ARGS.semester}\"")


def parse_args():
    parser = argparse.ArgumentParser(description="Downloads files from supported UCB course websites automatically")
    parser.add_argument("course", help="course abbreviation to download")
    parser.add_argument("semester", help="semester abbreviation to download: [sp/su/fa + YY]")
    parser.add_argument("--debug", "-v", action="store_true", help="verbose debugging to stdout")
    parser.add_argument("--include-yt", action="store_true", help="download Youtube videos")
    parser.add_argument("--no-gdrive", action="store_true", help="do not download Google Drive files")
    parser.add_argument("--max-size", type=check_positive, help="maximum single filesize (in MB)")
    parser.add_argument("--test", "-t", action="store_true", help="run a test script only")
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
    if ARGS.test:
        test.run_tests()
    else:
        main()
