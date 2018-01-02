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

class JukeBox4Kids:

    running = True
    volume = None
    playControl = None
    playlistControl = None
    display = None

    def __init__(self):

        # Init VolumeControl
        self.volume = VolumeControl()
        self.volume.setDaemon(True)
        self.volume.setName('Volume')
        self.volume.start()

        # Init Control for buttons
        self.playControl = PlayControl()

        # Init PlaylistControl
        self.playlistControl = PlaylistControl()
        self.playlistControl.setDaemon(True)
        self.playlistControl.start()

        # Init Display
        self.display = Display(GPIO.BOARD)
        self.display.setDaemon(True)
        self.display.start()

    def cleanUp(self):
        """Cleaning up resources."""
        GPIO.cleanup()
        self.display.clearDisplay()
        self.playControl.exit()
        self.playlistControl.exit()


    def isHealthy(self):
        return (self.display is not None
                and self.display.isHealthy()
                and self.volume is not None
                and self.volume.isHealthy()
                and self.playControl is not None
                and self.playControl.isHealthy()
                and self.playlistControl is not None
                and self.playlistControl.isHealthy())

#def exit(signal, frame):
#    """Interrupt main loop"""
#    print('Exiting')
#    self.running = False
#
#box = None

def main():
    # Hook the SIGINT
#    signal.signal(signal.SIGINT, exit)
#    signal.signal(signal.SIGTERM, exit)

    # Configure GPIO
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BOARD)

    global box
    box = JukeBox4Kids()

    # Init Service Watchdog
    n = sdnotify.SystemdNotifier()
    n.notify('READY=1')

    # Endlosschleife
    try:
        while True:
            time.sleep(1)
            if (box.isHealthy()):
                n.notify('WATCHDOG=1')
            else:
                print("Not all Components running")
    except Exception as e:
        logging.exception("Error in main program")
    box.cleanUp()


if __name__ == "__main__":
    main()
