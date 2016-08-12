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
from qdatamatrix._qspreadsheet import QSpreadSheet
from qtpy import QtWidgets, QtCore


class QDataMatrix(QtWidgets.QWidget):

	"""
	desc:
		QDataMatrix is the main widget for viewing DataMatrix objects.
	"""

	cellchanged = QtCore.Signal(int, int)
	changed = QtCore.Signal()

	def __init__(self, dm, parent=None):

		"""
		desc:
			Constructor to initialize a QDataMatrix object.

		arguments:
			dm:
				type:	`DataMatrix`

		keywords:
			parent:
				desc:	A parent QWidget, or None for no parent.
				type:	[QWidget, None]
		"""

		QtWidgets.QWidget.__init__(self, parent=parent)
		self._dm = dm
		self._spreadsheet = QSpreadSheet(self)
		self._layout = QtWidgets.QHBoxLayout(self)
		self._layout.addWidget(self._spreadsheet)
		self._layout.setContentsMargins(0,0,0,0)
		self.refresh()

	@property
	def dm(self):

		return self._dm

	@dm.setter
	def dm(self, dm):

		self._dm = dm

	def refresh(self):

		"""
		desc:
			Refresh the widget to reflect changes in the associated
			`DataMatrix`.
		"""

		self._spreadsheet.refresh()
