from os import path
import fliclib
from fliclib import ClickType
import pygame.mixer
import socket

HOST = "192.168.1.32"
PORT = 10002
BUF_SIZE = 100

COMMAND_CLICK = "IAVD0002"
COMMAND_DOUBLE_CLICK = "IAVD0001"
COMMAND_HOLD = "ITVD0   "

client = fliclib.FlicClient("localhost")

CUR_DIR = path.dirname(path.abspath( __file__))


def sendCommand(command):
    print("sendCommand:" + command)
    pygame.mixer.music.load(CUR_DIR + "/test.mp3")
    pygame.mixer.music.play(1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.send(command.encode('utf-8'))
    sock.send('\r\n'.encode('utf-8'))
    print(sock.recv(BUF_SIZE))
    sock.close()


def on_button_event(click_type):
    if click_type == ClickType.ButtonSingleClick:
        sendCommand(COMMAND_CLICK)
    elif click_type == ClickType.ButtonDoubleClick:
        sendCommand(COMMAND_DOUBLE_CLICK)
    elif click_type == ClickType.ButtonHold:
        sendCommand(COMMAND_HOLD)

def got_button(bd_addr):
    cc = fliclib.ButtonConnectionChannel(bd_addr)
    cc.on_button_single_or_double_click_or_hold = \
        lambda channel, click_type, was_queued, time_diff: \
            on_button_event(click_type)
    client.add_connection_channel(cc)

def got_info(items):
    print(items)
    for bd_addr in items["bd_addr_of_verified_buttons"]:
        got_button(bd_addr)


pygame.mixer.init()
client.get_info(got_info)
client.on_new_verified_button = got_button
client.handle_events()

