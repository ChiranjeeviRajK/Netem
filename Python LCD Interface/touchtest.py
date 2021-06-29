from time import *
import time
import MPR121



class TOUCH:
 def __init__(self):
  self.mi= MPR121.MPR121()
  self.mi.connect()


 def fun(self,val):
    switcher={
              1: '1',
              2: '2',
              4: '3',
              8: '4',
              32: '5',
              64: '6',
              128: '7',
              256: '8',
              512: '9',
              #1024: '10',
              #2048: '11',
            }
    return switcher.get(val, '')




 def keypad(self):
   while True:
    val = self.mi.readTouch()
    if val != 0:
     #print(" "+str(val))
     num= self.fun(val)
     print(num)
     return num
     num = ''
   #time.sleep(0.5)

