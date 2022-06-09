# bky-clss-dl

Downloads course files from supported UCB course websites automatically.

## Usage
1. Download this repository
2. Install [Python 3.5 or newer](https://www.python.org/downloads/)
3. Install required packages: `pip install -r requirements.txt`
   1. (optional) Install ffmpeg if downloading Youtube videos
4. Run `python3 main.py [course] [semester] (args)` (see arguments section below)
   1. For example: `python3 main.py eecs16a fa21`
5. All files from that course will be downloaded

## Arguments
```
usage: main.py [-h] [--debug] [--include-yt] [--no-gdrive]
               [--max-size MAX_SIZE] [--test]
               course semester

Downloads files from supported UCB course websites automatically

positional arguments:
  course               course abbreviation to download
  semester             semester abbreviation to download: [sp/su/fa + YY]

optional arguments:
  -h, --help           show this help message and exit
  --debug, -v          verbose debugging to stdout
  --include-yt         download Youtube videos
  --no-gdrive          do not download Google Drive files
  --max-size MAX_SIZE  maximum single filesize (in MB)
  --test, -t           run a test script only
```

## Troubleshooting
- Make sure Python 3.5+ is installed
- Ensure required packages have been installed
- Run test script and ensure all tests pass
- Delete `token.json` and sign in using a Berkeley Google account
- Use one word when passing course argument
- Ensure Python has write access to the current folder

## Supported Courses
| Course Name | Semesters |
|-------------|-----------|
| EECS16B     | SP22      |
| EECS16A     | FA21      |