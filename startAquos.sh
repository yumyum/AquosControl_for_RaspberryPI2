#!/bin/sh

FLIC_PATH="/home/pi/fliclib-linux-hci/bin/"

sudo hciconfig hci0 up
sudo ${FLIC_PATH}/armv6l/flicd -d -f flic.sqlite3
forever start -c python3 ./aquos.py
amixer set PCM on 100%
