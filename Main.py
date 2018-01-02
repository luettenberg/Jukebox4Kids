#!/usr/bin/env python
# -*- coding: utf8 -*-
import sdnotify
import time
import RPi.GPIO as GPIO
import signal
import logging
from volumeControl import VolumeControl
from playControl import PlayControl
from playlistControl import PlaylistControl
from display import Display


# Configure GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)

running = True


def exit(signal, frame):
    """Interrupt main loop"""
    print('Exiting')
    global running
    running = False


def cleanUp():
    """Cleaning up resources"""
    GPIO.cleanup()


# Hook the SIGINT
signal.signal(signal.SIGINT, exit)
signal.signal(signal.SIGTERM, exit)

# Init VolumeControl
volume = VolumeControl()
volume.setDaemon(True)
volume.setName('Volume')
volume.start()

# Init PlayControl
playControl = PlayControl()

# Init PlaylistControl
playlistControl = PlaylistControl()
playlistControl.setDaemon(True)
playlistControl.start()

# Init Display
display = Display(GPIO.BOARD)
display.setDaemon(True)
display.start()

# Init Service Watchdog
n = sdnotify.SystemdNotifier()
n.notify('READY=1')

# Endlosschleife
try:
    while running:
        time.sleep(1)
        if (display.isAlive() and playlistControl.isAlive() and volume.isAlive()):
            n.notify('WATCHDOG=1')
        else:
            print("Not all Components running")
except Exception as e:
	logging.exception("Error in main program")
cleanUp()
