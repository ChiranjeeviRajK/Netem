from time import *
import time
import MPR121

class TOUCH:
 def __init__(self):
  self.mi= MPR121.MPR121()
  self.mi.connect()


 def fun(self,val):
    switcher={
              1: 'T',
              2: 'L',
              4: 'R',
              8: 'D',
              64: 'O',
              128: 'B',
            }
    return switcher.get(val, '')

 def keypad(self):
  while True:
   val = self.mi.readTouch()
   if val != 0:
     print("Touch register=" + str(val))
     num =self.fun(val)
     print ("Actual----"+num)
     return num
     num = ''
 #time.sleep(0.5)
~
