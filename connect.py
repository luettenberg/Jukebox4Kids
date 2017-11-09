#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
import sys
import pprint
import RPi.GPIO as GPIO
import time


from mpd import (MPDClient, CommandError)
from socket import error as SocketError

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

HOST = 'localhost'
PORT = '6600'
PASSWORD = False
##
CON_ID = {'host':HOST, 'port':PORT}
##  

## Some functions
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

def loadAndPlayPlaylist(client, playlist):
    client.stop()
    client.clear()
    client.load(playlist)
    client.play()
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

def main():
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

    ## Fancy output
    pp = pprint.PrettyPrinter(indent=4)

    ## Print out MPD stats & disconnect
    #printState(pp,client)
    
    #listPlaylists(pp,client)
    loadAndPlayPlaylist(client, 'RITS Favs (by elixir046)')
    client.setVol(50)
    #playTrack(client, 'spotify:track:1ocmRsEMI6nO9d9BdQbXNI')

    ##client.playlistadd('kaffehausmusik','spotify:user:spotify:playlist:37i9dQZF1DX6KItbiYYmAv')
  
    while True:
        play_ = GPIO.input(17)
        prev_ = GPIO.input(22)
        next_ = GPIO.input(27)
        volUp = GPIO.input(23)
        volDown = GPIO.input(24)
        
        if play_ == False:
            print('Play Pressed')
            client.pause()
            time.sleep(2.0)
            
        elif prev_ == False:
            print('Prev Pressed')
            client.previous()
            time.sleep(2.0)
            
        elif next_ == False:
            print('Next Pressed')
            client.next()
            time.sleep(2.0)
       
        elif volUp == False:
            print('Increase Volume')
            currentVol = int(client.status()["volume"])
            if(currentVol<100)
             client.setvol(currentVol+1)
       
        elif volDown == False:
            print('Decrease Volume')
            currentVol = int(client.status()["volume"])
            if(currentVol>0)
             client.setvol(currentVol+1)
        
# Script starts here
if __name__ == "__main__":
    main()
