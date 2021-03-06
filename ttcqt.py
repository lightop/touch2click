#!/usr/bin/python3


# MIT License

# Copyright (c) 2018 Vassily Leushin

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
#import netifaces
import psutil
import sys
from asyncqt import QEventLoop, QThreadExecutor

pyautogui.PAUSE = 0.01 #Vasya! Don't you ever forget about this!

buttonData = []
faderData =[]
encoderData = []
keyData = []



buttons = []
faders = []
encoders = []
keys = []

prefix = 'none'


data = {
  
  "prefix":prefix,
  "faderData":faderData,
  "encoderData":encoderData,
  "buttonData":buttonData,
  "keyData":keyData
}

#print (data)




#dgw = netifaces.gateways()['default'][netifaces.AF_INET][1]
#ip = netifaces.ifaddresses(dgw)[netifaces.AF_INET][0]['addr']
# ip = "127.0.0.1"
# port = 8000


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		self.setWindowTitle("Touch2Click v0.07")
		self.resize(550,400)

		self.times = 0
		self.data = data
		self.ip = "127.0.0.1"
		self.port = 8000

		#self.dispatcher = dispatcher.Dispatcher()
		# self.loop = asyncio.get_event_loop()
		# self.server = osc_server.AsyncIOOSCUDPServer((ip, port), dispatcher, self.loop)

		self.buttonTable = TTCTab(['Index', 'X-Click', 'Y-Click',])
		self.faderTable = TTCTab(['Index', 'X-Zero','Y-Zero','X-Full', 'Y-Full'])
		self.encoderTable = TTCTab(['Index', 'X-Center','Y-Center','X-Step', 'Y-Step'])
		self.keyTable = TTCTab(['Index', 'Keys'])

		self.testTable = TTCTab(['1','2','3'])

		self.setup = SetupTab(self)

		self.tabwidget = QTabWidget()

		self.tabwidget.addTab(self.setup, "Setup")

		self.tabwidget.addTab(self.buttonTable,"Buttons")
		self.tabwidget.addTab(self.faderTable,"Faders")
		self.tabwidget.addTab(self.encoderTable,"Encoders")
		self.tabwidget.addTab(self.keyTable,"Keys")
		self.tabwidget.addTab(QLabel("Not yet implemented..."),"Grids")

		
		
		
		self.setCentralWidget(self.tabwidget)
		self.statusBar = self.statusBar()
		self.statusBar.showMessage("Address: {}".format((self.ip, self.port)))
		self.createActions()
		self.createMenus()

		self.toolBar = self.addToolBar("fgfd")
		
		testAct = QAction('Start',self)
		self.toolBar.addAction(self.startAct)
		test2Act = QAction('Hide',self)
		self.toolBar.addAction(self.hideAct)

		test3Act = QAction('Stop',self)
		self.toolBar.addAction(self.stopAct)

		self.tray = QSystemTrayIcon(self)
		self.tray.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
		traymenu = QMenu()
		traymenu.addAction(self.showAct)
		traymenu.addAction(self.hideAct)
		traymenu.addAction(self.quitAct)
		self.tray.setContextMenu(traymenu)
		self.tray.setIcon(QIcon("ttc.ico"))
		self.tray.show()

		#self.servThread = ServerThread()

	
		
	def gen_osc_addr (type, number):
		osc_addr = "/" + prefix + "/" + type +"/"+str(number)
		print (osc_addr)
		return (osc_addr)


	def open(self):
		filename, _ = QFileDialog.getOpenFileName(
			self, "Open file", 
			'~/git/touch2click',
			"T2C Files (*.t2c);;YAML Files (*.yaml)")
		print (filename)
		print (self.data)
		with open (filename, 'r') as f:
			self.data = yaml.load (f)
			prefix = self.data['prefix']
			buttonData= self.data ['buttonData']
			faderData = self.data ['faderData']
			encoderData = self.data ['encoderData']
			keyData = self.data ['keyData']


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
		filename, _ = QFileDialog.getSaveFileName(
			self, "Save File","","T2C Files (*.t2c);;YAML Files (*.yaml);;All Files (*)")
		if filename :
			with open (filename, 'w') as f:
				yaml.safe_dump(self.data, f)
		print (self.data)

	def fill(self):
		self.buttonTable.fillItems()


	def hides(self):
		self.hide()
		time.sleep(3)
		self.show()

	def startServer (self):
		#self.loop = asyncio.get_event_loop()
		self.server = osc_server.AsyncIOOSCUDPServer((self.ip, self.port), dispatcher, loop)
		self.server.serve()
		#self.servThread = ServerThread()
		#self.servThread.start()
		#self.loop.run_forever()
		#asyncio.set_event_loop(loop)

		with loop:
			loop.run_forever()

		
	def start2Server (self):
		self.server2.start()

	def stopServer(self):
		self.loop.close()

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
		self.stopAct = QAction ('Stop', self, triggered =self.stopServer)
		self.start2Act = QAction ('Start', self, triggered = self.start2Server)


	def createMenus(self):
		self.fileMenu = self.menuBar().addMenu("&File")
		self.fileMenu.addAction(self.openAct)
		self.fileMenu.addAction(self.saveAct)
		self.fileMenu.addAction(self.fillAct)
		self.fileMenu.addSeparator()
		self.fileMenu.addAction(self.exitAct)

		self.runMenu =self.menuBar().addMenu("&Run")

class TTCTab(QWidget):
	def __init__(self,*args):
		super(QWidget,self).__init__()
		layout = QGridLayout()

		self.columns = len(*args)
		
		self.setLayout(layout)
		self.table =QTableWidget()
		self.table.setRowCount(1)
		self.table.setColumnCount(len(*args))
		self.table.setHorizontalHeaderLabels(*args)
		self.table.resizeColumnsToContents()
		layout.addWidget(self.table,0,0)

		buttonWidget = QWidget()
		buttonLayout = QGridLayout()

		self.insButton = QPushButton ("Insert")
		buttonLayout.addWidget(self.insButton,0,0)
		self.delButton = QPushButton("Delete")
		buttonLayout.addWidget(self.delButton,0,1)
		self.someButton = QPushButton ("Any Key")
		buttonLayout.addWidget(self.someButton,0,2)
		
		buttonWidget.setLayout(buttonLayout)
		layout.addWidget(buttonWidget,1,0)

		
	def fillItems(self, data):
		length = len(data)
		self.table.setRowCount(length)
		for row in range (length):
			for column in range(self.columns):
				item = str(data[row][column])
				self.table.setItem(row, column, QTableWidgetItem(item))
				self.table.item(row, column).setTextAlignment(Qt.AlignCenter)
		self.table.resizeColumnsToContents()

class TTCClass(TTCTab):
	def __init__(self,*args):
		TTCTab.__init__(self, *args)

class SetupTab(QWidget):
	def __init__(self, parent):
		super(QWidget,self).__init__(parent)
		layout = QFormLayout()
		print (parent)
		self.parent = parent
		addressLabel = QLabel("Address")
		# addressLine = QLineEdit()
		# addressLine.setText(str(ip))
		# layout.addRow (addressLabel,addressLine)
		addressList = QComboBox()
		
		addresses = psutil.net_if_addrs()
		print (addresses)
		stats = psutil.net_if_stats()
		print (stats)

		available_networks = []
		for intface, addr_list in addresses.items():
			if any(getattr(addr, 'address').startswith("169.254") for addr in addr_list):
				continue
			elif intface in stats and getattr(stats[intface], "isup"):
				for addr in addr_list:
					addressList.addItem(getattr(addr, 'address'))
		addressList.activated[str].connect(self.onChanged)
		layout.addRow (addressLabel,addressList)

		portLabel = QLabel("Port")
		portLine = QLineEdit()
		portLine.setText(str(self.parent.port))
		portLine.textChanged.connect(self.textChanged)
		layout.addRow (portLabel,portLine)

		prefixLabel = QLabel("Prefix")
		prefixLine = QLineEdit()
		layout.addRow (prefixLabel, prefixLine)

		self.setLayout(layout)

	def onChanged(self, text):
		print (self.parent.ip)
		self.parent.ip = text
		print (text)
		self.parent.statusBar.showMessage("Address: {}".format((self.parent.ip, self.parent.port)))

	def textChanged (self, text):
		print (self.parent.port)
		self.parent.port = text
		self.parent.statusBar.showMessage("Address: {}".format((self.parent.ip, self.parent.port)))





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
    print ("")
    pyautogui.moveTo(self.x_zero - self.x_level, self.y_zero-self.y_level)
    

  def handler_z (self, unused_addr,args, volume):
    if (volume == 1): 
      pyautogui.mouseDown(self.x_zero - self.x_level,self.y_zero - self.y_level)
      
    if (volume == 0):
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

  	elif volume == 0.0:
  		return
 
class ServerThread (QThread):
	def __init__(self):
		super().__init__()

	def __del__(self):
		self.wait()

	def run(self):
		#server.serve()
		print ("11111111111111111111")
		loop.run_forever()
		print ("dgdfgdf")

	# def quit(self):
	# 	#self.server.stop()
	# 	print (loop.is_running)
	# 	loop.stop()
	# 	#loop.close()
	# 	print (loop.is_running)
	# 	#self.terminate()

if __name__ == '__main__':

	

	

	dispatcher = dispatcher.Dispatcher()
	# server = osc_server.AsyncIOOSCUDPServer(
	# 	(ip, port), dispatcher, loop)
	#print (server)
	#server.serve()
	#loop.stop()
	app = QApplication(sys.argv)
	loop = QEventLoop (app)
	app.setStyle("plastique")
	mainWin = MainWindow()

	mainWin.show()
	sys.exit(app.exec_())