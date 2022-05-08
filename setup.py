#!/usr/bin/env python

#
#  setup.py
#  
#  Copyright The SpaceLab-Transmitter Contributors.
#  
#  This file is part of SpaceLab-Transmitter.
#
#  SpaceLab-Transmitter is free software; you can redistribute it
#  and/or modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  
#  SpaceLab-Transmitter is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public
#  License along with SpaceLab-Transmitter; if not, see <http://www.gnu.org/licenses/>.
#  
#


import setuptools
import os

exec(open('spacelab_transmitter/version.py').read())

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name                            = "spacelab_transmitter",
    version                         = __version__,
    author                          = "Vitória Beatriz Bianchin", 
    author_email                    = "vitoriabbianchin@gmail.com",
    maintainer                      = "Gabriel Mariano Marcelino",
    maintainer_email                = "gabriel.mm8@gmail.com",
    url                             = "https://github.com/spacelab-ufsc/spacelab-transmitter",
    license                         = "GPLv3",
    description                     = "SpaceLab packet transmitter",
    long_description                = long_description,
    long_description_content_type   = "text/markdown",
    classifiers                     = [
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research"
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Communications :: Ham Radio",
        "Topic :: Education",
        "Topic :: Scientific/Engineering",
        ],
    download_url                    = "https://github.com/spacelab-ufsc/spacelab-transmitter/releases",
    packages                        = setuptools.find_packages(),
    install_requires                = ['PyGObject','pyngham'],
    entry_points                    = { 
        'gui_scripts': [
            'spacelab-transmitter = spacelab_transmitter.__main__:main'
            ]
        },
    data_files                      = [ 
        ('share/icons/', ['spacelab_transmitter/data/img/spacelab_transmitter_256x256.png']),
        ('share/applications/', ['spacelab_transmitter.desktop']),
        ('share/spacelab_transmitter/', ['spacelab_transmitter/data/ui/spacelab_transmitter.glade']),
        ('share/spacelab_transmitter/', ['spacelab_transmitter/data/img/spacelab-logo-full-400x200.png']),
        ('share/spacelab_transmitter/', ['spacelab_transmitter/data/satellites/floripasat-1.json']),
        ('share/spacelab_transmitter/', ['spacelab_transmitter/data/satellites/floripasat-2.json']),
        ],
)
