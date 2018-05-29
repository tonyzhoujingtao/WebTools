#!/usr/bin/env python3
"""Download all wallpapers from https://unsplash.com/.

# TODO:
* Add option to limit the number of pictures to download.
"""

from concurrent.futures import ThreadPoolExecutor
import contextlib
from http.client import InvalidURL
from urllib.error import HTTPError, URLError
import logging
import multiprocessing
import os
import re
import urllib.request
import uuid


USER_AGENT_VALUE = 'Magic Browser'
USER_AGENT = 'User-Agent'


def shorten(long_string):
    return '({} ...)'.format(long_string[:10])


def grep_urls(html):
    logging.info('Grepping urls from %s ...', shorten(html))

    pattern = re.compile('\\shref=\"(\\S+)\"\\s')

    all_hrefs = set()
    for href in re.findall(pattern, html):
        if href.startswith('http'):
            all_hrefs.add(href)
        else:
            all_hrefs.add('https://unsplash.com' + href)

    unsplash_hrefs = [x for x in all_hrefs if x.startswith('https://unsplash')]
    unsplash_hrefs = [x for x in unsplash_hrefs if 'login_view' not in x]
    unsplash_hrefs = [x for x in unsplash_hrefs if 'recover/initiate' not in x]

    photo_urls = set()
    non_photo_urls = set()

    for h in unsplash_hrefs:
        if h.startswith('https://unsplash.com/photos/') and h.endswith('download?force=true'):
            photo_urls.add(h)
        else:
            non_photo_urls.add(h)

    logging.info('Grepping urls from %s ... done\n', shorten(html))

    return photo_urls, non_photo_urls


def download_html(url):
    try:
        logging.info('Downloading html from %s ...', url)

        request = urllib.request.Request(
            url, headers={USER_AGENT: USER_AGENT_VALUE})

        html = ""
        with contextlib.closing(urllib.request.urlopen(request)) as html_file:
            html += html_file.read().decode("utf-8")

        logging.info('Downloading html from %s ... done\n', url)

        return html
    except (URLError, HTTPError, UnicodeDecodeError, InvalidURL):
        return ""


def grep_file_name(url):
    pattern = re.compile('.+photos/(\\S+)/download\\?force=true')
    names = re.findall(pattern, url)
    if names:
        return names[0]
    return uuid.uuid4().hex


def download(url, path):
    local_filename = path + grep_file_name(url) + '.jpg'

    logging.info('Downloading %s to %s ...', url, local_filename)

    request = urllib.request.Request(
        url, headers={USER_AGENT: USER_AGENT_VALUE})

    with contextlib.closing(urllib.request.urlopen(request)) as wallpaper_file:
        with open(local_filename, 'wb') as local_file:
            local_file.write(wallpaper_file.read())

    logging.info('Downloading %s to %s ... done', url, local_filename)


def download_all(photo_urls, path='/tmp/unsplash/'):
    logging.info('Downloading %d photos ...', len(photo_urls))

    if not os.path.exists(path):
        os.makedirs(path)

    for url in photo_urls:
        download(url, path)

    logging.info('Downloading %d photos ... done\n', len(photo_urls))


def main():
    logging.basicConfig(
        format='%(asctime)s %(threadName)s %(message)s', level=logging.INFO)

    non_photos_new = set(['https://unsplash.com/'])
    non_photos_visited = set()

    photos_visited = set()

    with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        while non_photos_new:
            non_photo_url = non_photos_new.pop()
            non_photos_visited.add(non_photo_url)

            html = download_html(non_photo_url)

            photo_urls, non_photo_urls = grep_urls(html)
            executor.submit(download_all, photo_urls - photos_visited)
            photos_visited |= photo_urls

            non_photos_new |= (non_photo_urls - non_photos_visited)

    logging.info('Downloaded %d images', len(non_photos_visited))


if __name__ == "__main__":
    main()
