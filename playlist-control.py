#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
sys.path.insert(0, '/opt/MFRC522-python/')
import RPi.GPIO as GPIO
import MFRC522
import signal
import connect
import time

continue_reading = True

def end_read(signal, frame):
    global continue_reading
    continue_reading = False
    GPIO.cleanup()


def play(uid, playlists):
    rfid = ','.join(str(e) for e in uid)
    if (rfid in playlists):
        connect.loadPlaylist(playlists[rfid].strip())
    else:
        print("Unkown card detected -> " + rfid)


# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
signal.signal(signal.SIGTERM, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Load Playlistfile
latestUid = None
playlists = {}
with open("playlist.txt") as file:
    for line in file:
        name, var = line.partition("=")[::2]
        playlists[name.strip()] = var

# This loop keeps checking for chips.
# If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        # Get the UID of the card
        (status, uid) = MIFAREReader.MFRC522_Anticoll()
        if not (uid is None) and (len(uid) == 5) and (uid != latestUid):
            latestUid = uid
            play(uid, playlists)
    time.sleep(0.3)
