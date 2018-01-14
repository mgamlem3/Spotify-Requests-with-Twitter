# coding=utf-8
# //  File Name:  LyricsCheck
# //  Project Name:  Spotify-Requests-with-Twitter
# //
# //  Created by Michael Gamlem III on January 13, 2018
# //  Copyright © 2018 Michael Gamlem III. All rights reserved.

import urllib3
import re

# makes URL for genius.com
def makeURL(track, artist):
    URL = "https://genius.com/"

    # convert strings to lowercase and strip whitespace and replace spaces
    track = track.lower().strip().replace(" ", "-")
    artist = artist.lower().strip().replace(" ", "-")

    # make a url in genius.com format
    URL = URL + artist + "-" + track + "-lyrics"

    return URL


# connects to URL given
def makeHTTPRequest(URL):
    # connect to URL
    try:
        http = urllib3.PoolManager()
        print("Requesting URL: {}".format(URL))
        response = http.request("GET", URL)

        # check for 200 response
        if response.status == 200:
            return response.data

        # raise exception
        else:
            raise Exception("Response other than 200 returned.\nReceived Response code: {}".format(response.status))

    except Exception as e:
        print(e)

    return ""

#parses lyrics to look for explicit content
#returns string with true, false, or not found
def parseResponse(artist, track, response):
    regex = "is_explicit[\"\,\d\w\:\[]+"
    # if response is empty, add song to list that needs to be checked by human
    if response == "":
        file = open("SongsWithNoResponse.txt", 'a')
        file.write("---Song---\tTitle: {}\n\tArtist: {}".format(track, artist))
        return "not found"

    #search for explicit flag in response
    else:
        found = re.match(regex, response)
        if found != None:
            #search for true
            #index of location is ignored, only looking for true or false value
            index = found.group(0).find('true' or 'True')
            if index != -1:
                return "true"
            # search for true
            # index of location is ignored, only looking for true or false value
            index = found.group(0).find('false' or 'False')
            if index != -1:
                return "false"

        #regular expression was not matched
        else:
            file = open("SongsWithNoResponse.txt", 'a')
            file.write("---Song---\tTitle: {}\n\tArtist: {}".format(track, artist))
            return "not found"


# check lyrics with genius.com
# returns bool to see if song is explicit or not
def checkLyrics(track, artist):
    URL = makeURL(track, artist)
    response = makeHTTPRequest(URL)
    explicit = parseResponse(artist, track, response)
    if explicit == "true":
        return True
    elif explicit == "false":
        return False
    elif explicit == "not found":
        print("LYRICS COULD NOT BE VERIFIED FOR {} BY {}".format(track, artist))
        return False