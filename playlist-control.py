#!/usr/bin/env python
# -*- coding: utf8 -*-
import RPi.GPIO as GPIO
import MFRC522
import connect
import time
import threading


class PlaylistControl(threading.Thread):

    continue_reading = True
    latestUid = None
    playlists = {}
    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()

    def __init__(self):
        print("Starting PlaylistControl")
        threading.Thread.__init__(self)
        self.loadPlaylist()
        print("Started PlaylistControl")

    def play(self, uid, playlists):
        if (uid != self.latestUid):
            self.latestUid = uid
            rfid = ','.join(str(e) for e in uid)
            if (rfid in playlists):
                connect.loadPlaylist(playlists[rfid].strip())
            else:
                print("Unkown card detected -> " + rfid)

    def loadPlaylist(self):
        with open("playlist.txt") as file:
            for line in file:
                name, var = line.partition("=")[::2]
                self.playlists[name.strip()] = var

    def run(self):
        while continue_reading:
            # Scan for cards
            (status, TagType) = self.MIFAREReader.MFRC522_Request(
                self.MIFAREReader.PICC_REQIDL)

            # If we have the UID, continue
            if status == self.MIFAREReader.MI_OK:
                # Get the UID of the card
                (status, uid) = self.MIFAREReader.MFRC522_Anticoll()
                if not (uid is None) and (len(uid) == 5):
                    self.play(uid, self.playlists)

            time.sleep(0.3)

    def exit(self):
        global continue_reading
        continue_reading = False
