#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from time import sleep

# IMPORTS
import sys
import pprint
import RPi.GPIO as GPIO
import time

from mpd import (MPDClient, CommandError)
from socket import error as SocketError

# Volume GPIO Ports
Vol_Enc_A = 16  # Encoder input A: input GPIO 12 (active high)
Vol_Enc_B = 12  # Encoder input B: input GPIO 16 (active high)


HOST = 'localhost'
PORT = '6600'
PASSWORD = False
##
CON_ID = {'host':HOST, 'port':PORT}
##  

## Some functions
def init():

    GPIO.setwarnings(True)

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # define the Encoder switch inputs
    GPIO.setup(Vol_Enc_A, GPIO.IN) # pull-ups are too weak, they introduce noise
    GPIO.setup(Vol_Enc_B, GPIO.IN)

    # setup an event detection thread for the A encoder switch
    GPIO.add_event_detect(Vol_Enc_A, GPIO.RISING, callback=rotation_decode, bouncetime=2) # bouncetime in mSec
    #
    return


def rotation_decode(Vol_Enc_A):
    '''
    This function decodes the direction of a rotary encoder and in- or
    decrements a counter.

    The code works from the "early detection" principle that when turning the
    encoder clockwise, the A-switch gets activated before the B-switch.
    When the encoder is rotated anti-clockwise, the B-switch gets activated
    before the A-switch. The timing is depending on the mechanical design of
    the switch, and the rotational speed of the knob.

    This function gets activated when the A-switch goes high. The code then
    looks at the level of the B-switch. If the B switch is (still) low, then
    the direction must be clockwise. If the B input is (still) high, the
    direction must be anti-clockwise.

    All other conditions (both high, both low or A=0 and B=1) are filtered out.

    To complete the click-cycle, after the direction has been determined, the
    code waits for the full cycle (from indent to indent) to finish.

    '''

    sleep(0.002) # extra 2 mSec de-bounce time

    # read both of the switches
    Switch_A = GPIO.input(Vol_Enc_A)
    Switch_B = GPIO.input(Vol_Enc_B)

    if (Switch_A == 1) and (Switch_B == 0) : # A then B ->
        changeVolume(+1)
        # at this point, B may still need to go high, wait for it
        while Switch_B == 0:
            Switch_B = GPIO.input(Vol_Enc_B)
        # now wait for B to drop to end the click cycle
        while Switch_B == 1:
            Switch_B = GPIO.input(Vol_Enc_B)
        return

    elif (Switch_A == 1) and (Switch_B == 1): # B then A <-
        changeVolume(-1)
         # A is already high, wait for A to drop to end the click cycle
        while Switch_A == 1:
            Switch_A = GPIO.input(Vol_Enc_A)
        return

    else: # discard all other combinations
        return

def changeVolume(amount):
    client = connect()
    currentVol = int(client.status()['volume'])
    newVol = currentVol+amount
    if (100 >= newVol) and (newVol >= 0):
        client.setvol(newVol)
    printState(client, 'volDown')
    
def mpdConnect(client, con_id):
    """
    Simple wrapper to connect MPD.
    """
    try:
        client.connect(**con_id)
    except SocketError:
        return False
    return True

def mpdAuth(client, secret):
    """
    Authenticate
    """
    try:
        client.password(secret)
    except CommandError:
        return False
    return True
##

def loadPlaylist(client, playlist):
    client.stop()
    client.clear()
    client.load(playlist)
##

def playTrack(client, track):
    client.stop()
    client.clear()
    client.add(track)
    client.play()
##

def printState(printer, client):
    ## Print out MPD stats & disconnect
    print('\nCurrent MPD state:')
    printer.pprint(client.status())

    print('\nMusic Library stats:')
    printer.pprint(client.stats())
##

def listPlaylists(printer, client):
    printer.pprint(client.listplaylists())
##

def listCurrentPlaylist(printer, client):
    printer.pprint(client.paylistinfo())
##

def printState(client, action):
  status = client.status()
  state = status.get('state','????').title()
  actSong = int(status.get('song','0'))+1
  songLength = status.get('playlistlength',-1)
  volume = int(status.get('volume'))
  message = '{:5} - {:>2} / {:>2} @ {:03d} Vol. | Action: {:10}'.format(state, actSong, songLength, volume, action)  
  print('\r' + message, end='')
  sys.stdout.flush()
##

def connect():
      ## MPD object instance
    client = MPDClient()
    if mpdConnect(client, CON_ID):
        print('Got connected!')
    else:
        print('fail to connect MPD server.')
        sys.exit(1)

    # Auth if password is set non False
    if PASSWORD:
        if mpdAuth(client, PASSWORD):
            print('Pass auth!')
        else:
            print('Error trying to pass auth.')
            client.disconnect()
            sys.exit(2)
    
    return client

def main():
    ## MPD object instance
    client = connect()
    
    init()
    ## Fancy output
    #pp = pprint.PrettyPrinter(indent=4)

    ## Print out MPD stats & disconnect
    #printState(pp,client)
    
    #listPlaylists(pp,client)
    #print client.status()
    loadPlaylist(client, 'RITS Favs (by elixir046)')
    client.setvol(5)
    #print client.status()
    #playTrack(client, 'spotify:track:1ocmRsEMI6nO9d9BdQbXNI')

    ##client.playlistadd('kaffehausmusik','spotify:user:spotify:playlist:37i9dQZF1DX6KItbiYYmAv')
  
    while True:
        play_ = GPIO.input(17)
        prev_ = GPIO.input(22)
        next_ = GPIO.input(27)
        volUp = GPIO.input(23)
        volDown = GPIO.input(24)
        
        if play_ == False:
            if client.status().get('state','stop') == 'stop':
              client.play()
            else: 
              client.pause()
            time.sleep(0.5)
            printState(client, 'prev') 
            
        elif prev_ == False:
            status = client.status();
            state = status.get('state')
            song = int(status.get('song', 0))
            if (state != 'stop') and (song > 0):
              client.previous()
            time.sleep(0.2)
            printState(client, 'prev') 
            
        elif next_ == False:
            status = client.status();
            state = status.get('state')
            nextSong = status.get('nextsong', -1)
            if (state != 'stop') and (nextSong != '-1'):
              client.next()
            time.sleep(0.2)
            printState(client, 'next')
       
        elif volUp == False:
            currentVol = int(client.status()['volume'])
            if currentVol < 100:
              client.setvol(currentVol+1)
            time.sleep(0.2)
            printState(client, 'volUp')
       
        elif volDown == False:
            currentVol = int(client.status()['volume'])
            if currentVol > 0:
              client.setvol(currentVol-1)
            time.sleep(0.2)
            printState(client, 'volDown')
        
# Script starts here
if __name__ == "__main__":
    main()
