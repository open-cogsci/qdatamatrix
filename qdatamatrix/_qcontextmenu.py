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

from qtpy import QtWidgets, QtGui, QtCore
from qdatamatrix.translate import _


class QContextAction(QtWidgets.QAction):

	def __init__(self, icon, title, menu, keyseq=None):

		QtWidgets.QAction.__init__(self, QtGui.QIcon.fromTheme(icon), title,
			menu)
		if keyseq is not None:
			self.setShortcut(QtGui.QKeySequence(keyseq))
		self._menu = menu
		self.triggered.connect(self.activate)

	@property
	def spreadsheet(self):

		return self._menu._spreadsheet

	def activate(self):

		pass


class QCopyAction(QContextAction):

	def __init__(self, menu):

		QContextAction.__init__(self, u'edit-copy', _(u'Copy'), menu, u'Ctrl+C')

	def activate(self):

		self.spreadsheet._copy()


class QCutAction(QContextAction):

	def __init__(self, menu):

		QContextAction.__init__(self, u'edit-cut', _(u'Cut'), menu, u'Ctrl+X')

	def activate(self):

		self.spreadsheet._cut()


class QPasteAction(QContextAction):

	def __init__(self, menu):

		QContextAction.__init__(self, u'edit-paste', _(u'paste'), menu,
			u'Ctrl+V')

	def activate(self):

		self.spreadsheet._paste()


class QRemoveRowAction(QContextAction):

	def __init__(self, menu):

		n = len(menu._spreadsheet._selected_rows)
		QContextAction.__init__(self, u'list-remove',
			_(u'Remove %d row(s)') % n, menu)

	def activate(self):

		self.spreadsheet._remove_rows()


class QRemoveColumnAction(QContextAction):

	def __init__(self, menu):

		n = len(menu._spreadsheet._selected_columns)
		QContextAction.__init__(self, u'list-remove',
			_(u'Remove %d column(s)') % n, menu)

	def activate(self):

		self.spreadsheet._remove_columns()


class QContextMenu(QtWidgets.QMenu):

	def __init__(self, spreadsheet=None):

		QtWidgets.QMenu.__init__(self, parent=spreadsheet)
		self._spreadsheet = spreadsheet
		self.addAction(QCutAction(self))
		self.addAction(QCopyAction(self))
		self.addAction(QPasteAction(self))
		self.addSeparator()
		if spreadsheet._selected_rows:
			self.addAction(QRemoveRowAction(self))
		if spreadsheet._selected_columns:
			self.addAction(QRemoveColumnAction(self))
