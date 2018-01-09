#!/usr/bin/env python
#
#  File Name:  Server.py
#  Project Name:  Spotify - Twitter Requests
#  Created by Michael Gamlem III on January 3, 2018
#  Copyright 2018 Michael Gamlem III. All Rights Reserved
#
#  Based upon final project from CS 313 Fall Semester at Whitworth University
#  Adapted with permission
#  Code can be found at: https://github.com/mgamlem3/CS-313/blob/master/Final%20Project/Final/SpotifyANDTwitter.py
#  Originally Created by Michael Gamlem III and Colin Brondy on December 4, 2017
#  Copyright 2017 Michael Gamlem III and Colin Brondy. All rights reserved.
#
# Description:
#   This application will search Twitter for a specified hashtag
#   and add then add requests with that hashtag to a Spotify
#   Playlist.

import spotipy
import spotipy.util as util
import tweepy
from tweepy import OAuthHandler
import time

# variable to check if first run
first = True
# stores secret information
authInfo = [None] * 9
# hashtag to search for
HASHTAG = "#WhitworthSpringNShout"


# will get secret information from file
# will store in an array to be accessed that variables will be set from
def getAuthInfo():
    info = open("authentication.txt")
    i = 0
    while i < 9:
        line = info.readline().split()
        authInfo[i] = str(line[2])
        i = i + 1
    info.close()


# Will add songs to Spotify Playlist
# must pass in a search string
def addSong(search):
    if token:
        # authorize with Spotify
        sp = spotipy.Spotify(auth=token)

        # search for track
        result = sp.search(search, 1, 0, 'track')

        # if a result was found in the database
        if (result['tracks']['items']):
            print("--- Found Result in Spotify Database ----")
            print(result['tracks']['items'])

            # must be list due to bug in Spotipy library even if only searching for one song
            track_id = []
            # append track uri to list
            track_id.append(result['tracks']['items'][0]['uri'])

            # add item to playlist
            results = sp.user_playlist_add_tracks(username, playlist_id, track_id)
            if (results):
                print(track_id[0] + " added successfully")
                track_id.pop()
            else:
                print(track_id[0] + " was not added")
                track_id.pop()

            # clear
            result.clear()
            results.clear()

    else:
        print("Can't get token for", username)


#### Authenticate to Spotify ####
# scope that the program is allowed

getAuthInfo()

scope = 'user-library-read playlist-modify-public'

# current username
username = authInfo[0]
# CS 313 Playlist
playlist_id = authInfo[1]

# authorization information for Spotify Web API
token = util.prompt_for_user_token(username, scope, client_id=authInfo[2],
                                   client_secret=authInfo[3],
                                   redirect_uri=authInfo[4])
########

#### Authenticate to Twitter ####
# Authorization Keys for Twitter API
CONSUMER_KEY = authInfo[5]
CONSUMER_SECRET = authInfo[6]
ACCESS_TOKEN = authInfo[7]
ACCESS_SECRET = authInfo[8]

# Library functions for handling all of the authorizations with Twitter
AUTH = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
API = tweepy.API(AUTH)

########

# This loop will continually search Twitter until a matching tweet is found
# Run this program until terminated by user
while (True):
    # check for authorization info on first run
    if (first):
        getAuthInfo()

    # only ask Twitter once per minute to avoid 429 error
    if (not first):
        print("Sleeping for 1 minute...\n")
        time.sleep(60)

    # ask Twitter for information
    try:
        print("Making Twitter Request...\n")
        RESULTS = tweepy.Cursor(API.search, q=HASHTAG, show_user='true', since_id='0').items(10)
        print(RESULTS)

    # if 429 error, wait 15 minutes until we can request again
    except tweepy.error.TweepError:
        print("429 Error.  Sleeping for 15 minutes\n")
        time.sleep(60 * 15)
        continue

    # if other exception, break program execution
    except StopIteration:
        print("UNKNOWN EXCEPTION\nTERMINATING PROGRAM\n")
        break

    except Exception as e:
        print("Other Error {}").format(e)

    # if a tweet is found pass to Spotify
    for tweet in RESULTS:
        # display tweet
        print("\tTweet Found:")
        print("{} {} {} {}").format(tweet.created_at, tweet.text, tweet.lang, tweet.id)
        tweetID = str(tweet.id)

        # check to see if Tweet has already been found
        filein = open("Tweets.txt")
        if tweetID in filein.read():
            continue
        filein.close()

        # store Tweet ID
        fileout = open("Tweets.txt", 'a')
        fileout.write(tweetID)
        fileout.write("\n")
        fileout.close()

        # prepare tweet to be sent to Spotify
        search = tweet.text

        # drop everything after the hastag "#...."
        search = search.split("#", 1)[0]

        # make Spotify request
        print("Making Spotify Request for: \"{}\"").format(search)
        if (search != ""):
            addSong(search)

    # not first run anymore
    first = False
