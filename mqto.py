import argparse
import math
import pyautogui
from pythonosc import dispatcher
from pythonosc import osc_server
import asyncio
import netifaces

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = True
PRESSED = 0
POS = 724
PREFIX = "mq"

faderData = [
              (1,128,726,128,634),
              (2,225,726,225,634),
              (3,322,726,322,634),
              (4,419,726,419,634),
              (5,516,726,516,634),
              (6,613,726,613,634),
              (7,710,726,710,634),
              (8,807,726,807,634),
              (9,904,726,904,634),
              (10,1001,726,1001,634),

              ]

encoderData = [

              (1,40,172),
              (2,40,262),
              (3,40,352),
              (4,40,442),
              (5,1092,172),
              (6,1092,262),
              (7,1092,352),
              (8,1092,442),

              ]

def gen_osc_addr (type, number):
  osc_addr = "/" + PREFIX + "/" + type +"/"+str(number)
  return (osc_addr)



class TTCButton ():

  def __init__(self,number,x,y):
    self.number = number
    self.x = x
    self.y = y
    self.type = "b"
    self.osc_addr = gen_osc_addr(self.type, self.number)
    dispatcher.map (self.osc_addr, self.handler, x, y )

  def handler (self, unused_addr,args, volume):
    if volume == 1.0 :
      print (args[0])
      print (args[1])
      pyautogui.click (args[0], args[1])


class TTCSlider ():
  
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
    self.type = "b"
    self.osc_addr = gen_osc_addr(self.type, self.number)
    dispatcher.map (self.osc_addr, self.handler, self.key )

  def handler (self, unused_addr,args, volume):
    if volume == 1.0 :
      pyautogui.hotkey(args[0], args[1])


def s_handler(unused_addr, args, volume):
  pyautogui.click(args[0],559)

def sb_handler(unused_addr,args,volume):
  #print (args[0])
  #print (PRESSED)
  pyautogui.click(args[0],105)

def go_handler(unused_addr,args,volume):
  if (volume == 1.0):
    pyautogui.click(args[0], 586)
  
def b_handler (unused_addr,args,volume):
  #print (args[0], args[1])
  if volume == 1.0 :
    pyautogui.click (args[0], args[1])
  #print ("V:"+str(volume))
  
def wb_handler (unused_addr,args,volume):
  if volume == 1.0 :
    pyautogui.click (120, args[0])
    #print (args[0])


      

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=8000, help="The port to listen on")
  args = parser.parse_args()
  dispatcher = dispatcher.Dispatcher()
  
  faders = []
  for x in faderData:
    f= TTCSlider (x[0], x[1], x[2], x[3], x[4])
    faders.append (f)

  encoders =[]
  for x in encoderData:
    e = TTCEncoder (x[0], x[1], x[2])
    encoders.append (e)


  for x in range (0,11):
      y = 128+x*80
      dispatcher.map("/mq/sb/"+str(x+1), sb_handler,y)

  for x in range (0,2):
    y=150+x*40
    dispatcher.map("/mq/wb/"+str(x+1),wb_handler,y)


  i=1
  for x in range (0,5):
    for y in range (0,3):
      dispatcher.map("/mq/b/"+str(i), b_handler,1126+30*y,600+30*x)
      i = i+1
  
  i=16
  for x in range (0,5):
    for y in range (0,4):
      dispatcher.map("/mq/b/"+str(i), b_handler, 1245+30*y, 600+30*x)
      i=i+1
  
  i=35
  for x in range(0,2):
    for y in range (0,3):
      dispatcher.map("/mq/b/"+str(i), b_handler, 1126+30*y, 500+30*x)
      i=i+1

  i=41
  for x in range(0,2):
    for y in range (0,4):
      dispatcher.map("/mq/b/"+str(i), b_handler, 1245+30*y, 500+30*x)
      i=i+1

  i=49
  for x in range(0,2):
    for y in range (0,6):
      dispatcher.map("/mq/b/"+str(i), b_handler, 1165+30*y, 245+30*x)
      i=i+1



loop = asyncio.get_event_loop()
server = osc_server.AsyncIOOSCUDPServer((args.ip, args.port), dispatcher, loop)
print ("Serving on {}".format((args.ip, args.port)))
server.serve()
loop.run_forever()
