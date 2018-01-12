#!/usr/bin/python3

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import yaml

buttonData = []


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		self.setWindowTitle("Touch2Click v0.01")
		self.resize(400,600)

		self.times = 0

		self.buttonTable = ButtonTab()

		self.tabwidget = QTabWidget()
		self.tabwidget.addTab(self.buttonTable,"Buttons")
		self.tabwidget.addTab(QLabel(""),"Faders")
		self.tabwidget.addTab(QLabel(""),"Encoders")
		self.tabwidget.addTab(QLabel(""),"Keys")
		self.tabwidget.addTab(QLabel(""),"Grids")

		self.setCentralWidget(self.tabwidget)

		self.statusBar().showMessage("Touch to click!!!")

		self.createActions()
		self.createMenus()


	def open(self):
		filename, _ = QFileDialog.getOpenFileName(self)
		print (filename)
		with open (filename, 'r') as f:
			data = yaml.load (f)
			buttonData= data ['buttonData']
			print (len(buttonData))
			self.buttonTable.fillItems(buttonData)
			

	def save(self):
		print ("Saved  "+str(self.times))
		self.times +=1
		print (buttonData)

	def fill(self):
		self.buttonTable.fillItems()



	def closeEvent(self,event):
		print ("Goodbye!!")
		event.accept()

	def createActions(self):

		self.openAct = QAction("&Open...", self, 
			shortcut=QKeySequence.Open, triggered=self.open)

		self.exitAct = QAction("E&xit", self, 
			shortcut="Ctrl+Q", triggered=self.close)

		self.saveAct = QAction("&Save", self, triggered=self.save)

		self.fillAct =QAction("&Fill", self, triggered=self.fill)



	def createMenus(self):
		self.fileMenu = self.menuBar().addMenu("&File")
		self.fileMenu.addAction(self.openAct)
		self.fileMenu.addAction(self.saveAct)
		self.fileMenu.addAction(self.fillAct)
		self.fileMenu.addSeparator()
		self.fileMenu.addAction(self.exitAct)

		self.runMenu =self.menuBar().addMenu("&Run")

class ButtonTab(QWidget):
	def __init__(self):
		super(QWidget,self).__init__()
		layout = QGridLayout()
		self.setLayout(layout)
		self.table = QTableWidget()
		self.table.setRowCount (0)
		self.table.setColumnCount (3)
		self.table.setHorizontalHeaderLabels(['Name', 'X Click', 'Y Click',])

		layout.addWidget(self.table,0,0)


	def fillItems(self, buttonData):
		length = len(buttonData)
		self.table.setRowCount(length)
		for row in range (length):
			for column in range(3):
				item = str(buttonData[row][column])
				self.table.setItem(row, column, QTableWidgetItem(item))

		



if __name__ == '__main__':

	import sys

	app = QApplication(sys.argv)
	mainWin = MainWindow()
	mainWin.show()
	sys.exit(app.exec_())