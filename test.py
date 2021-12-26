import common
import gutil

import os


def run_tests():
    count = file_test()
    count += download_test()
    print(f"TOTAL: {count}/8 tests passed, {8 - count}/8 failed.")


def file_test():
    print("\nFILE TEST:\n" +
          "Intended results (if found):\n" +
          "credentials.json - gsvc.conf previously decoded\n" +
          "token.json - previously logged in to Google\n")

    count = 0
    count += verify_file("credentials.json")
    count += verify_file("token.json")

    print("\nFile test done. Check test/ folder to verify intended results.")
    print(f"{count}/2 tests passed, {2 - count}/2 failed.")
    return count


def download_test():
    count = 0
    print("\nDOWNLOAD TEST:\n" +
          "Intended test results:\n" +
          "Lecture0B_Aug26_Slides.pdf\n" +
          "EECS16ADis1Amp4.mp4\n" +
          "EECS16ADis3Bmp4.mp4\n" +
          "CopyofEECS16AMidterm2ReviewSpring2021.pdf\n" +
          "EECS 16A Lecture 1A 08-31-21 [vzEy7l2uTlk].mp4\n" +
          "EECS 16A Lecture 12B 11-18-21 [vDF0cY1LCq0].mp4\n")

    print("pdf, regular, public (Lecture0B_Aug26_Slides.pdf)")
    common.download_file("https://eecs16a.org/lecture/Lecture0B_Aug26_Slides.pdf", "test")
    count += verify_file("test/Lecture0B_Aug26_Slides.pdf")

    print("video, gdrive, public (EECS16ADis1Amp4.mp4)")
    gutil.download_drive_file("1Pm5JvRDKsvlVte0mjYJFvIN9hrxHAHDO", "test")
    count += verify_file("test/EECS16ADis1Amp4.mp4")

    print("video, gdrive, private (EECS16ADis3Bmp4.mp4)")
    gutil.download_drive_file("1UDWT4bRTWyawCn2FdzeDNSzHsDT61Fwa", "test")
    count += verify_file("test/EECS16ADis3Bmp4.mp4")

    print("gdoc, gdrive, private (CopyofEECS16AMidterm2ReviewSpring2021.pdf)")
    gutil.download_drive_file("1R9kWCEu-7oTL6hLfWXNI6K7IeD1pyp_ZftbpPohD8yA", "test")
    count += verify_file("test/CopyofEECS16AMidterm2ReviewSpring2021.pdf")

    print("video, youtube, public (EECS 16A Lecture 1A 08-31-21 [vzEy7l2uTlk].mp4)")
    gutil.download_youtube_video("https://youtu.be/vzEy7l2uTlk", "test")
    count += verify_file("test/EECS 16A Lecture 1A 08-31-21 [vzEy7l2uTlk].mp4")

    print("video, youtube, private (EECS 16A Lecture 12B 11-18-21 [vDF0cY1LCq0].mp4)")
    gutil.download_youtube_video("https://youtu.be/vDF0cY1LCq0", "test")
    count += verify_file("test/EECS 16A Lecture 12B 11-18-21 [vDF0cY1LCq0].mp4")

    print("\nDownload test done. Check test/ folder to verify intended results.")
    print(f"{count}/6 tests passed, {6 - count}/6 failed.")
    return count


def verify_file(fn):
    exists = os.path.exists(fn)
    if exists:
        print(f"{fn} found\n")
    else:
        print(f"{fn} NOT FOUND\n")
    return exists
