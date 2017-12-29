from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
import requests
from urllib.parse import urlencode
import sys
import taglib
import os

getbpm_api_key = "notsureifishouldbesharingthis"

songdata = taglib.File(os.path.join(os.getcwd(), 'fireinthehole.flac'))
title = songdata.tags['TITLE'][0]
artist = songdata.tags['ARTIST'][0]
pretty_details = [title, artist]

def getBPM(artist, title, overwrite=False):
    existing_BPM = False
    if 'BPM' in songdata.tags and songdata.tags['BPM'] and songdata.tags['BPM'][0]:
        existing_BPM = True
        if overwrite:
            print('WARNING: BPM of', pretty_details, '@', str(songdata.tags['BPM']), 'will be overwritten!')
        else:
            print('Skipping', pretty_details, '- BPM tag exists')
            return  
        

    query = urlencode({'api_key': getbpm_api_key, 'type': 'both', 'lookup': 'artist:' + artist + 'song:' + title})
    req = requests.get(url='https://api.getsongbpm.com/search/?' + query)  
    if req.status_code == 200:
        api_data = req.json()
        if 'error' in api_data['search'] :
            if 'no result' in api_data['search']['error']:
                print('Could not find', pretty_details, 'will manually calculate!')
                #TODO: ... now manually calculate
            else:
                print(pretty_details, "returned", api_data['search']['error'], 'on getsongbpm.com')
        else:
            songdata.tags['BPM'] = api_data['search'][0]['tempo']
            songdata.save()
            print(pretty_details, 'updated to', songdata.tags['BPM'])
    else:
        print('<Problem running that query!>', '\n', req.text, '\n', "</Problem running that query!>")

def getMood():
    #TODO: do all the things
    return

def getLyrics():
    #TODO: do all the things
    return

#TODO: Make this a proper module like a decent human being?
getBPM(artist, title)