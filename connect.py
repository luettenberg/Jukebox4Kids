#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from time import sleep

# IMPORTS
import sys
import pprint

import time

from mpd import (MPDClient, CommandError)
from socket import error as SocketError

HOST = 'localhost'
PORT = '6600'
PASSWORD = False
##
CON_ID = {'host':HOST, 'port':PORT}
##

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

def changeVolume(amount):
    client = connect()
    changeVolume(cliemt, amount)

def changeVolume(client, amount):
    currentVol = int(client.status()['volume'])
    newVol = currentVol+amount
    if (100 >= newVol) and (newVol >= 0):
        client.setvol(newVol)
    printState(client, 'volDown')


def tooglePlay():
    tooglePlay(connect())

def tooglePlay(client):
    if client.status().get('state','stop') == 'stop':
      client.play()
    else:
      client.pause()
    time.sleep(0.5)
    printState(client, 'prev')

def playNext():
    playNext(connect())

def playNext(client):
    status = client.status()
    state = status.get('state')
    nextSong = status.get('nextsong', -1)
    if (state != 'stop') and (nextSong != '-1'):
      client.next()
    time.sleep(0.2)
    printState(client, 'next')

def playPrev():
    playPrev(connect())

def playPrev(client):
    status = client.status()
    state = status.get('state')
    song = int(status.get('song', 0))
    if (state != 'stop') and (song > 0):
      client.previous()
    time.sleep(0.2)
    printState(client, 'prev')

def loadPlaylist(playlist):
    client = connect();
    client.stop()
    client.clear()
    client.load(playlist)
##

def playTrack(track):
    client = connect();
    client.stop()
    client.clear()
    client.add(track)
    client.play()
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
