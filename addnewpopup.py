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
		self.listView.doubleClicked.connect(lambda: self.on_item_start_editing())
		self.listView.itemChanged.connect(lambda: self.on_item_renamed())
		self.show()

	def on_item_start_editing(self):
		self.prev_text = str(self.listView.selectionModel().selection().indexes()[0].data())

	def on_item_renamed(self):
		if (len(self.listView.selectionModel().selection().indexes()) > 0):
			new_text = str(self.listView.selectionModel().selection().indexes()[0].data())
			print(self.prev_text + ' -> ' + new_text)
			self.change_entry(self.prev_text, new_text)

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

	def change_entry(self, prev_text, new_text):
		try:
			cursor.execute("update %s set %s = '%s' where %s = %d" % (self.tablename, self.attributename, new_text, self.tablename[0]+'_id', self.get_attribute_uid(self.tablename, self.attributename, prev_text)))
			conn.commit()
			self.update_QList()
			self.window.update()
		except:
			pass

	def get_attribute_uid(self, tablename, attributename, value) -> int:
		cursor.execute("select * from %s where %s = '%s'" % (tablename, attributename, value))
		result = cursor.fetchone()
		if result is None:
			raise exception('Аттрибут не найден!')
		return int(result[0])

	def update_QList(self):
		self.listView.clear()
		cursor.execute('select %s from %s' % (self.attributename, self.tablename))
		for n in cursor.fetchall():
			if n[0][0] != ' ':
				self.listView.addItem(n[0])
		for index in range(self.listView.count()):
			item = self.listView.item(index)
			item.setFlags(item.flags() | Qt.ItemIsEditable)
