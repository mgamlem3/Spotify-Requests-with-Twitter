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
scope = 'user-library-read playlist-modify-public'

# current username
username = 'mgamlem3'
# CS 313 Playlist
playlist_id = '3iZ0kkNGnUWbah7jgyEMGz'

# authorization information for Spotify Web API
token = util.prompt_for_user_token(username, scope, client_id='72769ea151c446b5af6db14409bce6d7',
                                                    client_secret='10b9b03feecc4be891d8fd4b3037e34b',
                                                    redirect_uri='http://localhost:8888/callback')

########

#### Authenticate to Twitter ####
# Authorization Keys for Twitter API
CONSUMER_KEY = 'fmSSXCDXX7CNyRxGxnSdAO3F2'
CONSUMER_SECRET = 'JlzpHRlLDMnbNNFdMpVqNeDEYxxPkAWWdwNKCkfz6t1iLNMWnj'
ACCESS_TOKEN = '879480356486782976-vkRkfL1kpWSwuneodcHt97Z0qSbbLsB'
ACESS_SECRET = 'oiVDk6znp8KiNdF6I6bP2GsfYTicde9cZBcSjzEHNCQcC'

# Library functions for handling all of the authorizations with Twitter
AUTH = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACESS_SECRET)
API = tweepy.API(AUTH)

########

# This loop will continually search Twitter until a matching tweet is found
# run this program until terminated by user
while (True):
    # only ask Twitter once per minute to avoid 429 error
    if (not first):
        print("Sleeping for 1 minute...\n")
        time.sleep(60)

    # ask Twitter for information
    try:
        print("Making Twitter Request...\n")
        RESULTS = tweepy.Cursor(API.search, q='CS313Whitworth2017').items(10)
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

    # if a tweet is found pass to Spotify
    for tweet in RESULTS:
        # display tweet
        print("\tTweet Found:")
        print(tweet.created_at, tweet.text, tweet.lang, tweet.id)
        tweetID = str(tweet.id)

        #check to see if Tweet has already been found
        filein = open("Tweets.txt")
        if tweetID in filein.read():
            continue
        filein.close()

        #store Tweet ID
        fileout = open("Tweets.txt", 'a')
        fileout.write(tweetID)
        fileout.write("\n")
        fileout.close()

        # prepare tweet to be sent to Spotify
        search = tweet.text
        # drop everything after the hastag "#...."
        search = search.split("#", 1)[0]

        # make Spotify request
        print("Making Spotify Request for: \"" + search + "\"\n")
        if (search != ""):
            addSong(search)

    # not first run anymore
    first = False