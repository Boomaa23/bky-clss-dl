# bky-clss-dl

Downloads course files from supported UCB course websites automatically.

## Usage
1. Download this repository
2. Install [Python 3.5 or newer](https://www.python.org/downloads/)
3. Install required packages: `pip install -r requirements.txt`
4. Run `python3 main.py [course] [semester] (args)` (see arguments section below)
   1. *For example: `python3 main.py eecs16a fa21`*
5. All files from that course will be downloaded

## Arguments
```
usage: main.py [-h] [--debug] [--no-yt] [--no-gdrive] course semester

Downloads files from supported UCB course websites automatically

positional arguments:
  course       course abbreviation to download
  semester     semester abbreviation to download: [SP/SU/FA + YY]

optional arguments:
  -h, --help   show this help message and exit
  --debug      verbose debugging to stdout
  --no-yt      do not auth & download Youtube videos
  --no-gdrive  do not auth & download Google Drive files
```

## Troubleshooting
- Make sure Python 3.5+ is installed
- Ensure required packages have been installed
- Use one word when passing course argument
- Ensure Python has write access to the current folder

## Supported Courses
| Course Name | Semesters |
|-------------|-----------|
| EECS16A     | FA21      |