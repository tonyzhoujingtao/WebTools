#!/usr/bin/python
#
# Tony ZHOU
#

from distutils.core import setup

required = []


setup(
    name='zhouwebs',
    version='1.0.0',
    description='Python library for web',
    long_description="""\
The ZHOU Python client library makes it easy to interact with web data:
- ZHOU API for web
""",
    author='Tony ZHOU',
    author_email='tony.zjt.test@gmail.com',
    py_modules=['blogger', 'content_generator', 'copycat', 'docs', 'link', 'stock', 'wallpapers'],
    url='https://code.google.com/p/zhouweb/',
    package_dir={'':'src'}, requires=['mechanize']
)
