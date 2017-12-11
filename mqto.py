import argparse
import math
import pyautogui

from pythonosc import dispatcher
from pythonosc import osc_server

pyautogui.PAUSE = 0.1
pyautogui.FAILSAFE = True
PRESSED = 0
POS = 724


def s_handler(unused_addr, args, volume):
  #print("[{0}] ~ {1}".format(args[0], volume))
  #a = round (724-90*volume)
  #pyautogui.moveTo (128,a+1)
  #pyautogui.dragTo (128,a)
  print (args[0])
  pyautogui.click(args[0],559)

def sb_handler(unused_addr,args,volume):
  print (args[0])
  print (PRESSED)
  pyautogui.click(args[0],105)

def go_handler(unused_addr,args,volume):
  if (volume == 1.0):
    pyautogui.click(args[0], 586)

def ft_handler (unused_addr, args,volume):
  print (volume)
  print ("***")
  if (volume == 1): 
    pyautogui.mouseDown(128,724)
    print ("Down")

  if (volume ==0):
    pyautogui.mouseUp()
    print ("Up")

def f_handler (unused_addr, args,volume):
  #print (volume)
  if (volume == v):
    exit
    print ("UUU")
 # print ("------")
  #pyautogui.moveTo(128,724-volume)
  v = volume
  #sleep (1)

def b_handler (unused_addr,args,volume):
  print (args[0], args[1])
  if volume == 1.0 :
    pyautogui.click (args[0], args[1])
  print ("V:"+str(volume))
  



def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=8000, help="The port to listen on")
  args = parser.parse_args()
  dispatcher = dispatcher.Dispatcher()
  for x in range (0,9):
      print ("/mq/s/"+str(x+1))
      y = 128+x*97
      print (y)
      dispatcher.map("/mq/s/"+str(x+1), s_handler, y)
      dispatcher.map("/mq/fader/"+str(x+1)+"/z", ft_handler, y)
      dispatcher.map("/mq/fader/"+str(x+1), f_handler, y)
      dispatcher.map("/mq/go/"+str(x+1),go_handler, y)

  for x in range (0,11):
      y = 128+x*80
      print (y)
      dispatcher.map("/mq/sb/"+str(x+1), sb_handler,y)
  #dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)
  i=1
  for x in range (0,5):
    for y in range (0,3):
      dispatcher.map("/mq/b/"+str(i), b_handler,1126+30*y,600+30*x)
      print (1126+30*y, 600+30*x)
      print (i)
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

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()