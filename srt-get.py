#!/usr/bin/python
#coding=utf-8

from sys import argv, exit
import urllib

EXTENSIONS = ["amv", "asf", "avi", "drc", "flv", "m2v", "m4p", "m4v", "mkv", "mov", "mp2", "mp4", "mpe", "mpeg", "mpg", "mpv", "ogg", "qt", "rm", "rmvb", "vob", "wmv"]
movieName = ""


def main(args):
    if (not args or "--help" in args):
        showHelp()
    else:
        _parseInput(args)
        _displayAvailable()
        _getSubtitlesFile()


def _parseInput(args):
    """ Processes user input in search of the movie's title """
    args[0] = args[0].strip()
    if len(args) == 1:
        if any("." + ext in args[0] for ext in EXTENSIONS):
            _parseAsMovieFile(args[0], None)
        else:
            _parseAsMovieName(args[0])
    elif len(args) == 2:
        _parseAsMovieFile(args[0], args[1])


def _parseAsMovieFile(name, delimiter):
    global movieName
    movieName = name if delimiter is None or delimiter is " " else name.replace(delimiter, " ")


def _parseAsMovieName(name):
    global movieName
    movieName = name


def _displayAvailable():
    """ Displays subtitle files available for download """
    pass


def _getSubtitlesFile():
    """ Downloads the selected subtitles file """
    pass


def showHelp():
    print "usage:", "srt-get movie-name"
    print 6*" ", "srt-get movie-file [delimiter]"
    exit(0)


if __name__ == "__main__":
    main(argv[1:])
