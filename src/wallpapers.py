from threading import Thread
import urllib2, re, logging

class InterfacelifeWallpaperRetriever:
    def __init__(self, resolution, root_url_pattern, local_dir):
        self.resolution = resolution
        self.root_url = root_url_pattern
        self.local_dir = local_dir

    def copy_remote(self, request, remoteUrl, localFilename):
        logging.info('Retrieving %s to %s ...' % (remoteUrl, localFilename))
        request = urllib2.Request(remoteUrl, headers={'User-Agent':"Magic Browser"})
        wallpaper_file = urllib2.urlopen(request)
        output = open(localFilename, 'wb')
        output.write(wallpaper_file.read())
        output.close()
    
    def get_wallpaper_names(self, url, request):
        logging.info('Requesting page source from %s ...' % (url))
        htmlText = urllib2.urlopen(request).read()
        logging.info('Finding all wall papers in %s ...' % (url))
        regexprs = 'http://interfacelift.com/wallpaper/previews/(.+?)@2x.jpg', 'http://interfacelift.com/wallpaper/previews/(.+?).jpg'
        wallpapers = []
        for regexpr in regexprs:
            pattern = re.compile(regexpr)
            wallpapers.extend(re.findall(pattern, htmlText))
        
        logging.info(wallpapers)
        
        return wallpapers
    
    
    def get_all_wallpapers(self, resolution, request, wallpapers):
        head = 'http://interfacelift.com/wallpaper/7yz4ma1/'
        tail = '_' + resolution + '.jpg'
        
        for wallpaper in wallpapers:
            wallpaper_url = head + wallpaper + tail
            local_wallpaper_filename = self.local_dir + '/' + wallpaper_url.split('/')[-1]
            self.copy_remote(request, wallpaper_url, local_wallpaper_filename)
    
    def retrieve(self, url):
        request = urllib2.Request(url, headers={'User-Agent':"Magic Browser"})
        wallpapers = self.get_wallpaper_names(url, request)
        self.get_all_wallpapers(self.resolution, request, wallpapers)
    
    def concurrent_retrieve(self):
        threads = []
        total_threads = 0
        MAX_CONCURRENT_THREADS = 10
        for page in range(1, 304):
            url = self.root_url.format(page)
            t = Thread(target=self.retrieve, args=(url,))
            t.start()
            threads.append(t)
            
            total_threads += 1
            logging.info("Staring thread %d" % total_threads)
            if total_threads % MAX_CONCURRENT_THREADS == 0:
                logging.info("Waiting for threads to finish ...")
                for t in threads:
                    t.join()
                total_threads = 0
                threads = []
                logging.info("Waiting for threads to finish ... OK")
                
        logging.info('All done.')

class HdWallpaperRetriever:
    def __init__(self, resolution, root_url, local_dir):
        self.resolution = resolution
        self.root_url = root_url
        self.local_dir = local_dir
        
    def copy_remote(self, remoteUrl, localFilename):
        print 'Retrieving %s to %s ...' % (remoteUrl, localFilename)
        request = urllib2.Request(remoteUrl, headers={'User-Agent':"Magic Browser"})
        wallpaper_file = urllib2.urlopen(request)
        output = open(localFilename, 'wb')
        output.write(wallpaper_file.read())
        output.close()
    
    
    def get_html(self, url):
        print 'Requesting page source from %s ...' % (url)
        request = urllib2.Request(url, headers={'User-Agent':"Magic Browser"})
        html = urllib2.urlopen(request).read()
        return html
    
    
    def get_wallpaper_names(self, html):
        wallpaperNames = []
        regexprs = [ '<a href="/(.+?)-wallpapers.html' ]
        for regexpr in regexprs:
            print "Compiling %s ..." % regexpr
            pattern = re.compile(regexpr)
            wallpaperNames.extend(re.findall(pattern, html))
        
        print wallpaperNames
        return wallpaperNames
    
    def get_wallpaper_urls(self, page):
        url = self.root_url + self.resolution + '_hd-wallpapers-r/page/{}'.format(page)
        
        html = self.get_html(url)
        
        print 'Finding all wall papers in %s ...' % (url)
        wallpaperNames = self.get_wallpaper_names(html)
        
        wallpaperUrls = []
        for wallpaperName in wallpaperNames:
            wallpaperUrl = self.root_url + 'download/' + wallpaperName + '-' + self.resolution + '.jpg'
            wallpaperUrls.append(wallpaperUrl)
        
        return wallpaperUrls
    
    
    def get_all_wallpapers(self, wallpaperUrls):
        print "Retrieving " + str(wallpaperUrls) + "..."
        for wallpaperUrl in wallpaperUrls:
            localWallpaperFilename = self.local_dir + '/' + wallpaperUrl.split('/')[-1]
            self.copy_remote(wallpaperUrl, localWallpaperFilename)
    
    def retrieve(self, page):
        wallpaper_urls = self.get_wallpaper_urls(page)
        self.get_all_wallpapers(wallpaper_urls)
    
    def concurrent_retrieve(self):
        threads = []
        concurrentThreads = 0
        MAX_CONCURRENT_THREADS = 10
        
        for page in range(3, 206):
            t = Thread(target=self.retrieve, args=(page,))
            t.start()
            threads.append(t)
            
            concurrentThreads += 1
            print "Staring thread %d" % concurrentThreads
            if concurrentThreads % MAX_CONCURRENT_THREADS == 0:
                print "Waiting for threads to finish ..."
                for t in threads:
                    t.join()
                concurrentThreads = 0
                threads = []
                print "Waiting for threads to finish ... OK"   
                
        print 'All done.'

def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    
    retriever = HdWallpaperRetriever('1920x1080', 'http://www.hdwallpapers.in/', 'C:/Users/Tony/Pictures/wallpaper/hdwallpapers2')
    retriever.concurrent_retrieve()
    
    retriever = InterfacelifeWallpaperRetriever('1920x1080', 'http://interfacelift.com/wallpaper/downloads/date/any/index{}.html', 'C:/Users/Tony/Pictures/wallpaper/interfacelift2')
    retriever.concurrent_retrieve()

if __name__ == "__main__":
    main()
