#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="Ente",
    version="0.1",
    description="place finder on commoncrawl dataset",
    author="László Nagy",
    author_email="rizsotto@gmail.com",
    license='LICENSE',
    url='https://github.com/rizsotto/Ente',
    long_description=open('README.md').read(),
    scripts=['bin/ente']
)
