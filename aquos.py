from os import path
from flic import flic
import pygame.mixer
import socket

HOST = "192.168.1.32"
PORT = 10002
BUF_SIZE = 100

COMMAND_CLICK = "IAVD0002"
COMMAND_DOUBLE_CLICK = "IAVD0001"
COMMAND_HOLD = "ITVD0   "

client = flic.Client()

CUR_DIR = path.dirname(path.abspath( __file__))

class ButtonEventListener(flic.ButtonEventListener):
    def __init__(self):
        super(ButtonEventListener, self).__init__()
        pygame.mixer.init()

    def getHash(self):
        return "main"

    def onButtonUpOrDown(self, deviceId, queued, timeDiff, isUp, isDown):
        manager = client.getManager()
        button = manager.getButton(deviceId)
        #print(button.getDeviceId() + (" up" if isUp else " down"))
        #self.aquosCtl.onButtonUpOrDown(deviceId, isUp)
    def onButtonSingleOrDoubleClickOrHold(self, deviceId, queued, timeDiff, isSingleClick, isDoubleClick, isHold):
        if isSingleClick:
            self.sendCommand(COMMAND_CLICK)
        elif isDoubleClick:
            self.sendCommand(COMMAND_DOUBLE_CLICK)
        elif isHold:
            self.sendCommand(COMMAND_HOLD)

    def sendCommand(self, command):
        print("sendCommand:" + command)
        pygame.mixer.music.load(CUR_DIR + "/test.mp3")
        pygame.mixer.music.play(1)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.send(command)
        sock.send('\r\n')
        print(sock.recv(BUF_SIZE))
        sock.close()

buttonEventListener = ButtonEventListener()

def addButtonEventListener(button):
    button.addButtonEventListener(buttonEventListener)

class ButtonListener(flic.ButtonListener):
    def getHash(self):
        return "main"

    def onButtonDiscover(self, button):
        addButtonEventListener(button)

buttonListener = ButtonListener()

class InitializedCallback(flic.CallbackVoid):
    def callback(self):
        print("Initialized")
        manager = client.getManager()
        buttons = manager.getButtons()
        try:
            for button in buttons:
                addButtonEventListener(button)
            manager.addButtonListener(buttonListener)
        except:
            pass

class UninitializedCallback(flic.CallbackBool):
    def callback(self):
        print("Uninitialized")


init = InitializedCallback()
uninit =  UninitializedCallback()
client.start(init.getCallback(), uninit.getCallback())

client.run()
