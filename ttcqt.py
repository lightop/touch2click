#!/usr/bin/python3

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


buttonData = [
              ('ws1',50,68),
              ('ws2',50,101),
              ('ws3',50,134),
              ('ws4',50,167),
              ('ws5',50,200),
              ('ws6',50,233),
              ('ws7',50,266),
              ('ws8',50,299),
              ('ws9',50,332),
              ('ws10',50,365),

              ('pageplus', 45, 506),
              ('pageminus',45, 678),

              ('flash1',127,586),
              ('flash2',206,586),
              ('flash3',285,586),
              ('flash4',364,586),
              ('flash5',443,586),
              ('flash6',522,586),
              ('flash7',601,586),
              ('flash8',680,586),
              ('flash9',759,586),
              ('flash10',838,586),

              ('swop1',127,545),
              ('swop2',206,545),
              ('swop3',285,545),
              ('swop4',364,545),
              ('swop5',443,545),
              ('swop6',522,545),
              ('swop7',601,545),
              ('swop8',680,545),
              ('swop9',759,545),
              ('swop10',838,545),

              ('intensity',1029,538),
              ('position',1071,538),
              ('color',1113,538),
              ('gobo',1155,538),
              ('beam',1197,538),
              ('effect',1239,538),
              ('special',1281,538),
              ('fx',1323,538),

              ('encoder1up',1074,646),
              ('encoder2up',1188,646),
              ('encoder3up',1304,646),
              ('encoder1down',1074,698),
              ('encoder2down',1188,698),
              ('encoder3down',1304,698),

              ]

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


	def fillItems(self):
		length = len(buttonData)
		self.table.setRowCount(length)
		for row in range (length):
			for column in range(3):
				item = str(buttonData[row][column])
				self.table.setItem(row, column, QTableWidgetItem(item))

		super.statusBar().showMessage("Filled!!!!!!!!!!!")

		



if __name__ == '__main__':

	import sys

	app = QApplication(sys.argv)
	mainWin = MainWindow()
	mainWin.show()
	sys.exit(app.exec_())