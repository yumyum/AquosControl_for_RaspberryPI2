#!/bin/sh

FLIC_PATH="/home/pi/flic"

sudo hciconfig hci0 up
sudo ${FLIC_PATH}/armv7l/daemon -d
forever start -c python ./aquos.py
amixer set PCM on 100%
