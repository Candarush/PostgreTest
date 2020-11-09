import sys
import mytable
import dialog
import change
import psycopg2
from settings import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt, pyqtSlot
from PyQt5 import QtWidgets, QtGui
from addnewpopup import AddNewPopup
from changeentrywindow import ChangeEntryWidnow

conn = psycopg2.connect(dbname=DBNAME, port=PORT,user=USER, password=PASSWORD)
cursor = conn.cursor()

# update для дочерних таблиц.
# добавить LIKE для всех полей ввода к запросу where ( ... where tel like '%запрос%' ).


'''Главное окошко пользовательского интерфейса.'''
class MainApp(QtWidgets.QMainWindow, mytable.Ui_Dialog):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.setup_buttons()
		self.update()
		self.to_start_screen()
		self.MainTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

	'''Обновить главную таблицу и выпадающие списки.'''
	def update(self):
		self.update_table()

	'''Открыть редактирование атрибута таблички, при условии если никакое другое диалоговое окно не открыто.'''
	def showdialog(self, tablename, attributename):
		if hasattr(self, 'msg') and self.msg.isVisible(): return
		self.msg = AddNewPopup(self, tablename, attributename)

	'''Установить функцию клика на кнопку на необходимый метод (для кажой кнопки).'''
	def setup_buttons(self):
		self.CloseButton.clicked.connect(lambda: self.close_app())
		self.NewEntryButton.clicked.connect(lambda: self.add_new_entry())
		self.DeleteEntryButton.clicked.connect(lambda: self.remove_entry())
		self.ChangeEntryButton.clicked.connect(lambda: self.change_entry())
		self.FindEntryButton.clicked.connect(lambda: self.search_entry())
		self.ClearEntryButton.clicked.connect(lambda: self.to_start_screen())

	'''Закрыть это окошко и все диалоговые окна.'''
	def close_app(self):
		if hasattr(self, 'msg'):
			if self.msg.isVisible():
				self.msg.close()
		self.close()

	'''Удалить запись из главной таблицы. Выбор происходит через выделение строчки в главной таблице.'''
	def remove_entry(self):
		if len(self.MainTable.selectionModel().selectedRows()) == 1:
			cursor.execute("delete from main where u_id = %d" % int(self.MainTable.model().data(self.MainTable.selectionModel().selectedRows()[0])))
			conn.commit()
			self.update()
			return
		QMessageBox.warning(self, "Ошибка", "Полностью выделите нужную строку для удаления.")

	'''Добавить новую запись в главную таблицу по заданным значениям в выпадающих списках и полях ввода. Если что-то пошло не так выдать всплывающее окно.'''
	def add_new_entry(self):
		try:
			if  self.familiaBox.currentText()[0] == ' ' or \
				self.nameBox.currentText()[0] == ' ' or \
				self.otcestvoBox.currentText()[0] == ' ' or \
				self.cityBox.currentText()[0] == ' ' or \
				self.streetBox.currentText()[0] == ' ' or \
				self.buildingBox.toPlainText()[0] == ' ' or \
				self.telBox.toPlainText()[0] == ' ':
				raise Exception('Wrong arguements.')
			cursor.execute("insert into main values (default, %d, %d, %d, %d, %d, '%s', '%s', '%s')" % 
				(
				self.get_attribute_uid('fam_tab', 'fam', self.familiaBox.currentText()),
				self.get_attribute_uid('nam_tab', 'nam', self.nameBox.currentText()),
				self.get_attribute_uid('otc_tab', 'otc', self.otcestvoBox.currentText()),
				self.get_attribute_uid('city_tab', 'city', self.cityBox.currentText()),
				self.get_attribute_uid('street_tab', 'street', self.streetBox.currentText()),
				self.corpBox.toPlainText(),
				self.telBox.toPlainText(),
				self.buildingBox.toPlainText(),
			)	)
			conn.commit()
			self.update()
		except:
			QMessageBox.warning(self, "Ошибка", "Проверьте заполнение полей.")

	'''Изменить запись главной таблицы. Выбор записи происходит через выделение строки в гл. таблице.'''
	def change_entry(self):
		if not len(self.MainTable.selectionModel().selectedRows()) == 1:
			QMessageBox.warning(self, "Ошибка", "Полностью выделите нужную строку для изменения.")
			return
		if hasattr(self, 'msg') and self.msg.isVisible(): return
		self.msg = ChangeEntryWidnow(self, int(self.getRowData(0)), self.familiaBox, self.getRowData(1), self.nameBox, self.getRowData(2), self.otcestvoBox, self.getRowData(3), self.cityBox, self.getRowData(4), self.streetBox, self.getRowData(5), self.getRowData(7), self.getRowData(8), self.getRowData(6))

	'''Поиск записей по заполненным полям и выпадающим спискам. При отсутвии значения в полях, они не учитываются при поиске.'''
	def search_entry(self):
		if hasattr(self, 'msg'):
			if self.msg.isVisible():
				return
		combo = {'fam' : self.get_attribute_uid('fam_tab', 'fam', self.familiaBox.currentText()), 'nam' : self.get_attribute_uid('nam_tab', 'nam', self.nameBox.currentText()), 'otc' : self.get_attribute_uid('otc_tab', 'otc', self.otcestvoBox.currentText()), 'city' : self.get_attribute_uid('city_tab', 'city', self.cityBox.currentText()), 'street' : self.get_attribute_uid('street_tab', 'street', self.streetBox.currentText())}
		text = {'corp' : self.corpBox.toPlainText(), 'tel' : self.telBox.toPlainText(), 'bldn' : self.buildingBox.toPlainText()}
		query = 'with res as (select * from main '
		isFirst = True
		ckeys = combo.keys()
		tkeys = text.keys()
		for k in ckeys:
			cursor.execute("select * from %s_tab where %s_id = %d " % (k,k[0],combo[k]))
			fetch = cursor.fetchone()[1][0]
			if not fetch == ' ':
				if isFirst:
					isFirst = False
					query = query + ('where %s = %d ' % (k, combo[k])) 
				else: 
					query = query + ('and %s = %d ' % (k, combo[k])) 
		for k in tkeys:
			if not (text[k]) == '':
				if isFirst:
					isFirst = False
					query = query + ("where %s like '%s' " % (k, text[k])) 
				else: 
					query = query + ("and %s like '%s' " % (k, text[k])) 
		query = query + ')'
		query = query + '''select u_id, fam_tab.fam, nam_tab.nam, otc_tab.otc, city_tab.city, street_tab.street, bldn, corp, tel 
		from res
		join fam_tab on res.fam=fam_tab.f_id
		join nam_tab on res.nam=nam_tab.n_id
		join otc_tab on res.otc=otc_tab.o_id
		join city_tab on res.city=city_tab.c_id
		join street_tab on res.street=street_tab.s_id'''
		cursor.execute(query)
		data = cursor.fetchall()
		self.show_entries_from_data(data)

	'''Установить текущее значение выпадающего списка на значение содержащее text.'''
	def setComboBox(self, box, text):
		index = box.findText(text.ljust(30));
		if not index == -1:
			box.setCurrentIndex(index)

	'''Вернуть все к начальным значениям. Очистить поля и установить значения выпадающих списков на пустые. Выдать все записи на гл. табличке.'''
	def to_start_screen(self):
		self.update_table()
		self.setComboBox(self.familiaBox,' ')
		self.setComboBox(self.nameBox,' ')
		self.setComboBox(self.otcestvoBox,' ')
		self.setComboBox(self.cityBox,' ')
		self.setComboBox(self.streetBox,' ')
		self.corpBox.setText('')
		self.telBox.setText('')
		self.buildingBox.setText('')

	'''Достать значение из таблики QT на выделенной строке и столбику id.'''
	def getRowData(self, id):
		r = self.MainTable.currentRow()
		return self.MainTable.item(r,id).text()
	'''Достать ВСЕ данные из гл. таблице Postgre.'''
	def get_data(self):
		cursor.execute('''
		select u_id, fam_tab.fam, nam_tab.nam, otc_tab.otc, city_tab.city, street_tab.street, bldn, corp, tel
		from main 
		join fam_tab on main.fam=fam_tab.f_id
		join nam_tab on main.nam=nam_tab.n_id
		join otc_tab on main.otc=otc_tab.o_id
		join city_tab on main.city=city_tab.c_id
		join street_tab on main.street=street_tab.s_id
		''')
		result = cursor.fetchall()
		return result

	'''Обновить данные таблички и выпадающих списков.'''
	def update_table(self):
		table = self.MainTable
		self.show_entries_from_data(self.get_data())
		self.update_attributes()

	'''Показать данные соответствующие полям и выпадающим спискам, которые выбрал пользователь.'''
	def show_entries_from_data(self, data):
		table = self.MainTable
		table.setColumnCount(9)
		table.setRowCount(len(data))
		table.setHorizontalHeaderLabels(["Id","Фамилия", "Имя", "Отчество", "Город", "Улица", "Здание", "Корпус", "Телефон"])
		for c_entry in range(len(data)):
			for c_attr in range(9):
				table.setItem(c_entry, c_attr, QTableWidgetItem(str(data[c_entry][c_attr])))
		table.resizeColumnsToContents()

	'''Определить идентификатор атрибута по его значению.'''
	def get_attribute_uid(self, tablename, attributename, value) -> int:
		cursor.execute("select * from %s where %s = '%s'" % (tablename, attributename, value))
		result = cursor.fetchone()
		if result is None:
			raise exception('Аттрибут не найден!')
		return int(result[0])

	'''Обновить все выпадающие списки и кнопки. Создать ссылки на названия таблички и атрибута из родительских таблиц Postgre.'''
	def update_attributes(self):
		self.setup_attribute(self.familiaBox, self.newFamiliaButton, 'fam_tab', 'fam')
		self.setup_attribute(self.nameBox, self.newNameButton, 'nam_tab', 'nam')
		self.setup_attribute(self.otcestvoBox, self.newOtchestvoButton, 'otc_tab', 'otc')
		self.setup_attribute(self.cityBox, self.newCityButton, 'city_tab', 'city')
		self.setup_attribute(self.streetBox, self.newStreetButton, 'street_tab', 'street')

	'''Обновить ссылки для пары из кнопки и списка.'''
	def setup_attribute(self, box, addnew_button, tablename, attributename):
		self.setup_QPushButtton(addnew_button, tablename, attributename)
		self.update_QComboBox(box, tablename, attributename)

	'''Обновить ссылку на необходимый метод для кнопки.'''
	def setup_QPushButtton(self, button, tablename, attributename):
		button.clicked.connect(lambda: self.showdialog(tablename, attributename))

	'''Обновить значения в списке.'''
	def update_QComboBox(self, box, tablename, attributename):
		box.clear()
		cursor.execute('select %s from %s' % (attributename, tablename))
		for n in cursor.fetchall():
			box.addItem(n[0])

def main():
	app = QtWidgets.QApplication(sys.argv)
	window = MainApp()
	window.show()
	app.exec_()

if __name__ == '__main__':
	main()
