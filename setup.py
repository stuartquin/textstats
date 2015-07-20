import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="textstats",
    version="0.1",
    author="Stuart",
    author_email="stuart.quin@gmail.com",
    description=(""),
    url="https://github.com/stuartquin/textstats",
    packages=['textstats'],
    package_dir={'textstats': 'textstats'},
    data_files=[('', ['README.md'])],
    long_description=read('README.md'),
    install_requires=[
    ]
)
