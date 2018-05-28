#!/usr/bin/env python
"""Download all wallpapers from https://unsplash.com/.

# NOTE:

Photo hyperlink pattern: https://unsplash.com/photos/<.+>/download?force=true


# TODO:
    * Download the html of https://unsplash.com/ to /tmp/unsplash.html

    * Crawl all the non-photo hyperlinks in unsplash.html and save them
    together with https://unsplash.com/ to /tmp/non_photo_links.txt

    * Grep all the photo hyperlinks in the HTMLs of each of the non_photo_links
    and save to /tmp/photo_links.txt

    * Download all the photos to /tmp/photo_links.txt to /tmp/unsplash
"""

import contextlib
import logging
import urllib2

USER_AGENT_VALUE = 'Magic Browser'
USER_AGENT = 'User-Agent'


def download_unsplash_html(path='/tmp/'):
    """Download the html of https://unsplash.com/ to /{path}/unsplash.html.

    Args:
        path (str): The path to save the downloaded html to.

    Returns:
        str: the full path of the downloaded html.

    Side effect:
        I/O:
            1. Web download an html
            2. Save the html to local file system
    """
    url = 'https://unsplash.com/'
    filename = 'unsplash.html'
    local_filename = path + filename

    logging.info("downloading unsplash html from %s to %s ...",
                 url, path)

    request = urllib2.Request(url, headers={USER_AGENT: USER_AGENT_VALUE})

    with contextlib.closing(urllib2.urlopen(request)) as wallpaper_file:
        with open(local_filename, 'w') as output:
            output.write(wallpaper_file.read())

    logging.info("downloading unsplash html from %s to %s ... done",
                 url, path)

    return local_filename


def main():
    """Bootstrap."""
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    download_unsplash_html()


if __name__ == "__main__":
    main()
