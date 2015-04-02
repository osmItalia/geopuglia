#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="geopuglia",
    version="0.1.0",
    author="Alessandro De Noia",
    author_email="alessandro.denoia@gmail.com",
    packages=[
        "geopuglia",
    ],
    include_package_data=True,
    install_requires=[
        "Django==1.8c1",
    ],
    zip_safe=False,
    scripts=["geopuglia/manage.py"],
)
