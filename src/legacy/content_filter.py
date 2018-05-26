#!/usr/bin/python

__author__ = 'tony.zjt.test@gmail.com (Tony ZHOU)'

from content_generator import ContentGenerator
import logging
import re


def filter_content(content):
    patterns = ['<h3 style="font-family: Verdana;"><span class="Apple-style-span".+?Related post.+article</b></div>', '<div class="MsoNormal">\n<span class="MsoHyperlink"><span style="color: black; font-size: 9pt;">Other.+article</b></div>',
        '<div class="MsoNormal"><span style="color: black; font-family: Verdana; font-size: 9pt;"><b>Java tutorials.+article</b></div>',
        '<div class="MsoNormal">\n<span style="font-family: Arial; font-size: 9.0pt; mso-bidi-font-weight: bold;">Related.+article</b></div>',
        '<span style="color: black; font-family: Verdana; font-size: 8pt;">If you are like MySQL.+article</b></div>',
        '<div class="MsoNormal"><span class="MsoHyperlink"><span style="color: black; font-family: Verdana; font-size: 9pt;">Some more.+article</b></div>']
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.S)
    
    return content


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    
    content_generator = ContentGenerator('http://javarevisited.blogspot.sg/2010/10/basic-networking-commands-in-linuxunix.html')
    
    content = content_generator.generate_readable_article()

    logging.info(filter_content(content))
    
if __name__ == '__main__':
    main()
