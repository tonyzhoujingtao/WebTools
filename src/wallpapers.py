#!/usr/bin/env python

from threading import Thread
import urllib2
import re
import logging

USER_AGENT_VALUE = "Magic Browser"
USER_AGENT = 'User-Agent'


class InterfacelifeWallpaperRetriever:
    def __init__(self, resolution, root_url_pattern, local_dir):
        self.resolution = resolution
        self.root_url = root_url_pattern
        self.local_dir = local_dir
        self.threads = []
        self.total_threads = 0

    @staticmethod
    def get_wallpapers(url):
        logging.info('Getting wallpaper names in %s ...' % url)

        regular_expressions = 'http://interfacelift.com/wallpaper/previews/(.+?)@2x.jpg', 'http://interfacelift.com/wallpaper/previews/(.+?).jpg'

        return InterfacelifeWallpaperRetriever.extract_wallpapers(get_html(url), regular_expressions)

    @staticmethod
    def extract_wallpapers(html, regular_expressions):
        wallpapers = []
        tmp_names = []
        for regular_expression in regular_expressions:
            pattern = re.compile(regular_expression)
            tmp_names.extend(re.findall(pattern, html))
        for tmp_name in tmp_names:
            wallpapers.append(tmp_name.replace('_672x420', ''))

        logging.info("Find %d Wallpapers: %s" % (len(wallpapers), wallpapers))

        return wallpapers

    def download_wallpapers(self, url):
        head = 'http://interfacelift.com/wallpaper/7yz4ma1/'
        tail = '_' + self.resolution + '.jpg'
        wallpapers = self.get_wallpapers(url)

        for wallpaper in wallpapers:
            remote_url = head + wallpaper + tail
            local_uri = self.local_dir + '/' + remote_url.split('/')[-1]
            copy_remote(remote_url, local_uri)

    def concurrent_download(self, max_concurrent_threads, page):
        url = self.root_url.format(page)
        t = Thread(target=self.download_wallpapers, args=(url,))
        t.start()
        self.threads.append(t)
        self.total_threads += 1
        logging.info("Staring thread %d" % self.total_threads)
        if self.total_threads % max_concurrent_threads == 0:
            logging.info("Waiting for threads to finish ...")
            for t in self.threads:
                t.join()
            logging.info("Waiting for threads to finish ... OK")

    def download(self):
        max_concurrent_threads = 10

        start_page = 107
        end_page = 109

        for page in range(start_page, end_page):
            self.concurrent_download(max_concurrent_threads, page)

        logging.info('All done.')


def copy_remote(remote_url, local_filename):
    logging.info('Copying %s to %s ...' % (remote_url, local_filename))
    request = urllib2.Request(remote_url, headers={USER_AGENT: USER_AGENT_VALUE})
    wallpaper_file = urllib2.urlopen(request)
    output = open(local_filename, 'wb')
    output.write(wallpaper_file.read())
    output.close()


def get_html(url):
    logging.info('Requesting page source from %s ...' % url)
    request = urllib2.Request(url, headers={USER_AGENT: USER_AGENT_VALUE})
    html = urllib2.urlopen(request).read()
    return html


class HdWallpaperRetriever:
    def __init__(self, resolution, root_url, local_dir):
        self.resolution = resolution
        self.root_url = root_url
        self.local_dir = local_dir
        self.threads = []
        self.concurrent_threads = 0
        self.max_concurrent_threads = 10

    @staticmethod
    def get_wallpaper_names(html):
        wallpaper_names = []
        regular_expressions = ['<a href="/(.+?)-wallpapers.html']
        for regular_expression in regular_expressions:
            logging.info("Compiling %s ..." % regular_expression)
            pattern = re.compile(regular_expression)
            wallpaper_names.extend(re.findall(pattern, html))

        logging.info(wallpaper_names)
        return wallpaper_names

    def get_wallpaper_urls(self, page):
        url = self.root_url + self.resolution + '_hd-wallpapers-r/page/{}'.format(page)

        html = get_html(url)

        logging.info('Finding all wall papers in %s ...' % url)
        wallpaper_names = self.get_wallpaper_names(html)

        wallpaper_urls = []
        for wallpaperName in wallpaper_names:
            wallpaper_url = self.root_url + 'download/' + wallpaperName + '-' + self.resolution + '.jpg'
            wallpaper_urls.append(wallpaper_url)

        return wallpaper_urls

    def get_all_wallpapers(self, wallpaper_urls):
        logging.info("Retrieving " + str(wallpaper_urls) + "...")
        for wallpaper_url in wallpaper_urls:
            local_wallpaper_filename = self.local_dir + '/' + wallpaper_url.split('/')[-1]
            copy_remote(wallpaper_url, local_wallpaper_filename)

    def retrieve(self, page):
        wallpaper_urls = self.get_wallpaper_urls(page)
        self.get_all_wallpapers(wallpaper_urls)

    def concurrent_download(self, page):
        t = Thread(target=self.retrieve, args=(page,))
        t.start()
        self.threads.append(t)
        self.concurrent_threads += 1
        logging.info("Staring thread %d" % self.concurrent_threads)
        if self.concurrent_threads % self.max_concurrent_threads == 0:
            logging.info("Waiting for threads to finish ...")

            for t in self.threads:
                t.join()

            logging.info("Waiting for threads to finish ... OK")

    def concurrent_retrieve_all(self):
        for page in range(3, 5):
            self.concurrent_download(page)

        logging.info('All done.')


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

    retriever = HdWallpaperRetriever('2880x1800', 'http://www.hdwallpapers.in/', '/tmp/hdwallpapers')
    retriever.concurrent_retrieve_all()

    # retriever = InterfacelifeWallpaperRetriever('2880x1800',
    #                                             'http://interfacelift.com/wallpaper/downloads/date/any/index{}.html',
    #                                             '/tmp/interfacelift')
    # retriever.download()


if __name__ == "__main__":
    main()
