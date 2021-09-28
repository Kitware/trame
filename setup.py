#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

from setuptools import setup, find_packages

# perform the install
setup(
    name="trame",
    description="Framework for building interactive Web applications quickly in plain Python",
    long_description="""
    Trame aims to be a framework for building interactive applications using a web front-end in plain Python. Such applications can be used locally as any desktop application but also be deployed in the cloud or on premise to access big and/or sensitive data.
    Trame comes with lots of capabilities built-in by leveraging existing libraries or tools such as Vuetify, Altair, Vega, Deck, VTK, ParaView and more. Trame lets you create interactive data processing applications with rich visualizations without switching languages or technologies.
    Trame lets you define your application in a very compact and intuitive way while letting you take over if you know better. Several available layouts let you build your application in no time.
    Trame is the perfect companion to VTK or ParaView by offering various rendering and processing configurations. Trame lets you choose between server-side and client-side rendering along with hybrid approaches.
    """,
    author="Kitware, Inc.",
    author_email="kitware@kitware.com",
    url=f"https://github.com/kitware/trame",
    license="BSD-3-Clause",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: JavaScript",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="Python Interactive Web Application Framework",
    packages=find_packages(".", exclude=("tests.*", "tests")),
    package_dir={"": "."},
    package_data={},
    install_requires=["pywebvue"],
)
