#!/usr/bin/env python

from setuptools import setup, find_packages
import os.path

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="gtexttospeech",
    version="0.1.9",
    author="Paul Miller",
    author_email="paulmillr@me.com",
    description="Converts text to speech using google translate",
    url="http://github.com/paulmillr/gtexttospeech",
    license="MIT",

    long_description=read('README.rst'),
    zip_safe=False,
    packages=['gtexttospeech'],
    package_data={'': ['*.txt', '*.rst', '*.md']},
    data_files=[('', ['LICENSE'])],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    install_requires=['setuptools'],
    entry_points={
        'console_scripts': ['gtts = gtexttospeech.main:main'],
    },
)
