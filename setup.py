#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    setup.py
    ~~~~~~~~

    A set of tools for lawyers

    :copyright: (c) 2021 by Law Engineering Systems SRL.
    :license: see LICENSE for more details.
"""

import codecs
import os
import re
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """Taken from pypa pip setup.py:
    intentionally *not* adding an encoding option to open, See:
       https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    """
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='lawyertools',
    version=find_version("lawyertools", "__init__.py"),
    description='A set of tools for lawyers',
    long_description=read('README.rst'),
    classifiers=[
        ],
    author='Biagio Distefano',
    author_email='b.distefano@lawengineeringsystems.com',
    url='https://gitlab.com/lawengineeringsystems/lawyertools',
    packages=[
        'lawyertools'
        ],
    platforms='any',
    license='LICENSE',
    install_requires=[
        'virtualenv>=1.11.6',
        'pep8>=1.5.7',
        'pyflakes>=0.8.1',
        'fastapi==0.70.0',
        ]
)
