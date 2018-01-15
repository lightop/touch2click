#!/usr/bin/python3

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import yaml
import time
import argparse
import math
import pyautogui
from pythonosc import dispatcher
from pythonosc import osc_server
import asyncio
import netifaces

pyautogui.PAUSE = 0.01 #Vasya! Don't you ever forget about this!

buttonData = []
faderData =[]
encoderData = []
keyData = []

buttons = []
faders = []
encoders = []
keys = []

global prefix







dgw = netifaces.gateways()['default'][netifaces.AF_INET][1]
ip = netifaces.ifaddresses(dgw)[netifaces.AF_INET][0]['addr']
port = 8000


# def gen_osc_addr (type, number):
# 		osc_addr = "/" + prefix + "/" + type +"/"+str(number)
# 		print (osc_addr)
# 		return (osc_addr)



class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		self.setWindowTitle("Touch2Click v0.01")
		self.resize(550,400)

		self.times = 0

		self.buttonTable = ButtonTab()
		self.faderTable = FaderTab()
		self.encoderTable = EncoderTab()
		self.keyTable = KeyTab()

		self.tabwidget = QTabWidget()
		self.tabwidget.addTab(self.buttonTable,"Buttons")
		self.tabwidget.addTab(self.faderTable,"Faders")
		self.tabwidget.addTab(self.encoderTable,"Encoders")
		self.tabwidget.addTab(self.keyTable,"Keys")
		self.tabwidget.addTab(QLabel("Not yet implemented..."),"Grids")
		
		
		self.setCentralWidget(self.tabwidget)

		self.statusBar().showMessage("Touch to click!!!")
		self.createActions()
		self.createMenus()

		self.toolBar = self.addToolBar("fgfd")
		
		testAct = QAction('Start',self)
		self.toolBar.addAction(self.startAct)
		test2Act = QAction('Start2',self)
		self.toolBar.addAction(self.start2Act)

		self.tray = QSystemTrayIcon(self)
		self.tray.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
		traymenu = QMenu()
		traymenu.addAction(self.showAct)
		traymenu.addAction(self.hideAct)
		traymenu.addAction(self.quitAct)
		self.tray.setContextMenu(traymenu)
		self.tray.setIcon(QIcon("ttc.ico"))
		self.tray.show()

		self.server = ServerThread()
		
	def gen_osc_addr (type, number):
		osc_addr = "/" + prefix + "/" + type +"/"+str(number)
		print (osc_addr)
		return (osc_addr)


	def open(self):
		filename, _ = QFileDialog.getOpenFileName(self)
		print (filename)
		with open (filename, 'r') as f:
			data = yaml.load (f)
			prefix = data['prefix']
			buttonData= data ['buttonData']
			faderData = data ['faderData']
			encoderData = data ['encoderData']
			keyData = data ['keyData']
			

			for x in faderData:
				f= TTCFader (prefix,*x)
				faders.append (f)

			for x in encoderData:
				e = TTCEncoder (prefix,*x)
				encoders.append (e)

			for x in buttonData:
				b = TTCButton (prefix, *x)
				buttons.append(b)

			for x,y in keyData:
				k = TTCKey (prefix,x, y)
				keys.append(k)

			print (prefix)
			self.buttonTable.fillItems(buttonData)
			self.faderTable.fillItems(faderData)
			self.encoderTable.fillItems(encoderData)
			self.keyTable.fillItems(keyData)
			

	def save(self):
		print ("Saved  "+str(self.times))
		self.times +=1
		print (buttonData)

	def fill(self):
		self.buttonTable.fillItems()


	def hides(self):
		self.hide()
		time.sleep(3)
		self.show()

	def startServer (self):
		self.server.start()
		
	def start2Server (self):
		self.server2.start()

	def closeEvent(self,event):
		print ("Goodbye!!")
		event.accept()

	def createActions(self):

		self.openAct = QAction("&Open...", self, 
			shortcut=QKeySequence.Open, triggered=self.open)

		self.exitAct = QAction("E&xit", self, 
			shortcut="Ctrl+Q", triggered=self.close)

		self.saveAct = QAction("&Save", self, triggered=self.save)
		self.fillAct = QAction("&Fill", self, triggered=self.fill)
		self.showAct = QAction('Show', self, triggered = self.show)
		self.hideAct = QAction('Hide', self, triggered = self.hide)
		self.quitAct = QAction('Quit', self, triggered=qApp.quit)
		self.startAct = QAction ('Start', self, triggered = self.startServer)
		self.start2Act = QAction ('Start', self, triggered = self.start2Server)


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
		self.table.setHorizontalHeaderLabels(
			['Index', 'X-Click', 'Y-Click',])
		self.table.resizeColumnsToContents()

		layout.addWidget(self.table,0,0)


	def fillItems(self, buttonData):
		length = len(buttonData)
		self.table.setRowCount(length)
		for row in range (length):
			for column in range(3):
				item = str(buttonData[row][column])
				self.table.setItem(row, column, QTableWidgetItem(item))

class FaderTab (QWidget):
	def __init__(self):
		super(QWidget,self).__init__()
		layout = QGridLayout()
		self.setLayout(layout)
		self.table =QTableWidget()
		self.table.setRowCount(0)
		self.table.setColumnCount(5)
		self.table.setHorizontalHeaderLabels(
			['Index', 'X-Zero','Y-Zero','X-Full', 'Y-Full'])
		self.table.resizeColumnsToContents()
		layout.addWidget(self.table,0,0)
	
	def fillItems(self, faderData):
		length = len(faderData)
		self.table.setRowCount(length)
		for row in range (length):
			for column in range(5):
				item = str(faderData[row][column])
				print (item)
				self.table.setItem(row, column, QTableWidgetItem(item))

class EncoderTab (QWidget):
	def __init__(self):
		super(QWidget,self).__init__()
		layout = QGridLayout()
		self.setLayout(layout)
		self.table =QTableWidget()
		self.table.setRowCount(0)
		self.table.setColumnCount(5)
		self.table.setHorizontalHeaderLabels(
			['Index', 'X-Center','Y-Center','X-Step', 'Y-Step'])
		self.table.resizeColumnsToContents()
		layout.addWidget(self.table,0,0)
	
	def fillItems(self, encoderData):
		length = len(encoderData)
		self.table.setRowCount(length)
		for row in range (length):
			for column in range(5):
				item = str(encoderData[row][column])
				print (item)
				self.table.setItem(row, column, 
					QTableWidgetItem(item))

class KeyTab (QWidget):
	def __init__(self):
		super(QWidget,self).__init__()
		layout = QGridLayout()
		self.setLayout(layout)
		self.table =QTableWidget()
		self.table.setRowCount(0)
		self.table.setColumnCount(2)
		self.table.setHorizontalHeaderLabels(
			['Index', 'Keys'])
		layout.addWidget(self.table,0,0)
		self.table.resizeColumnsToContents()
	
	def fillItems(self, keyData):
		length = len(keyData)
		self.table.setRowCount(length)
		for row in range (length):
			for column in range(2):
				item = str(keyData[row][column])
				print (item)
				self.table.setItem(row, column, 
					QTableWidgetItem(item))



class TTCButton ():

  def __init__(self,prefix,number,x,y):
    self.number = number
    self.x = x
    self.y = y
    self.type = "button"
    self.osc_addr =   "/" + prefix + "/" + self.type +"/"+str(self.number)
    dispatcher.map (self.osc_addr, self.handler, x, y )

  def handler (self, unused_addr,args, volume):
    if volume == 1.0:  
      pyautogui.mouseDown (args[0], args[1])
    if volume == 0.0:
      pyautogui.mouseUp ()


class TTCFader ():
  
  def __init__(self, prefix,number, x_zero, y_zero, x_full, y_full):
    self.number = number
    self.x_zero = x_zero
    self.y_zero = y_zero
    self.x_full = x_full
    self.y_full = y_full
    self.prefix = prefix
    self.y_size = self.y_zero - self.y_full
    self.x_size = self.x_zero - self.x_full
    self.type = "fader"
    self.x_level = 0
    self.y_level = 0
    self.osc_addr =  "/" + self.prefix + "/" + self.type +"/"+str(self.number)
    print (self.osc_addr)
    dispatcher.map (self.osc_addr, self.handler, self.x_zero, self.y_zero)
    dispatcher.map (self.osc_addr+"/z",self.handler_z, self.x_zero, self.y_zero)

  def handler (self, unused_addr, args, volume):
    self.y_level = volume*self.y_size
    self.x_level = volume*self.x_size
    pyautogui.moveTo(self.x_zero - self.x_level, self.y_zero-self.y_level)
    

  def handler_z (self, unused_addr,args, volume):
    if (volume == 1): 
      pyautogui.mouseDown(self.x_zero - self.x_level,self.y_zero - self.y_level)
      
    if (volume ==0):
      pyautogui.mouseUp()


class TTCEncoder ():

  def __init__(self, prefix,number,x,y,h,v):
    self.number = number
    self.x = x
    self.y = y
    self.h = h
    self.v = v
    self.type = "encoder"
    self.osc_addr =  "/" + prefix + "/" + self.type +"/"+str(self.number)
    dispatcher.map (self.osc_addr, self.handler,self.x, self.y)
    dispatcher.map (self.osc_addr+"/z", self.handler_z, self.x, self.y)

  def handler(self,unused_addr,args,volume):
    if (volume == 1.0):
      try:
        pyautogui.moveRel(self.h, self.v)
      except (RuntimeError,ValueError): pass
    
    if (volume == 0.0):
      try:
        pyautogui.moveRel(self.h*-1,self.v*-1)
      except (RuntimeError,ValueError): pass

  def handler_z(self, unused_addr, args, volume):
    
    if (volume == 1.0):
      try:
        pyautogui.mouseDown (args[0], args[1])
      except (RuntimeError,ValueError): pass
    
    if (volume == 0.0):
      try:
        pyautogui.mouseUp()
      except (RuntfimeError,ValueError): pass



class TTCKey ():

  def __init__(self,prefix,number,key):
    self.number = number
    self.key = key
    self.type = "button"
    self.osc_addr =  "/" + prefix + "/" + self.type +"/"+str(self.number)
    dispatcher.map (self.osc_addr, self.handler, self.key )

  def handler (self, unused_addr,args, volume):
    if volume == 1.0 :
       pyautogui.hotkey (*args[0], interval = 0.1)
       #    for i in args[0]:
    #     pyautogui.keyDown (i)
    #     print (i)
    # if volume == 0.0:
    #   for i in args[0]:
    #     pyautogui.keyUp (i)
    #     print (i)


class ServerThread (QThread):
	def __init__(self):
		QThread.__init__(self)

	def __del__(self):
		self.wait()

	def run(self):
		server.serve()
		loop.run_forever()



  

  




if __name__ == '__main__':

	import sys


	dispatcher = dispatcher.Dispatcher()
	loop = asyncio.get_event_loop()
	server = osc_server.AsyncIOOSCUDPServer(
		(ip, port), dispatcher, loop)
	app = QApplication(sys.argv)
	mainWin = MainWindow()
	mainWin.show()
	sys.exit(app.exec_())