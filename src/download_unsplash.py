#!/usr/bin/env python
"""Download all wallpapers from https://unsplash.com/.

# NOTE:

Photo hyperlink pattern: https://unsplash.com/photos/<.+>/download?force=true


# TODO:
    * Download photos to /tmp/unsplash from urls in /tmp/photo_urls.txt.

    * Delete /tmp/photo_urls.txt.

    * Save all non_photo_urls to /tmp/non_photo_urls.txt.

    * Repeatly crawl all the urls in /tmp/non_photo_urls.txt until it's empty.

# DONE:
    * Download the html of https://unsplash.com/.
    * Grep all the photo urls from the downloaded html.
"""

import contextlib
import logging
import re
import urllib2

USER_AGENT_VALUE = 'Magic Browser'
USER_AGENT = 'User-Agent'


def shorten(long_string):
    return '({} ...)'.format(long_string[:10])


def grep_photo_urls(html):
    """Grep all photo urls from unsplash.html.

    Args:
        path (str): The path to save photo_urls.txt to.

    Returns:
        photo_urls (list).
    """

    logging.info("Grepping photo urls from %s ...", shorten(html))

    p = re.compile('https://unsplash.com/photos/\\S+/download\\?force=true')
    photo_urls = re.findall(pattern=p, string=html)

    logging.info("Grepping photo urls from %s ... done", shorten(html))

    return photo_urls


def download_unsplash_html():
    """Download the html of https://unsplash.com/ to /{path}/unsplash.html.

    Args:
        path (str): The path to save the downloaded html to.

    Returns:
        html (str): unsplash.html in string.

    Side effect:
        I/O:
            1. Web download an html
    """
    url = 'https://unsplash.com/'

    logging.info("Downloading unsplash html from %s ...", url)

    request = urllib2.Request(url, headers={USER_AGENT: USER_AGENT_VALUE})

    html = ""
    with contextlib.closing(urllib2.urlopen(request)) as wallpaper_file:
        html += wallpaper_file.read()

    logging.info("Downloading unsplash html from %s ... done", url)

    return html


def main():
    """Bootstrap."""
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    html = download_unsplash_html()
    photo_urls = grep_photo_urls(html)
    logging.info(photo_urls)
    logging.info(len(photo_urls))


if __name__ == "__main__":
    main()
