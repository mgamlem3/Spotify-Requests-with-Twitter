#coding=utf-8
#//  File Name:  LyricsCheck
#//  Project Name:  Spotify-Requests-with-Twitter
#//
#//  Created by Michael Gamlem III on January 13, 2018
#//  Copyright © 2018 Michael Gamlem III. All rights reserved.

import urllib3

#make URL
def makeURL(track, artist):
    URL = "https://genius.com/"
    #https://genius.com/Kings-kaleidoscope-a-prayer-lyrics

    #convert strings to lowercase and strip whitespace and replace spaces
    track = track.lower().strip().replace(" ", "-")
    artist = artist.lower().strip().replace(" ", "-")

    #make a url in genius.com format
    URL = URL + artist + "-" + track + "-lyrics"

    #connect to URL
    try:
        http = urllib3.PoolManager()
        print("Requesting URL: {}".format(URL))
        response = http.request("GET", URL)

        #check for 200 response
        if(response.status == 200):
            return response.data

        #raise exception
        else:
            raise Exception("Response other than 200 returned.\nReceived Response code: {}".format(response.status))

    except Exception as e:
        print(e)

    return "Exception Occurred"

def getLyrics(URL):
    return 0

def parseLyrics():
    return 0

# check lyrics with genius.com
def checkLyrics(track, artist):
    explicit = False

    URL = makeURL(track, artist)
    getLyrics(URL)

    return explicit