#!/bin/python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

sdict = {}

exec(compile(open("autoprotista/version.py").read(), "autoprotista/version.py", 'exec'), {}, sdict)

sdict.update({
    "name" : "autoprotista",
    "description" : "Cellular Automata Engine 1D & 2D",
    "url": "http://github.com/Gab0/autoprotista",
    "author" : "Gabriel Araujo",
    "author_email" : "gabriel_scf@hotmail.com",
    "keywords" : ["cellular automata"],
    "license" : "MIT",
    "install_requires": [
        "nose",
        "coverage"],
    "packages" : ["autoprotista"],
    "classifiers" : [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python"],
})

setup(**sdict)
