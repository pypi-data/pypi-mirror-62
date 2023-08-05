#!/usr/bin/python

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='pyaig',
    version='1.0.5',
    license='MIT',
    author=u'Baruch Sterin',
    author_email='pyaig@bsterin.com',
    url='http://github.com/sterin/pyaig',
    description='A simple Python AIG package',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    platforms='any',
    install_requires=[
        'click',
        'future'
    ],
    packages=['pyaig'],
)
