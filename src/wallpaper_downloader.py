#!/usr/bin/env python

from threading import Thread
import urllib2
import re
import logging

USER_AGENT_VALUE = "Magic Browser"
USER_AGENT = 'User-Agent'


class WallpaperDownloader(object):
    def __init__(self, resolution, local_dir):
        self.resolution = resolution
        self.local_dir = local_dir
        self.threads = []
        self.total_threads = 0
        self.max_threads = 10

    def download(self, start_page, end_page):
        for page in range(start_page, end_page):
            self.concurrent_download(page)

        logging.info('All done.')

    def concurrent_download(self, page):
        t = Thread(target=self.download_wallpapers, args=(page,))
        t.start()

        self.threads.append(t)
        self.total_threads += 1

        logging.info("Staring thread %d" % self.total_threads)
        if self.total_threads % self.max_threads == 0:
            logging.info("Waiting for threads to finish ...")

            for t in self.threads:
                t.join()

            logging.info("Waiting for threads to finish ... OK")

    def copy_remote_all(self, wallpaper_urls):
        logging.info("Copying " + str(wallpaper_urls) + "...")
        for remote_url in wallpaper_urls:
            local_uri = self.local_dir + '/' + remote_url.split('/')[-1]
            copy_remote(remote_url, local_uri)

    def download_wallpapers(self, page):
        wallpaper_urls = self.get_wallpaper_urls(page)
        self.copy_remote_all(wallpaper_urls)

    def get_wallpaper_urls(self, page):
        wallpaper_names = self.get_wallpaper_names(self.get_page_url(page))

        wallpaper_urls = []
        for wallpaper_name in wallpaper_names:
            wallpaper_url = self.get_wallpaper_url(wallpaper_name)
            wallpaper_urls.append(wallpaper_url)

        return wallpaper_urls


class InterfacelifeWallpaperDownloader(WallpaperDownloader):
    @staticmethod
    def get_regular_expressions():
        return 'http://interfacelift.com/wallpaper/previews/(.+?)@2x.jpg', 'http://interfacelift.com/wallpaper/previews/(.+?).jpg'

    @staticmethod
    def get_wallpaper_names(page_url):
        logging.info('Getting wallpaper names in %s ...' % page_url)
        regular_expressions = InterfacelifeWallpaperDownloader.get_regular_expressions()
        return InterfacelifeWallpaperDownloader.extract_wallpaper_names(get_html(page_url), regular_expressions)

    @staticmethod
    def extract_wallpaper_names(html, regular_expressions):
        wallpaper_names = []
        for wallpaper_name in extract_wallpaper_names(html, regular_expressions):
            wallpaper_names.append(wallpaper_name.replace('_672x420', ''))
        logging.info("Find %d Wallpapers: %s" % (len(wallpaper_names), wallpaper_names))
        return wallpaper_names

    def __init__(self, resolution, local_dir):
        super(InterfacelifeWallpaperDownloader, self).__init__(resolution, local_dir)
        self.root_url = 'http://interfacelift.com/wallpaper/downloads/date/any/index{}.html'


    def get_page_url(self, page):
        return self.root_url.format(page)

    def get_wallpaper_url(self, wallpaper_name):
        head = 'http://interfacelift.com/wallpaper/7yz4ma1/'
        tail = '_' + self.resolution + '.jpg'
        return head + wallpaper_name + tail


class HdWallpaperDownloader(WallpaperDownloader):
    @staticmethod
    def get_regular_expressions():
        return ['<a href="/(.+?)-wallpapers.html']

    @staticmethod
    def get_wallpaper_names(page_url):
        logging.info('Getting wallpaper names in %s ...' % page_url)
        regular_expressions = HdWallpaperDownloader.get_regular_expressions()
        return HdWallpaperDownloader.extract_wallpaper_names(get_html(page_url), regular_expressions)

    @staticmethod
    def extract_wallpaper_names(html, regular_expressions):
        wallpaper_names = extract_wallpaper_names(html, regular_expressions)
        logging.info("Find %d Wallpapers: %s" % (len(wallpaper_names), wallpaper_names))
        return wallpaper_names

    def __init__(self, resolution, local_dir):
        super(HdWallpaperDownloader, self).__init__(resolution, local_dir)
        self.root_url = 'http://www.hdwallpapers.in/'

    def get_page_url(self, page):
        return self.root_url + self.resolution + '_hd-wallpapers-r/page/{}'.format(page)

    def get_wallpaper_url(self, wallpaper_name):
        head = self.root_url + 'download/'
        tail = '-' + self.resolution + '.jpg'
        return head + wallpaper_name + tail


def extract_wallpaper_names(html, regular_expressions):
    wallpaper_names = []
    for regular_expression in regular_expressions:
        pattern = re.compile(regular_expression)
        wallpaper_names.extend(re.findall(pattern, html))
    return wallpaper_names


def copy_remote(remote_url, local_filename):
    logging.info('Copying %s to %s ...' % (remote_url, local_filename))
    request = urllib2.Request(remote_url, headers={USER_AGENT: USER_AGENT_VALUE})
    wallpaper_file = urllib2.urlopen(request)
    output = open(local_filename, 'wb')
    output.write(wallpaper_file.read())
    output.close()


def get_html(url):
    logging.debug('Requesting page source from %s ...' % url)
    request = urllib2.Request(url, headers={USER_AGENT: USER_AGENT_VALUE})
    html = urllib2.urlopen(request).read()
    return html


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    downloader = HdWallpaperDownloader('2880x1800', '/tmp/hdwallpapers')
    downloader.download(15, 17)

    downloader = InterfacelifeWallpaperDownloader('2880x1800', '/tmp/interfacelift')
    downloader.download(107, 109)


if __name__ == "__main__":
    main()
