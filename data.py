import argparse
import math
import pyautogui
from pythonosc import dispatcher
from pythonosc import osc_server
import asyncio
import json

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
prefix = "avo"

faderData = [
              (1,135,840,135,760),
              (2,240,840,240,760),
              (3,345,840,345,760),
              (4,450,840,450,760),
              (5,555,840,555,760),
              (6,660,840,660,760),
              (7,765,840,765,760),
              (8,870,840,870,760),
              (9,975,840,975,760),
              (10,1080,840,1080,760),

              ]

encoderData = [

              ('A',40,172),
              ('B',40,262),
              ('C',40,352),

              ]

buttonData = [
              
              
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
           ('',['']),
           
           


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
           ('system', ['alt', 'shift','l']),
           ('view', ['alt', 'v']),
           ('go', ['alt', 'g']),
           ('delete', ['alt', 'd']),
           ('shape', ['alt', 's']),
           





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

  def __init__(self, number,x,y):
    self.number = number
    self.x = x
    self.y = y
    self.type = "encoder"
    self.osc_addr = gen_osc_addr(self.type, self.number)
    dispatcher.map (self.osc_addr, self.handler,self.x, self.y)
    dispatcher.map (self.osc_addr+"/z", self.handler_z, self.x, self.y)

  def handler(self,unused_addr,args,volume):
    if (volume == 1.0):
      try:
        pyautogui.moveRel(0,1)
      except (RuntimeError,ValueError): pass
    
    if (volume == 0.0):
      try:
        pyautogui.moveRel(0,-1)
      except (RuntimeError,ValueError): pass

  def handler_z(self, unused_addr, args, volume):
    
    if (volume == 1.0):
      try:
        pyautogui.mouseDown (args[0], args[1])
      except (RuntimeError,ValueError): pass
    
    if (volume == 0.0):
      try:
        pyautogui.mouseUp()
      except (RuntimeError,ValueError): pass


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
  

  
def b_handler (unused_addr,args,volume):
  if volume == 1.0 :
    pyautogui.click (args[0], args[1])
  
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="192.168.1.123", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=8000, help="The port to listen on")
  parser.add_argument ("--file", help="Filename")
  args = parser.parse_args()
  dispatcher = dispatcher.Dispatcher()

  with open (args.file, 'r') as f:
    dd = json.load (f)

  print (dd)
  
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
