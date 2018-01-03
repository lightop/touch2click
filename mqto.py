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

buttonData = [
              
              ('select1',128,559),
              ('select2',225,559),
              ('select3',322,559),
              ('select4',419,559),
              ('select5',516,559),
              ('select6',613,559),
              ('select7',710,559),
              ('select8',807,559),
              ('select9',904,559),
              ('select10',1001,559),

              ('go1', 128,586),
              ('go2', 225,586),
              ('go3', 322,586),
              ('go4', 419,586),
              ('go5', 516,586),
              ('go6', 613,586),
              ('go7', 710,586),
              ('go8', 807,586),
              ('go9', 904,586),
              ('go10', 1001,586),

              ('pause1', 128,586),
              ('pause2', 128,586),
              ('pause3', 128,586),
              ('pause4', 128,586),
              ('pause5', 128,586),
              ('pause6', 128,586),
              ('pause7', 128,586),
              ('pause8', 128,586),
              ('pause9', 128,586),
              ('pause10', 128,586),

              ('flash1', 128,586),
              ('flash2', 128,586),
              ('flash3', 128,586),
              ('flash4', 128,586),
              ('flash5', 128,586),
              ('flash6', 128,586),
              ('flash7', 128,586),
              ('flash8', 128,586),
              ('flash9', 128,586),
              ('flash10', 128,586),
              

              

]

def gen_osc_addr (type, number):
  osc_addr = "/" + PREFIX + "/" + type +"/"+str(number)
  print (osc_addr)
  return (osc_addr)



class TTCButton ():

  def __init__(self,number,x,y):
    self.number = number
    self.x = x
    self.y = y
    self.type = "button"
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
    f= TTCSlider (*x)
    faders.append (f)

  encoders =[]
  for x in encoderData:
    e = TTCEncoder (*x)
    encoders.append (e)

  buttons = []
  for x in buttonData:
    b = TTCButton (*x)
    buttons.append(b)

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
