#!/usr/bin/env python
"""Download all wallpapers from https://unsplash.com/.

# NOTE:

Photo hyperlink pattern: https://unsplash.com/photos/<.+>/download?force=true


# Algorithm

* Download the html of https://unsplash.com/ to /tmp/unsplash.html

* Crawl all the non-photo hyperlinks in unsplash.html and save them together
with https://unsplash.com/ to /tmp/non_photo_links.txt

* Grep all the photo hyperlinks in the HTMLs of each of the non_photo_links
and save to /tmp/photo_links.txt

* Download all the photos to /tmp/photo_links.txt to /tmp/unsplash
"""

import logging


def main():
    """Bootstrap."""
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info("Hello unsplash")


if __name__ == "__main__":
    main()
