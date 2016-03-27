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

from qdatamatrix import __version__
from setuptools import setup, find_packages

setup(
	name=u'python-qdatamatrix',
	version=__version__,
	description= u'A PyQt4/PyQt5 widget for viewing and editing a DataMatrix object',
	author=u'Sebastiaan Mathot',
	author_email=u's.mathot@cogsci.nl',
	license=u'GNU GPL Version 3',
	url=u'https://github.com/smathot/python-qdatamatrix',
	packages=find_packages('.'),
	install_requires=['python-datamatrix'],
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering',
		 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
	],
)
