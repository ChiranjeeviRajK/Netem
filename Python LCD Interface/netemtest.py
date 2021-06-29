import subprocess
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


def get_active_rules():
     proc = subprocess.Popen(['tc', 'qdisc'], stdout=subprocess.PIPE)
     output = proc.communicate()[0].decode()
     lines = output.split('\n')[:-1]
     rules = []
     dev = set()
     for line in lines:
         arguments = line.split(' ')
         rule = parse_rule(arguments)
         if rule['name'] and rule['name'] not in dev:
             rules.append(rule)
             dev.add(rule['name'])
     return rules

def parse_rule(splitted_rule):
     rule = {'name': None,
             'rate': None,
             'delay': None,
             'loss': None,
             'duplicate': None,
             'reorder': None,
             'corrupt': None}
     i = 0
     for argument in splitted_rule:
         if argument == 'dev':
             if pattern is None and dev_list is None:
                 rule['name'] = splitted_rule[i + 1]
             if pattern:
                 if pattern.match(splitted_rule[i + 1]):
                     rule['name'] = splitted_rule[i + 1]
             if dev_list:
                 if splitted_rule[i + 1] in dev_list:
                     rule['name'] = splitted_rule[i + 1]
         elif argument == 'rate':
             rule['rate'] = splitted_rule[i + 1].split('Mbit')[0]
         elif argument == 'delay':
             rule['delay'] = splitted_rule[i + 1]
         elif argument == 'loss':
             rule['loss'] = splitted_rule[i + 1]
         elif argument == 'duplicate':
             rule['duplicate'] = splitted_rule[i + 1]
	 elif argument == 'reorder':
             rule['reorder'] = splitted_rule[i + 1]
         elif argument == 'corrupt':
             rule['corrupt'] = splitted_rule[i + 1]
         i += 1
     return rule

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


if __name__ == "__main__":
     	get_active_rules()
     	parse_rule()
	display.lcd_clear()
        display.lcd_display_string("Settings",1)
        time.sleep(2)

lcdloop =1
try:
   while lcdloop ==1 :
        ipconf()
        status()
        monitor()
        tests()
        time.sleep(2)

except KeyboardInterrupt:
    print("Cleaning up!")
    display.lcd_clear()
