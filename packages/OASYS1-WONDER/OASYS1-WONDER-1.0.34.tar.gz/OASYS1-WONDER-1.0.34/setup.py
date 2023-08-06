#!/usr/bin/env python3

import io
import os, sys

from setuptools import setup, find_packages

with io.open('README.md', 'r', encoding='utf-8') as f:
    ABOUT = f.read()

NAME = 'OASYS1-WONDER'

MAJOR = 1
MINOR = 0
MICRO = 34
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

AUTHOR = 'Luca Rebuffi, Paolo Scardi, Alberto Flor'
AUTHOR_EMAIL = 'paolo.scardi@unitn.ut'

URL = 'https://github.com/WONDER-project/OASYS1-WONDER'
DESCRIPTION = 'Whole POwder PatterN MoDEl in OASYS.'
LONG_DESCRIPTION = ABOUT
LICENSE = 'GPL3+'

CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3 :: Only'
]

KEYWORDS = [
    'oasys1',
]

PACKAGES = find_packages()

PACKAGE_DATA = {
    'orangecontrib.wonder.widgets.wonder' : ['icons/*.*', 'data/*.*'],
    'orangecontrib.wonder.fit.functions.data'       : ['*.*', 'delta_l_files/*.*', 'wulff_solids/*.*'],
}

INSTALL_REQUIRES = sorted(set(
    line.partition('#')[0].strip()
    for line in open(os.path.join(os.path.dirname(__file__), 'requirements.txt'))) - {''})

platform = sys.platform

if platform == "darwin":
    INSTALL_REQUIRES.append('GSAS-II-WONDER-osx>=1.0.3')
elif platform.startswith("win"):
    INSTALL_REQUIRES.append('GSAS-II-WONDER-win')
elif platform.startswith("linux"):
    INSTALL_REQUIRES.append('GSAS-II-WONDER-linux')

NAMESPACE_PACKAGES = ["orangecontrib", "orangecontrib.wonder", "orangecontrib.wonder.widgets"]


ENTRY_POINTS = {
    'oasys.addons': ("WONDER 1 = orangecontrib.wonder",),
    'oasys.widgets': (
        "Wonder 1 = orangecontrib.wonder.widgets.wonder",
    ),
    'oasys.menus': ("wondermenu = orangecontrib.wonder.menu",)

}

from distutils.core import setup

if __name__ == '__main__':

    setup(
        name=NAME,
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        url=URL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license=LICENSE,
        packages=PACKAGES,
        package_data=PACKAGE_DATA,
        keywords=KEYWORDS,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        namespace_packages=NAMESPACE_PACKAGES,
        entry_points=ENTRY_POINTS
    )
