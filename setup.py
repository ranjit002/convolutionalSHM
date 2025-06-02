#! /usr/bin/env python
from setuptools import setup

setup(
    name="animation",
    version="0.1",
    packages=["animation"],
    entry_points={
        "console_scripts": [
            "shm = animation.shm:main",
        ],
    },
)
