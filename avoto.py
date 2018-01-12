import argparse
import math
import pyautogui
from pythonosc import dispatcher
from pythonosc import osc_server
import asyncio
import json

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
PREFIX = "avo"

faderData = [
              (1,127,702,127,620),
              (2,206,702,206,620),
              (3,285,702,285,620),
              (4,364,702,364,620),
              (5,443,702,443,620),
              (6,522,702,522,620),
              (7,601,702,601,620),
              (8,680,702,680,620),
              (9,759,702,759,620),
              (10,838,702,838,620),

              ]

encoderData = [

              (1,1070,580,10,0),
              (2,1190,580,10,0),
              (3,1310,580,10,0),

              ]

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

keyData = [
           
           ('A', ['alt','1']),
           ('B', ['alt','2']),
           ('C', ['alt','3']),
           ('D', ['alt','4']),
           ('E', ['alt','5']),
           ('F', ['alt','6']),
           ('G', ['alt', '7']),

           ('1',['1']),
           ('2',['2']),
           ('3',['3']),
           ('4',['4']),
           ('5',['5']),
           ('6',['6']),
           ('7',['7']),
           ('8',['8']),
           ('9',['9']),
           ('0',['0']),

           ('enter',['enter']),
           ('exit',['esc']),
           ('avo',['alt', 'a']),
           ('clear',['alt','c']),

           ('f1', ['f1']),
           ('f2', ['f2']),
           
           ('f3', ['f3']),
           ('f3s', ['shift','f3']),
           
           ('f4', ['f4']),
           ('f4s', ['shift','f4']),
           
           ('f5', ['f5']),
           ('f5s', ['shift','f5']),
           
           ('f6', ['f6']),
           ('f7', ['f7']),
           ('f8', ['f8']),
           ('f9', ['f9']),
           ('f10', ['f10']),
           ('f11', ['f11']),
           ('f12', ['f12']),
           

           ('fixture',['alt','shift','f']),
           ('palette',['alt','shit','p']),
           ('macro',['alt','shift','m']),
           ('group',['alt','shift','g']),
           ('thro',['divide']),
           ('at',['multiply']),
           ('not',['subtract']),
           ('and',['add']),
           ('undo',['ctrl','z']),
           ('record',['alt','r']),
           ('locate', ['alt', 'l']),
           ('patch', ['alt','p']),
           ('disk', ['alt', 'shift','d']),
           ('system', ['alt', 'shift','s']),
           ('view', ['alt','v']),
           ('go', ['alt', 'g']),
           ('delete', ['alt', 'd']),
           ('copy', ['alt','shift','c']),
           ('move', ['alt', 'm']),
           ('unfold', ['alt','u']),
           ('include', ['alt', 'i']),
           ('release', ['alt','shift','r']),
           ('shape', ['alt', 's']),
           ('mlmenu', ['alt', 't']),
           ('blind', ['alt','b']),
           ('off', ['alt','o']),
           ('fan', ['alt', 'f']),
           ('options', ['alt','shift','o']),
           ('latch', ['alt','shift','l']),
           ('fixprev', ['alt', 'left']),
           ('fixnext', ['alt', 'right']),
           ('all', ['alt','up']),
           ('highlight', ['alt', 'down']),



]

def gen_osc_addr (type, number):
  osc_addr = "/" + PREFIX + "/" + type +"/"+str(number)
  print (osc_addr)
  return (osc_addr)

def store_data (filename):
  print (filename)
  data = (buttonData, faderData, keyData, encoderData)
  #self.filename = filename
  with open (filename, 'w') as f:
    json.dump(data, f, indent = 2)



class TTCButton ():

  def __init__(self,number,x,y):
    self.number = number
    self.x = x
    self.y = y
    self.type = "button"
    self.osc_addr = gen_osc_addr(self.type, self.number)
    dispatcher.map (self.osc_addr, self.handler, x, y )

  def handler (self, unused_addr,args, volume):
    if volume == 1.0:  
      pyautogui.mouseDown (args[0], args[1])
    if volume == 0.0:
      pyautogui.mouseUp ()


class TTCFader ():
  
  def __init__(self, number, x_zero, y_zero, x_full, y_full):
    self.number = number
    self.x_zero = x_zero
    self.y_zero = y_zero
    self.x_full = x_full
    self.y_full = y_full
    self.y_size = self.y_zero - self.y_full
    self.x_size = self.x_zero - self.x_full
    self.type = "fader"
    self.x_level = 0
    self.y_level = 0
    self.osc_addr = gen_osc_addr (self.type, self.number)
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

  def __init__(self, number,x,y,h,v):
    self.number = number
    self.x = x
    self.y = y
    self.h = h
    self.v = v
    self.type = "encoder"
    self.osc_addr = gen_osc_addr(self.type, self.number)
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

  def __init__(self,number,key):
    self.number = number
    self.key = key
    self.type = "button"
    self.osc_addr = gen_osc_addr(self.type, self.number)
    dispatcher.map (self.osc_addr, self.handler, self.key )

  def handler (self, unused_addr,args, volume):
    if volume == 1.0 :
       pyautogui.hotkey (*args[0], interval = 0.1)
       print (*args[0])
    #    for i in args[0]:
    #     pyautogui.keyDown (i)
    #     print (i)
    # if volume == 0.0:
    #   for i in args[0]:
    #     pyautogui.keyUp (i)
    #     print (i)
  

  
# def b_handler (unused_addr,args,volume):
#   if volume == 1.0 :
#     pyautogui.click (args[0], args[1])
  
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="192.168.1.123", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=8000, help="The port to listen on")
  parser.add_argument ("--file", help="Filename")
  args = parser.parse_args()
  dispatcher = dispatcher.Dispatcher()

  
  
  faders = []
  for x in faderData:
    f= TTCFader (*x)
    faders.append (f)

  encoders =[]
  for x in encoderData:
    e = TTCEncoder (*x)
    encoders.append (e)

  buttons = []
  for x in buttonData:
    b = TTCButton (*x)
    buttons.append(b)

  keys = []
  #print (keyData)
  for x,y in keyData:
    k = TTCKey (x, y)

  


loop = asyncio.get_event_loop()
server = osc_server.AsyncIOOSCUDPServer((args.ip, args.port), dispatcher, loop)
print ("Serving on {}".format((args.ip, args.port)))
server.serve()
loop.run_forever()
