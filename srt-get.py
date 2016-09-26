#!/usr/bin/env python
# coding=utf-8

import urllib2
from bs4 import BeautifulSoup
from sys import argv, exit

longest_name_length = 0
longest_format_length = 0
longest_author_length = 0

chosen_subtitle_id = None
movie_name = None
sub_lang = None
subtitles = []


class Movie:
    def __init__(self, id, name, format, author, rating, date_added):
        self.id = id
        self.name = name
        self.format = format
        self.author = author if author is not None else "*anonymous*"
        self.rating = rating
        self.date_added = date_added

        global longest_name_length
        global longest_format_length
        global longest_author_length
        if len(self.name) > longest_name_length:
            longest_name_length = len(self.name)
        if len(self.format) > longest_format_length:
            longest_format_length = len(self.format)
        if len(self.author) > longest_author_length:
            longest_author_length = len(self.author)


def main(args):
    _parse_input_params(args)
    _display_subtitles_menu()
    _get_subtitles_file()


def _parse_input_params(args):
    """ Interprets user input in search of the movie's title """

    global movie_name, sub_lang
    args[0] = args[0].strip()

    if len(args) == 2 and not "--help" in args:
        movie_name = args[0]
        sub_lang = args[1].capitalize()
    else:
        show_help()


def _display_subtitles_menu():
    """ Displays subtitle files available for download """

    global subtitles
    subtitles = _get_available_subtitles()

    print "##__NAME" + (longest_name_length - 2) * "_" \
          + "EXT" + (longest_format_length - 1) * "_" \
          + "BY" + longest_author_length * "_" \
          + "ADDED ON" + 11 * "_"

    for i in xrange(0, len(subtitles)):
        s = subtitles[i]
        print "%2d  %s %s %s %s %s %s %s" \
              % (i, s.name, (longest_name_length - len(s.name)) * " ", s.format,
                 (longest_format_length - len(s.format)) * " ", s.author,
                 (longest_author_length - len(s.author)) * " ", s.date_added)

    _display_choice_prompt()


def _display_choice_prompt():
    global chosen_subtitle_id

    try:
        user_choice = int(raw_input("Number of subtitles file to download? "))
        chosen_subtitle_id = subtitles[user_choice].id
    except IndexError, ValueError:
        print "Invalid number. Please type in the number next to your chosen option."
        _display_choice_prompt()


def _get_available_subtitles():
    """ Gets subtitles available on the server """

    global sub_lang, movie_name
    soup = BeautifulSoup(urllib2.urlopen(
            "http://www.opensubtitles.org/en/search/moviename-" \
            + movie_name.replace(" ", "+") \
            + "/sublanguageid-all/simplexml"), \
            "html.parser")
    subtitle_tags = soup.search.findAll('subtitle')
    subtitles_available = []

    for subtitle in subtitle_tags:
        if subtitle.language.string == sub_lang:
            name = subtitle.releasename.string
            format = subtitle.format.string
            user = subtitle.user.string
            rating = subtitle.subrating.string
            date_added = subtitle.subadddate.string
            id = subtitle.idsubtitle.string

            movie = Movie(id, name, format, user, rating, date_added)
            subtitles_available.append(movie)

    return subtitles_available


def _get_subtitles_file():
    """ Downloads the selected subtitles file """

    global chosen_subtitle_id
    subtitle_file_stream = urllib2.urlopen("http://www.opensubtitles.org/en/subtitleserve/sub/" + chosen_subtitle_id)
    subtitle_file_output = movie_name + ".zip"
    with open(subtitle_file_output, "wb") as output:
        output.write(subtitle_file_stream.read())
    print "Successfully downloaded the file to your current directory as", subtitle_file_output + ". Enjoy!"


def show_help():
    print "usage:", "srt-get movie-name language"
    exit(0)


if __name__ == "__main__":
    main(argv[1:])
