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

class ChangeEntryWidnow(QtWidgets.QMainWindow, change.Ui_Dialog):
	def __init__(self, maintable, entry_id, familiaBox, familiaText, nameBox, nameText, otcestvoBox, otcestvoText, cityBox, cityText, streetBox, streetText, corpBox, telBox, buildingBox):
		super().__init__()
		self.maintable = maintable
		self.entry_id = entry_id
		self.setupUi(self)
		self.copy_QComboBox(self.familiaBox, familiaBox)
		self.setComboBox(self.familiaBox, familiaText)
		self.copy_QComboBox(self.nameBox, nameBox)
		self.setComboBox(self.nameBox, nameText)
		self.copy_QComboBox(self.otcestvoBox, otcestvoBox)
		self.setComboBox(self.otcestvoBox, otcestvoText)
		self.copy_QComboBox(self.cityBox, cityBox)
		self.setComboBox(self.cityBox, cityText)
		self.copy_QComboBox(self.streetBox, streetBox)
		self.setComboBox(self.streetBox, streetText)
		self.corpBox.setText(corpBox)
		self.telBox.setText(telBox)
		self.buildingBox.setText(buildingBox)
		self.CloseButton.clicked.connect(lambda: self.close())
		self.ChangeEntryButton.clicked.connect(lambda: self.commitUpdate())
		self.show()

	def copy_QComboBox(self, target, box):
		for n in range(0,box.count()):
			if not box.itemText(n)[0] == ' ':
				target.addItem(box.itemText(n))

	def setComboBox(self, box, text):
		index = box.findText(text);
		if not index == -1:
			box.setCurrentIndex(index)

	def commitUpdate(self):
		try:
			cursor.execute("update main set fam = %d where u_id = %d" % (self.get_attribute_uid('fam_tab', 'fam', self.familiaBox.currentText()), self.entry_id))
			cursor.execute("update main set nam = %d where u_id = %d" % (self.get_attribute_uid('nam_tab', 'nam', self.nameBox.currentText()), self.entry_id))
			cursor.execute("update main set otc = %d where u_id = %d" % (self.get_attribute_uid('otc_tab', 'otc', self.otcestvoBox.currentText()), self.entry_id))
			cursor.execute("update main set city = %d where u_id = %d" % (self.get_attribute_uid('city_tab', 'city', self.cityBox.currentText()), self.entry_id))
			cursor.execute("update main set street = %d where u_id = %d" % (self.get_attribute_uid('street_tab', 'street', self.streetBox.currentText()), self.entry_id))
			cursor.execute("update main set bldn = '%s' where u_id = %d" % (self.buildingBox.toPlainText(), self.entry_id))
			cursor.execute("update main set corp = '%s' where u_id = %d" % (self.corpBox.toPlainText(), self.entry_id))
			cursor.execute("update main set tel = '%s' where u_id = %d" % (self.telBox.toPlainText(), self.entry_id))
			conn.commit()
			self.maintable.update()
			self.close()
		except:
			pass
	
	def get_attribute_uid(self, tablename, attributename, value) -> int:
		cursor.execute("select * from %s where %s = '%s'" % (tablename, attributename, value))
		result = cursor.fetchone()
		if result is None:
			raise exception('Аттрибут не найден!')
		return int(result[0])