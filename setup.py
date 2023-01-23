#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of qdatamatrix.

qdatamatrix is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

qdatamatrix is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with qdatamatrix.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import os
from qdatamatrix import __version__
from setuptools import setup, find_packages

# Increment to force a change in the source tarball.
DUMMY=1

setup(
	name='qdatamatrix',
	version=__version__,
	description= 'A PyQt4/PyQt5 widget for viewing and editing a DataMatrix object',
	author='Sebastiaan Mathot',
	author_email='s.mathot@cogsci.nl',
	license='GNU GPL Version 3',
	url='https://github.com/open-cogsci/qdatamatrix',
	packages=find_packages('.'),
	install_requires=['datamatrix'],
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering',
		 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
	],
)
