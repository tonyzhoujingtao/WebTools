__author__ = 'tony.zjt.test@gmail.com (Tony ZHOU)'

import mechanize
from bs4 import BeautifulSoup
from readability.readability import Document

class ContentGenerator:
    def __init__(self, url):
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Firefox')]
        html = br.open(url).read()
        self.doc = Document(html)
        self.readable_article = ''
        self.raw_article = ''
        self.readable_title = ''
        self.first_paragraph = ''

    def generate_readable_article(self):
        print "Generating article ..."
        if not self.readable_article:
            self.readable_article = self.doc.summary()
        print "Generating article ...OK"
        return self.readable_article

    def generate_readable_title(self):
        print "Generating title ..."
        if not self.readable_title:
            self.readable_title = self.doc.title()
        print "Generating title ... OK"
        return self.readable_title
            
    def generate_raw_article(self):
        if not self.raw_article:
            self.generate_readable_article()
        
            soup = BeautifulSoup(self.readable_article)
            # print "soup = %s" % soup
            self.raw_article = soup.text
            # print "raw_article = %s" % raw_article
        return self.raw_article
    
    def generate_first_paragraph(self):
        if not self.first_paragraph:
            self.generate_readable_article()
            soup = BeautifulSoup(self.readable_article)
            self.first_paragraph = soup.find('p').text
            
        return self.first_paragraph
    

def main():
    contentGenerator = ContentGenerator('http://www.nytimes.com/2013/05/12/us/politics/tucked-in-immigration-bill-special-deals-for-some.html')
    print contentGenerator.generate_readable_article()
    print contentGenerator.generate_first_paragraph()
    

if __name__ == '__main__':
    main()
