import lcddriver
from time import *
import time
import touchtest
import socket
import lib
import subprocess
display = lcddriver.lcd()
n = touchtest.TOUCH()

#display.LCD_CURSORON = 0x02

#display.lcd_display_string(fontdata, 1)
#display.lcd_write(0x80)
#display.lcd_write_char(0)

#display.lcd_display_string("!",0x01)
#display.lcd_display_string("!",0x0F)
#time.sleep(2)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("google.com",80))
yourIP = s.getsockname()[0]
s.close()
num = n.keypad()


def ipconf():
        display.lcd_clear()
        display.lcd_display_string("Settings>IPconf", 1)
        display.lcd_display_string("Host:" + str((socket.gethostname())), 2)
        #while true:
        time.sleep(3)
        display.lcd_display_string("IP:" + str(yourIP), 2)
        time.sleep(2)

def basic_WANem_settings():
        display.lcd_clear()
        display.lcd_display_string("Settings>BasicWANem", 1)
        display.lcd_display_string("Bandwidth:", 2)
        #display.lcd_display_string("Delay: 200", 2)
        time.sleep(2)
        num = n.keypad()
        display.lcd_display_string("" +str(num) , 2)
        display.lcd_display_string("Delay: 200", 1)
        subprocess.call(["tc", "qdisc", "add", "dev", "eth0", "root" , "netem" , "delay" , "200ms"])
        subprocess.call(["tc", "qdisc", "add", "dev", "eth1", "root" , "netem" , "delay" , "200ms"])
        subprocess.call(["tc", "qdisc", "add", "dev", "eth2", "root" , "netem" , "delay" , "200ms"])
        p=subprocess.Popen(['ping','192.168.1.2','-c','4',"-W","2"])
        p.wait()
        time.sleep(2)

def extended_WANem_settings():
        display.lcd_clear()
        display.lcd_display_string("Settings>cWANem", 1)
        display.lcd_display_string("Loss: 50", 2)
        #num = n.keypad()
        display.lcd_display_string("Touched" +str(4) , 2)
        subprocess.call(["tc", "qdisc", "change", "dev", "eth0", "root" , "netem" , "loss" , "50%"])
        time.sleep(3)
        display.lcd_display_string("Duplication:", 2)
        #subprocess.call(["tc", "qdisc", "change", "dev", "eth0", "root" , "netem" , "duplicate" , "50%"])
        #time.sleep(3)
        display.lcd_display_string("Packet reordering::", 2)
        #subprocess.call(["tc", "qdisc", "change", "dev", "eth0", "root" , "netem" , "gap" , "5" , "delay" , "10ms"])
        #time.sleep(3)
        display.lcd_display_string("Ideal timer:", 2)
        #time.sleep(3)
        display.lcd_display_string("Random disconnect:", 2)
        #time.sleep(3)
        display.lcd_display_string("Random conn disconn:", 2)
        time.sleep(2)

def status():
        display.lcd_clear()
        display.lcd_display_string("Settings>Status", 1)
        time.sleep(2)

def monitor():
        display.lcd_clear()
        time.sleep(2)
        display.lcd_display_string("Settings>Monitor", 1)
        display.lcd_display_string("Interface stats:", 2)
        time.sleep(3)
        display.lcd_display_string("Bandwidth monitor:", 2)
        time.sleep(2)


def tests():
        display.lcd_clear()
        time.sleep(2)
        display.lcd_display_string("Settings>Tests", 1)
        p=subprocess.Popen(['ping','192.168.1.2','-c','4',"-W","2"])
        p.wait()
        #print (p.poll())
        display.lcd_display_string("Ping:"+str(p.poll()),2)
        display.lcd_display_string("Ping:",2)
        time.sleep(2)

# Main settings
def settings():
        display.lcd_clear()
        display.lcd_display_string("Settings",1)
        time.sleep(2)

lcdloop =1
try:
   while lcdloop ==1 :
        settings()
        ipconf()
        basic_WANem_settings()
        extended_WANem_settings()
        status()
        monitor()
        tests()
        time.sleep(2)

except KeyboardInterrupt:
    print("Cleaning up!")
    display.lcd_clear()




