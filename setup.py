#!/usr/bin/env python

from setuptools import setup, find_packages
import os.path

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="gtexttospeech",
    version="0.1.4",
    packages=['gtexttospeech'],
    package_data={
        '': ['*.txt', '*.rst', '*.md']
    },
    data_files=[
        ('', ['LICENSE'])
    ],

    author="Paul Bagwell",
    author_email="pbagwl@gmail.com",
    description="Converts text to speech using google translate",
    url="http://pbagwl.com/projects/gtexttospeech",
    license="MIT",

    long_description=read('README'),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'setuptools',
    ],
    entry_points={
        'console_scripts': [
            'gtts = gtexttospeech.main:main',
        ],
    },
)
