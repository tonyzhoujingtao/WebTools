__author__ = 'tony.zjt.test@gmail.com (Tony ZHOU)'

import mechanize, re
from sets import Set

class LinkCollector:
    def __init__(self):
        self.br = mechanize.Browser()
        self.br.set_handle_robots(False)
        self.br.addheaders = [('User-agent', 'Firefox')]
        
        self.links = Set([])

    def collect(self, url, regexpr):
        if not url in self.links:
            print 'Crawling %s ...' % url
            
            self.links.add(url)
            
            html = self.br.open(url).read()
            pattern = re.compile(regexpr)
            
            child_links = re.findall(pattern, html)
            for child_link in child_links:
                self.collect(child_link, regexpr)
            
            print 'Crawling %s ... OK' % url
        
        return self.links
        

def main():
    link_collector = LinkCollector()
    print link_collector.collect('http://javarevisited.blogspot.sg/', 'href="(http://javarevisited.blogspot.com/[0-9][0-9][0-9][0-9]/[0-9][0-9]/.+?.html)')

if __name__ == '__main__':
    main()
