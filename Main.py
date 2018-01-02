#!/usr/bin/env python
# -*- coding: utf8 -*-
import sdnotify
import time
import RPi.GPIO as GPIO
import play-control
import playlist-control

def onExit():
    """cleansup everything"""
    GPIO.remove_event_detect()
    GPIO.cleanup()

# Configure GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

volume = Volume()
volume.start()

playControl = new PlayControl()

playlistControl = new PlaylistControl()
playlistControl.start();

display = new Display()
display.start()

#Init Service Watchdog
n = sdnotify.SystemdNotifier()
n.notify('READY=1')


# Endlosschleife
try:
    while True:
        time.sleep(1)
        if (display.started and playlistControl.started and volume.started):
            n.notify('WATCHDOG=1')
        else:
            print("Not all Components running")
except Exception:
    print('Exception raised - exiting')
onExit()
