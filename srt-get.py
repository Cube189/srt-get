#!/usr/bin/env python
# coding=utf-8

import urllib2
from bs4 import BeautifulSoup
from sys import argv, exit

EXTENSIONS = ["amv", "asf", "avi", "drc", "flv", "m2v", "m4p", "m4v", "mkv",
              "mov", "mp2", "mp4", "mpe", "mpeg", "mpg", "mpv", "ogg", "qt",
              "rm", "rmvb", "vob", "wmv"]

LONGEST_NAME_LEN = 0
LONGEST_FORMAT_LEN = 0
LONGEST_AUTHOR_LEN = 0

chosenSubtitleId = None
movieName = None
subLang = None
subtitles = []


class Movie:
    def __init__(self, name, format, author, rating, date_added, id):
        self.name = name
        self.format = format
        self.author = author if author is not None else "*anonymous*"
        self.rating = rating
        self.date_added = date_added
        self.id = id

        global LONGEST_NAME_LEN
        global LONGEST_FORMAT_LEN
        global LONGEST_AUTHOR_LEN
        if len(self.name) > LONGEST_NAME_LEN:
            LONGEST_NAME_LEN = len(self.name)
        if len(self.format) > LONGEST_FORMAT_LEN:
            LONGEST_FORMAT_LEN = len(self.format)
        if len(self.author) > LONGEST_AUTHOR_LEN:
            LONGEST_AUTHOR_LEN = len(self.author)


def main(args):
    _parse_input(args)
    _display_subtitles_menu()
    _get_subtitles_file(chosenSubtitleId)


def _parse_input(args):
    """ Interprets user input in search of the movie's title """

    global subLang
    args[0] = args[0].strip()

    if len(args) == 2 and not "--help" in args:
        if any("." + ext in args[0] for ext in EXTENSIONS):
            _parse_as_movie_file(args[0], None)
        else:
            _parse_as_movie_name(args[0])
        subLang = args[1]
    else:
        show_help()


def _parse_as_movie_file(name, delimiter):
    global movieName
    movieName = name if delimiter is None or delimiter is " " else name.replace(delimiter, " ")


def _parse_as_movie_name(name):
    global movieName
    movieName = name


def _display_subtitles_menu():
    """ Displays subtitle files available for download """

    global subtitles
    subtitles = _get_available_subtitles()

    print "##__NAME" + (LONGEST_NAME_LEN - 2) * "_"\
          + "EXT" + (LONGEST_FORMAT_LEN - 1) * "_"\
          + "BY" + (LONGEST_AUTHOR_LEN) * "_"\
          + "ADDED ON" + 11 * "_"

    for i in xrange(0, len(subtitles)):
        s = subtitles[i]
        print "%2d  %s %s %s %s %s %s %s" % (
            i, s.name, (LONGEST_NAME_LEN - len(s.name)) * " ", s.format,
            (LONGEST_FORMAT_LEN - len(s.format)) * " ", s.author,
            (LONGEST_AUTHOR_LEN - len(s.author)) * " ", s.date_added)

    _display_choice_prompt()


def _display_choice_prompt():
    global chosenSubtitleId

    try:
        userChoice = int(raw_input("Number of subtitles file to download? "))
        chosenSubtitleId = subtitles[userChoice].id
    except IndexError, ValueError:
        print "Invalid number. Please type in the number next to your chosen option."
        _display_choice_prompt()


def _get_available_subtitles():
    global subLang, movieName
    soup = BeautifulSoup(urllib2.urlopen(
            "http://www.opensubtitles.org/en/search/moviename-"\
            + movieName.replace(" ", "+") + "/sublanguageid-all/simplexml"),\
            "html.parser")
    subtitleTags = soup.search.findAll('subtitle')
    subtitles = []

    for subtitle in subtitleTags:
        if subtitle.language.string == subLang:
            name = subtitle.releasename.string
            format = subtitle.format.string
            user = subtitle.user.string
            rating = subtitle.subrating.string
            dateAdded = subtitle.subadddate.string
            id = subtitle.idsubtitle.string

            movie = Movie(name, format, user, rating, dateAdded, id)
            subtitles.append(movie)

    return subtitles


def _get_subtitles_file(dw_link):
    """ Downloads the selected subtitles file """

    global chosenSubtitleId
    subtitleFileUrl = "http://www.opensubtitles.org/en/subtitleserve/sub/"+chosenSubtitleId
    subtitleFile = urllib2.urlopen(subtitleFileUrl)
    subtitleFileName = movieName+".zip"
    with open(movieName+".zip", "wb") as output:
        output.write(subtitleFile.read())
    print "Successfully downloaded the file to your current directory as", subtitleFileName + ". Enjoy!"


def show_help():
    print "usage:", "srt-get movie-name language"
    exit(0)


if __name__ == "__main__":
    main(argv[1:])
