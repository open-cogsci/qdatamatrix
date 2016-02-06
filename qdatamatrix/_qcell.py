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
from qtpy.QtWidgets import QTableWidgetItem
from qtpy.QtCore import Qt
from qtpy.QtGui import QFont, QColor, QBrush

class QCell(QTableWidgetItem):

	def __init__(self, val=u'', style=None):

		QTableWidgetItem.__init__(self, safe_decode(val))
		self._style = style
		self.update_style()
		# self.unhighlight()

	def clone(self):

		return self.__class__()

	def set_header_style(self):

		fnt = QFont()
		fnt.setWeight(QFont.Black)
		self.setFont(fnt)
		self.setBackground(QBrush(QColor(u'#d3d7cf')))
		# self.unhighlight()

	@property
	def style(self):

		if self.row() == 0:
			return u'header'
		if self._style is None:
			try:
				float(self.text())
				return u'numeric'
			except:
				return u'text'
		return self._style

	@style.setter
	def style(self, style):

		self._style = style
		self.update_style()

	def update_style(self):

		self.setBackground(QBrush(QColor(u'#eeeeec')))
		if self.style == u'numeric':
			self.setTextAlignment(Qt.AlignRight)
		elif self.style == u'text':
			self.setTextAlignment(Qt.AlignLeft)
		elif self.style == u'header':
			self.setTextAlignment(Qt.AlignCenter)
			self.set_header_style()
		elif self.style == u'row':
			self.setTextAlignment(Qt.AlignRight)
		else:
			raise Exception(u'Unknown style: %s' % self.style)

	# def highlight(self):
	#
	# 	self.setBackground(QBrush(QColor(u'#d3d7cf')))
	#
	# def unhighlight(self):
	#
	# 	self.setBackground(QBrush(QColor(u'#eeeeec')))
