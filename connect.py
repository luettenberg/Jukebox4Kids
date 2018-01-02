#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import time
from time import sleep
from mpd import (MPDClient, CommandError)
from socket import error as SocketError

HOST = 'localhost'
PORT = '6600'
PASSWORD = False
MAX_VOLUME = 100
MIN_VOLUME = 0
##
CON_ID = {'host': HOST, 'port': PORT}
##


def mpdConnect(client, con_id):
    """Simple wrapper to connect MPD."""
    try:
        client.connect(**con_id)
    except SocketError:
        return False
    return True


def mpdAuth(client, secret):
    """Authenticate against mdp server."""
    try:
        client.password(secret)
    except CommandError:
        return False
    return True


def changeVolume(amount):
    """Change volume on mdp server."""
    client = connect()
    changeVolumeInternal(client, amount)
    disconnect(client)


def changeVolumeInternal(client, amount):
    currentVol = int(client.status()['volume'])
    newVol = currentVol+amount
    if (newVol < 0):
	       newVol = 0
    elif (newVol > 100):
	       newVol = 100
    setVolumeInternal(client, newVol)
    printState(client, 'volDown')


def setVolume(value):
    """Set volume on mdp server. Value must be 0 => value <= 100"""
    client = connect()
    setVolumeInternal(client, value)
    disconnect(client)


def setVolumeInternal(client, value):
    if (value < MIN_VOLUME):
	value = MIN_VOLUME
    elif (value > MAX_VOLUME):
   	value = MAX_VOLUME
    client.setvol(value)


def tooglePlay():
    client = connect()
    tooglePlayInternal(client)
    disconnect(client)


def tooglePlayInternal(client):
    if client.status().get('state', 'stop') == 'stop':
        client.play()
    else:
        client.pause()
    time.sleep(0.5)
    printState(client, 'prev')


def playNext():
    client = connect()
    playNextInternal(client)
    disconnect(client)


def playNextInternal(client):
    status = client.status()
    state = status.get('state')
    nextSong = status.get('nextsong', -1)
    if (state != 'stop') and (nextSong != '-1'):
        client.next()
    time.sleep(0.2)
    printState(client, 'next')


def playPrev():
    client = connect()
    playPrevInternal(client)
    client.close()
    client.disconnect()


def playPrevInternal(client):
    status = client.status()
    state = status.get('state')
    song = int(status.get('song', 0))
    if (state != 'stop') and (song > 0):
        client.previous()
    time.sleep(0.2)
    printState(client, 'prev')


def loadPlaylist(playlist):
    client = connect()
    reset(client)
    client.load(playlist)
    client.play()
    disconnect(client)


def playTrack(track):
    client = connect()
    client.stop()
    client.clear()
    client.add(track)
    client.play()
    client.close()
    client.disconnect()


def listPlaylists(printer, client):
    printer.pprint(client.listplaylists())


def listCurrentPlaylist(printer, client):
    printer.pprint(client.paylistinfo())


def printState(client, action):
    status = client.status()
    state = status.get('state', '????').title()
    actSong = int(status.get('song', '0')) + 1
    songLength = status.get('playlistlength', -1)
    volume = int(status.get('volume'))
    message = '{:5} - {:>2} / {:>2} @ {:03d} Vol. | Action: {:10}'.format(
        state, actSong, songLength, volume, action)
    print('\r' + message, end='')
    sys.stdout.flush()


def reset(client):
    client.stop()
    client.clear()


def disconnect(client):
    client.close()
    client.disconnect()


def connect():
    # MPD object instance
    client = MPDClient()
    if not mpdConnect(client, CON_ID):
        print('WARN NOT CONNECTED!')
        return None

    # Auth if password is set non False
    if PASSWORD:
        if mpdAuth(client, PASSWORD):
            print('Pass auth!')
        else:
            print('Error trying to pass auth.')
            client.disconnect()
            sys.exit(2)

    return client
