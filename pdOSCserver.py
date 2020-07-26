# import argparse
# import math

from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from pythonosc.udp_client import SimpleUDPClient
from gpiozero import Button, LED

ip = "127.0.0.1"

red = LED(17)
green = LED(18)
switchButton = Button(26, hold_time = 3)
red.on()
currentLEDstatus = "red on"

def redOn():
    if not red.is_lit():
        red.on()
        green.off()

def greenOn():
    if not green.is_lit():
        green.on()
        red.off()

# OSC CLIENT

clientPort = 9001

print ("*** starting OSC client ***")

client = SimpleUDPClient(ip, clientPort)

switchButton.when_pressed = lambda: client.send_message("/switch", 'switch')
switchButton.when_held = lambda: client.send_message("/save", 'save')

# OSC SERVER

serverPort = 2
print ("*** starting OSC server ***")

def record_mode(address, *args):
    print(f"{address}: {args}")
    redOn

def play_mode(address, *args):
    print(f"{address}: {args}")
    greenOn

def save_lights_start(address, *args):
    currentLEDred = red.is_lit()
    print(f"{address}: {args}")
    red.blink(on_time = 0.1, off_time = 0.2, n = 5, background = False)
    green.blink(on_time = 0.1, off_time = 0.2, n = 5, background = False)
    if currentLEDstatus:
        red.on()
        green.off()
    else:
        green.on()
        red.off()

def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")


dispatcher = Dispatcher()

dispatcher.map("/record", record_mode)
dispatcher.map("/play", play_mode)
dispatcher.map("/saveStart", save_lights_start)
#dispatcher.map("/saveEnd", save_lights_stop)
dispatcher.set_default_handler(default_handler)

server = BlockingOSCUDPServer((ip, serverPort), dispatcher)
server.serve_forever()
