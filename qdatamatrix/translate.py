#-*- coding:utf-8 -*-

"""
This file is part of qdatamatatrix.

qdatamatatrix is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

qdatamatatrix is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with qdatamatatrix.  If not, see <http://www.gnu.org/licenses/>.
"""

from datamatrix.py3compat import *
from qtpy import QtCore

qt_major_version = int(QtCore.PYQT_VERSION_STR.split(".")[0])

if py3 or qt_major_version > 4:
	def _(s):
		return QtCore.QCoreApplication.translate(u'qdatamatrix', s)
else:
	def _(s):
		return QtCore.QCoreApplication.translate(u'qdatamatrix', s,
			encoding=QtCore.QCoreApplication.UnicodeUTF8)
