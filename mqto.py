import argparse
import math
import pyautogui
from pythonosc import dispatcher
from pythonosc import osc_server
import asyncio

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = True
PRESSED = 0
POS = 724
PREFIX = "mq"

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
  
  def __init__(self, number, x, y_bottom, y_top):
    self.number = number
    self.x = x
    self.y_bottom = y_bottom
    self.y_top = y_top
    self.height = self.y_bottom - self.y_top
    self.type = "fader"
    self.level = 0
    self.osc_addr = gen_osc_addr (self.type, self.number)
    dispatcher.map (self.osc_addr, self.handler, self.x, self.y_bottom)
    dispatcher.map (self.osc_addr+"/z",self.handler_z, self.x, self.y_bottom)

  def handler (self, unused_addr, args, volume):
    self.level = volume*self.height
    pyautogui.moveTo(self.x,self.y_bottom-self.level)
    

  def handler_z (self, unused_addr,args, volume):
    if (volume == 1): 
      pyautogui.mouseDown(self.x,self.y_bottom-self.level)
      
    if (volume ==0):
      pyautogui.mouseUp()


class TTCEncoder ():

  def __init__(self, number,x,y):
    self.number = number
    self.x = x
    self.y = y
    self.type = "e"
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

def wt_handler (unused_addr,args,volume):
  if (volume == 1.0):
    try:
      pyautogui.mouseDown (40,args[0])
    except (RuntimeError,ValueError): pass
  if (volume == 0.0):
    try:
      pyautogui.mouseUp()
    except (RuntimeError,ValueError): pass

def w_handler (unused_addr,args,volume):
  if (volume == 1.0):
    try:
      #pyautogui.mouseDown (40,172)
      pyautogui.moveRel(0,1)
      #pyautogui.mouseUp()
    except (RuntimeError,ValueError): pass
  if (volume == 0.0):
    try:
        ##pyautogui.mouseDown(40,172)
      pyautogui.moveRel(0,-1)
      #pyautogui.mouseUp()
    except (RuntimeError,ValueError): pass
      

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=8000, help="The port to listen on")
  args = parser.parse_args()
  dispatcher = dispatcher.Dispatcher()
  
  faders = []
  for x in range(0,9):
    yx = 128+x*97
    f= TTCSlider (x+1, yx, 724, 634)
    faders.append (f)



  for x in range (0,11):
      y = 128+x*80
      dispatcher.map("/mq/sb/"+str(x+1), sb_handler,y)

  for x in range (0,2):
    y=150+x*40
    dispatcher.map("/mq/wb/"+str(x+1),wb_handler,y)

  for x in range (0,4):
    y = 172+x*90
    dispatcher.map("/mq/wheel/"+str(x+1),w_handler, y)
    dispatcher.map("/mq/wheel/"+str(x+1)+"/z", wt_handler,y)

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
