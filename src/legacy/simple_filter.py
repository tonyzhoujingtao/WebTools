#!/usr/bin/python

__author__ = 'tony.zjt.test@gmail.com (Tony ZHOU)'

import files
import logging


class SimpleFilter:
    def __init__(self, filter_file_name='SimpleFilterRecord.txt'):
        self.filter_file = files.touch_open(filter_file_name, "r+")
        self.existing_items = set(self.filter_file.read().splitlines())
        print "Current existing items: {}", len(self.existing_items)

    def filter(self, item):
        if item not in self.existing_items:
            self.existing_items.add(item)
            return item
        else:
            return ''

    def remove(self, item):
        self.existing_items.remove(item)

    def record(self):
        print 'Writing out all {} existing items to file ...', len(self.existing_items)
        for item in self.existing_items:
            self.filter_file.write(item + "\n")
        self.filter_file.close()
        print 'Writing out all {} existing items to file ... OK', len(self.existing_items)

    def __del__(self):
        self.record()


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

    items = ('one', 'One', 'one', 'two')
    simple_filter = SimpleFilter()
    for item in items:
        filtered_item = simple_filter.filter(item)
        logging.info(filtered_item)

if __name__ == '__main__':
    main()
