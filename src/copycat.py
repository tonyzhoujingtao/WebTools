#!/usr/bin/python

# This file demonstrates how to use the Google Data API's Python client library
# to interface with the Blogger service.  There are examples for the following
# operations:
#
# * Retrieving the list of all the user's blogs
# * Retrieving all posts on a single blog
# * Performing a date-range query for posts on a blog
# * Creating draft posts and publishing posts
# * Updating posts
# * Retrieving comments
# * Creating comments
# * Deleting comments
# * Deleting posts

__author__ = 'tony.zjt.test@gmail.com (Tony ZHOU)'

from blogger import BloggerService
from content_generator import ContentGenerator
from link import LinkCollector
from content_filter import filter_content
from simple_filter import SimpleFilter
import logging, sys

def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    
    linkCollector = LinkCollector()
    links = linkCollector.collect('http://javarevisited.blogspot.sg/', 'href="(http://javarevisited.blogspot.com/[0-9][0-9][0-9][0-9]/[0-9][0-9]/.+?.html)')
    
    logging.info('Total articles to copy: {}'.format(str(len(links))))
    
    bloggerService = BloggerService()
#     bloggerService.delete_all_posts()
    
    simple_filter = SimpleFilter('CrawledLinks.txt')
    
    for link in links:
        try:
            filtered_link = simple_filter.filter(link)
            
            if filtered_link:
                contentGenerator = ContentGenerator(filtered_link)
                
                title = contentGenerator.generate_readable_title()
                content = filter_content(contentGenerator.generate_readable_article())
                
                bloggerService.create_post(title, content, False)
        except (ValueError, TypeError) as e:
            logging.error('Bypassing: {}'.format(str(e)))
            simple_filter.remove(link)
        except:
            logging.error('Bypassing unexpected error: {}'.format(str(sys.exc_info()[0])))
            simple_filter.remove(link)
            
    simple_filter.record()


if __name__ == '__main__':
    main()
