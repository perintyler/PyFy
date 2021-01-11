# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyty-perintyler", # Replace with your own username
    version="0.0.1",
    author="Tyler Perin",
    author_email="pyty.lib@gmail.com",
    description="A lightweight library for interacting with APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/perintyler/PyTy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2.0 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
