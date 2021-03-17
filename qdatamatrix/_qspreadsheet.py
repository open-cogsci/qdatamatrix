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
from qdatamatrix.decorators import undoable, disconnected, fix_cursor, silent
from qdatamatrix._qcell import QCell
from qdatamatrix._qcelldelegate import QCellDelegate
from qtpy import QtWidgets, QtGui, QtCore
import re

EMPTY_STR = u'__empty__'
MAX_COL_WIDTH = 300
MARGIN = 30

class QSpreadSheet(QtWidgets.QTableWidget):

	"""
	desc:
		QSpreadSheet implements the table/ spreadsheet of a QDataMatrix. It's
		created automatically by QDataMatrix.
	"""

	def __init__(self, qdm=None, read_only=False):

		QtWidgets.QTableWidget.__init__(self, parent=qdm)
		self._qdm = qdm
		self._undo_stack = []
		self._in_undo_action = False
		self._auto_update = True
		self._silent = False
		self.read_only = read_only
		self._shortcut(u'Ctrl+Z', self._undo)
		self._shortcut(u'Ctrl+C', self._copy)
		self._shortcut(u'Ctrl+V', self._paste)
		self._shortcut(u'Ctrl+X', self._cut)
		# self._shortcut(u'Ctrl+P', self._print)
		self._shortcut(u'Del', self._delete)
		# The cell delegate captures left/ right keypresses so that these
		# immediately move the cursor
		self.delegate = QCellDelegate(self)
		self.delegate.move.connect(self._move)
		self.setItemDelegate(self.delegate)
		# The custom cell object is necessary for styling
		self.setItemPrototype(QCell())
		self.horizontalHeader().hide()
		self.cellChanged.connect(self._on_cell_changed)
		self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
		self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
		# Regular expression to catch all newline varieties of various OS's
		self.newlines_re = re.compile(r'(\r\n|\r|\n)')

	def _print(self):

		print(self.dm)

	def _shortcut(self, keyseq, target):

		QtWidgets.QShortcut(QtGui.QKeySequence(keyseq), self, target,
			context=QtCore.Qt.WidgetWithChildrenShortcut)

	@property
	def _column_names(self):

		"""
		desc:
			Gives a non-sorted representation of the columns.
		"""

		return [column_name for column_name, column in self.dm.columns]

	@property
	def dm(self):

		return self._qdm.dm

	@dm.setter
	def dm(self, dm):

		self._qdm.dm = dm

	@silent
	@fix_cursor
	@disconnected
	def refresh(self):

		self.clear()
		self._adjust_size()
		self._last_visible_row = 0
		for colnr, (name, col) in enumerate(self.dm.columns):
			self._setcell(0, colnr, name)
		self._fill_visible_cells()
			
	@silent
	@fix_cursor
	@disconnected
	def verticalScrollbarValueChanged(self, pos):
		
		self._fill_visible_cells()
	
	@silent
	@fix_cursor
	@disconnected
	def resizeEvent(self, event):
		
		self._fill_visible_cells()

	@silent
	@fix_cursor
	@disconnected
	def showEvent(self, event):
		
		self._fill_visible_cells()
			
	def _fill_visible_cells(self, fill_all=False):

		if self._last_visible_row == len(self.dm):
			return
		# For performance reasons we don't initialize read-tables completely.
		# This makes it possible to view very larges data structures.
		last_row = len(self.dm) if fill_all else min(
			len(self.dm),
			self.rowAt(self.height())
		)
		# rowAt() will return -1 when there is no row at that location. This
		# appears to happen when the last visible row is outside of the dm, and
		# then we just fall back to showing all rows.
		if last_row < 0:
			last_row = len(self.dm)
		for colnr, (name, col) in enumerate(self.dm.columns):
			for rownr in range(self._last_visible_row, last_row):
				val = col[rownr]
				self._setcell(rownr + 1, colnr, val)
			self._optimize_column_width(colnr)
		self._last_visible_row = last_row

	# Overridden functions

	def contextMenuEvent(self, e):

		"""
		desc:
			Shows a context menu.

		arguments:
			e:
				type:	QContextMenuEvent
		"""

		from qdatamatrix._qcontextmenu import QContextMenu
		QContextMenu(self).exec_(e.globalPos())

	@silent
	@fix_cursor
	@disconnected
	def selectAll(self):
		
		"""
		desc:
			Selects all existing cells.
		"""
		
		self._fill_visible_cells(fill_all=True)
		self.setRangeSelected(
			QtWidgets.QTableWidgetSelectionRange(
				0, 0, len(self.dm), len(self.dm.columns) - 1
			),
			True
		)

	# Private functions

	def _adjust_size(self):
		
		if self.read_only:
			self.setColumnCount(len(self.dm.columns))
			self.setRowCount(len(self.dm) + 1)
		else:
			self.setColumnCount((1+(len(self.dm.columns)+50) // 100) * 100)
			self.setRowCount(1 + (1+(len(self.dm)+50) // 100) * 100)
		self.setVerticalHeaderLabels([u'']+ \
			[str(i) for i in range(1, len(self.dm)+1)]+ \
			[u'']*(self.rowCount()-len(self.dm)-1))

	def _move(self, drow, dcol):

		"""
		desc:
			Move the cursor, i.e. the selected cell.

		arguments:
			dRow:
				desc:	The number of rows to move.
				type:	int
			dCol:
				desc:	The number of columns to move.
				type:	int
		"""

		row = max(0, self.currentRow()+drow)
		col = max(0, self.currentColumn()+dcol)
		self.setCurrentCell(row, col)

	@property
	def _selected_columns(self):

		return sorted(set([i.column() for i in self.selectedIndexes() \
			if i.column() < len(self.dm.columns)]))

	@property
	def _selected_rows(self):

		return sorted(set([i.row()-1 for i in self.selectedIndexes() \
			if i.row() > 0 and i.row() <= len(self.dm)]))

	@property
	def _clipboard(self):
		return QtWidgets.QApplication.clipboard()

	@property
	def _cursor_pos(self):

		return self.currentRow(), self.currentColumn()

	@_cursor_pos.setter
	def _cursor_pos(self, pos):

		selection_ranges = self.selectedRanges()
		self.setCurrentCell(pos[0], pos[1])
		for selection_range in selection_ranges:
			self.setRangeSelected(selection_range, True)

	def _column_by_index(self, colnr):

		return self.dm.columns[colnr][1]

	def _add_columns(self, colnr):

		for i in range(len(self.dm.columns), colnr+1):
			self.dm[self._unique_name] = u''
			item = self.item(0, i)
			if item is None:
				self._setcell(0, i, self._column_names[i])
			for rownr in range(1, len(self.dm)+1):
				item = self.item(rownr, i)
				if item is None:
					self._setcell(rownr, i)
		self._adjust_size()

	def _add_rows(self, rownr):

		for i in range(self.dm.length, rownr+1):
			for colnr in range(len(self.dm.columns)):
				item = self.item(i, colnr)
				if item is None:
					self._setcell(i, colnr)
		self.dm.length = rownr
		self._adjust_size()

	@undoable
	def _remove_columns(self):

		for colnr in self._selected_columns[::-1]:
			del self.dm[self._column_names[colnr]]
		self.refresh()
		self._qdm.changed.emit()

	@undoable
	def _remove_rows(self):

		for row in self._selected_rows[::-1]:
			del self.dm[row]
		self.refresh()
		self._qdm.changed.emit()

	def _rename_column(self, colnr):

		old_name = self._column_names[colnr]
		new_name = self._value(0, colnr)
		if old_name == new_name:
			return
		if new_name in self.dm.column_names:
			new_name = self._unique_name
			self._setcell(0, colnr, new_name)
		try:
			self.dm.rename(old_name, new_name)
			self._qdm.changed.emit()
		except:
			self._setcell(0, colnr, old_name)

	def _change_cell(self, rownr, colnr):

		self._column_by_index(colnr)[rownr-1] = self._value(rownr, colnr)

	@disconnected
	@undoable
	def _on_cell_changed(self, rownr, colnr):

		if colnr >= len(self.dm.columns):
			self._add_columns(colnr)
		if rownr > len(self.dm):
			self._add_rows(rownr)
		if rownr == 0:
			self._rename_column(colnr)
		else:
			self._change_cell(rownr, colnr)
		self.item(rownr, colnr).update_style()
		if not self._silent:
			self._optimize_column_width(colnr)
			self._qdm.cellchanged.emit(rownr, colnr)
			self._qdm.changed.emit()

	def _optimize_column_width(self, colnr):

		self.resizeColumnToContents(colnr)
		if self.columnWidth(colnr) > MAX_COL_WIDTH:
			self.setColumnWidth(colnr, MAX_COL_WIDTH)
		else:
			self.setColumnWidth(colnr, self.columnWidth(colnr)+MARGIN)

	def _setcell(self, rownr, colnr, val=u''):

		item = self.item(rownr, colnr)
		if item is None:
			item = QCell(val)
			self.setItem(rownr, colnr, item)
		else:
			item.setText(safe_decode(val))
		item.update_style()
		if self.read_only:
			item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)

	@property
	def _unique_name(self):

		i = 1
		while True:
			name = u'new_column_%d' % i
			if name not in self._column_names:
				return name
			i += 1

	def _value(self, rownr, colnr):

		return self.item(rownr, colnr).text()

	def _undo(self):

		"""
		desc:
			Reverts to the last state of the undo stack (if any).
		"""

		self._in_undo_action = True
		if not self._undo_stack:
			self._in_undo_action = False
			return
		self._cursor_pos, self.dm = self._undo_stack.pop()
		self._in_undo_action = False
		self.refresh()
		self._qdm.changed.emit()

	def _start_undo_action(self):

		"""
		desc:
			Starts an undo action.
		"""

		if self._in_undo_action:
			return False
		self._add_undo_history()
		self._in_undo_action = True
		return True

	def _end_undo_action(self):

		"""
		desc:
			Ends an undo action.
		"""

		self._in_undo_action = False

	def _clear_undo(self):

		"""
		desc:
			Clears the undo stack.
		"""

		self._undo_stack = []

	def _add_undo_history(self):

		"""
		desc:
			Adds the current state to the undo stack.
		"""

		if not self._in_undo_action:
			self._undo_stack.append( (self._cursor_pos, self.dm[:]) )

	@undoable
	def _cut(self):

		"""
		desc:
			Copies the current selection to the clipboard, and then clears the
			current selection.
		"""

		self._copy(clear=True)

	@undoable
	def _delete(self):

		"""
		desc:
			Clears the current selection.
		"""

		self._copy(clear=True, copy=False)

	@silent
	def _copy(self, clear=False, copy=True):

		"""
		desc:
			Copies the current selection to the clipboard.

		keywords:
			clear:
				desc:	Indicates whether copied cells should be cleared.
				type:	bool
			copy:
				desc:	Indicates whether cells should be copied to the
						clipboard.
				type:	bool
		"""

		# Get the start and end of the selection
		selection = self.selectedRanges()
		if not selection:
			return
		firstrow = min([r.topRow() for r in selection])
		firstcolnr = min([r.leftColumn() for r in selection])
		lastrow = max([r.bottomRow() for r in selection])
		lastcolnr = max([r.rightColumn() for r in selection])
		colspan = lastcolnr - firstcolnr + 1
		rowspan = lastrow - firstrow + 1
		# Create an empty list of lists, where the value __empty__ indicates
		# that there's nothing in it (not even an empty string). This allows us
		# to deal with non-contiguous selections.
		matrix = []
		for col in range(rowspan):
			matrix.append([EMPTY_STR]*colspan)
		# Add all selected cells.
		columns_to_optimize = set()
		for item in self.selectedItems():
			rownr = self.row(item) - firstrow
			if rownr > self._last_visible_row:
				for colnr, (name, col) in enumerate(self.dm.columns):
					try:
						self._setcell(rownr + 1, colnr, col[rownr])
					except IndexError:
						pass  # Appears to happen in rare conditions
					columns_to_optimize.add(colnr)
			colnr = self.column(item) - firstcolnr
			matrix[rownr][colnr] = item.text()
			if clear:
				self._setcell(self.row(item), self.column(item))
		for colnr in columns_to_optimize:
			self._optimize_column_width(colnr)
		if not copy:
			return
		# Convert the selection to text and put it on the clipboard
		txt = u'\n'.join([u'\t'.join(_col) for _col in matrix])
		self._clipboard.setText(txt)

	@silent
	@undoable
	def _paste(self):

		"""
		desc:
			Pastes the current clipboard contents onto the DataFrame.
		"""

		txt = self._clipboard.mimeData().text()
		rows = self.newlines_re.sub('\n', txt).split(u'\n')
		columns = []
		for i, row in enumerate(rows):
			if not row:  # avoid pasting an empty row at the end
				continue
			cells = row.split(u'\t')
			for j, cell in enumerate(cells):
				if cell != EMPTY_STR:
					col = self.currentColumn()
					if col not in columns:
						columns.append(col)
					self._setcell(self.currentRow()+i, col+j, cell)
		for col in columns:
			self._optimize_column_width(col)
		self._qdm.changed.emit()
