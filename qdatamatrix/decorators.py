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


def disconnected(fnc):

	def inner(self, *args, **kwdict):

		try:
			self.cellChanged.disconnect()
			cellChanged = True
		except:
			cellChanged = False
		retval = fnc(self, *args, **kwdict)
		if cellChanged:
			self.cellChanged.connect(self._on_cell_changed)
		return retval

	return inner

def silent(fnc):

	def inner(self, *args, **kwdict):

		_silent = self._silent
		self._silent = True
		retval = fnc(self, *args, **kwdict)
		self._silent = _silent
		return retval

	return inner

def undoable(fnc):

	"""
	desc:
		A decorator that adds the operations done by a function to the undo
		stack.
	"""

	def inner(self, *args, **kwdict):

		if self._auto_update:
			undo = self._start_undo_action()
		else:
			undo = False
		retval = fnc(self, *args, **kwdict)
		if undo:
			self._end_undo_action()
		return retval

	return inner


def fix_cursor(fnc):

	"""
	desc:
		A decorator that preserves the cursor position.
	"""

	def inner(self, *args, **kwdict):

		pos = self._cursor_pos
		retval = fnc(self, *args, **kwdict)
		self._cursor_pos = pos
		return retval

	return inner
