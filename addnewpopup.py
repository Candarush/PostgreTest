import sys
import mytable
import dialog
import change
import psycopg2
from settings import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt, pyqtSlot
from PyQt5 import QtWidgets, QtGui

conn = psycopg2.connect(dbname=DBNAME, port=PORT,user=USER, password=PASSWORD)
cursor = conn.cursor()

class AddNewPopup(QtWidgets.QMainWindow, dialog.Ui_Dialog):
	def __init__(self, window, tablename, attributename):
		self.window = window
		self.tablename = tablename
		self.attributename = attributename
		super().__init__()
		self.setupUi(self)
		self.update_QList()
		self.closeButton.clicked.connect(lambda: self.close())
		self.newEntryButton.clicked.connect(lambda: self.new_entry())
		self.removeEntryButton.clicked.connect(lambda: self.remove_entry())
		self.listView.selectionModel().selectionChanged.connect(lambda: self.on_item_selected())
		self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers);
		self.show()

	def on_item_selected(self):
		self.lineEdit.setText(str(self.listView.selectionModel().selection().indexes()[0].data()))

	def new_entry(self):
		try:
			cursor.execute("select * from %s where %s = '%s'" % (self.tablename, self.attributename, self.lineEdit.text()))
			result = cursor.fetchone()
			if result is None:
				cursor.execute("insert into %s values(default, '%s')" % (self.tablename, self.lineEdit.text()))
				conn.commit()
				self.update_QList()
				self.window.update()
		except:
			pass

	def remove_entry(self):
		try:
			if self.lineEdit.text()[0] == ' ':
				return
			cursor.execute("select * from %s where %s = '%s'" % (self.tablename, self.attributename, self.lineEdit.text()))
			result = cursor.fetchone()
			if result is None:
				return
			cursor.execute("delete from %s where %s = '%s'" % (self.tablename, self.attributename, self.lineEdit.text()))
			conn.commit()
			self.update_QList()
			self.window.update()
		except:
			pass

	def update_QList(self):
		model = QtGui.QStandardItemModel()
		self.listView.setModel(model)
		cursor.execute('select %s from %s' % (self.attributename, self.tablename))
		for n in cursor.fetchall():
			if n[0][0] != ' ':
				model.appendRow(QtGui.QStandardItem(n[0]))
		self.listView.setModel(model)
