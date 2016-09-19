#!/usr/bin/python
#coding=utf-8

from bs4 import BeautifulSoup
from sys import argv, exit
import urllib2

EXTENSIONS = ["amv", "asf", "avi", "drc", "flv", "m2v", "m4p", "m4v", "mkv", "mov", "mp2", "mp4", "mpe", "mpeg", "mpg", "mpv", "ogg", "qt", "rm", "rmvb", "vob", "wmv"]
URL = "http://www.opensubtitles.org/en/search/sublanguageid-all/simplexml" #TODO: Add
movieName = ""

LONGEST_NAME_LEN = 0
LONGEST_FORMAT_LEN = 0
LONGEST_AUTHOR_LEN = 0

class Movie:
    def __init__(self, name, format, author, rating, dateadded, dwLink):
        self.name = name
        self.format = format
        self.author = author if author != None else "*anonymous*" 
        self.rating = rating
        self.dateAdded = dateadded
        self.dwLink = dwLink

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
    if (not args or "--help" in args):
        showHelp()
    else:
        _parseInput(args)
        _displayAvailableSubtitles()
        _getSubtitlesFile()


def _parseInput(args):
    """ Interprets user input in search of the movie's title """

    args[0] = args[0].strip()

    if len(args) == 2:
        if any("." + ext in args[0] for ext in EXTENSIONS):
            _parseAsMovieFile(args[0], None)
        else:
            _parseAsMovieName(args[0])
    
    elif len(args) == 3:
        _parseAsMovieFile(args[0], args[1])


def _parseAsMovieFile(name, delimiter):
    global movieName
    movieName = name if delimiter is None or delimiter is " " else name.replace(delimiter, " ")


def _parseAsMovieName(name):
    global movieName
    movieName = name


def _displayAvailableSubtitles():
    """ Displays subtitle files available for download """

    subtitles = _getAvailableSubtitles()

    print "##__NAME" + (LONGEST_NAME_LEN-2)*"_" + "EXT" + (LONGEST_FORMAT_LEN-1)*"_" + "BY" + (LONGEST_AUTHOR_LEN)*"_" + "ADDED ON" + 11*"_"
    for i in xrange(0, len(subtitles)):
        s = subtitles[i]
        print "%2d  %s %s %s %s %s %s %s" % (i, s.name, (LONGEST_NAME_LEN-len(s.name))*" ", s.format, (LONGEST_FORMAT_LEN-len(s.format))*" ", s.author, (LONGEST_AUTHOR_LEN-len(s.author))*" ", s.dateAdded)


def _getAvailableSubtitles():
    soup = BeautifulSoup(urllib2.urlopen(URL), "html.parser")
    subtitleTags = soup.search.findAll('subtitle')
    subtitles = []

    for subtitle in subtitleTags:
        name = subtitle.releasename.string
        format = subtitle.format.string
        user = subtitle.user.string
        rating = subtitle.subrating.string
        dateAdded = subtitle.subadddate.string
        dwLink = subtitle.download.string

        movie = Movie(name, format, user, rating, dateAdded, dwLink)
        subtitles.append(movie)

    return subtitles


def _getSubtitlesFile():
    """ Downloads the selected subtitles file """

    pass


def showHelp():
    print "usage:", "srt-get movie-name language"
    print 6*" ", "srt-get movie-file language [delimiter]"
    exit(0)


if __name__ == "__main__":
    main(argv[1:])