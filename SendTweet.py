#coding=utf-8
# File Name:  SendTweet
# Project Name:  Spotify-Requests-with-Twitter
#
# Created by Michael Gamlem III on January 14, 2018
# Copyright © 2018 Michael Gamlem III. All rights reserved.

# used to tell of successful adding to playlist
def tweetSuccess(tweetID, tweetUsername, trackName, artistName, tweepy):
    # create tweet to send
    tweetText = "@{} Your song was added.  We hope to see you at Spring n\' Shout!".format(tweetUsername)
    tweepy.update_status(tweetText, tweetID)

# used to tell of explicit song
def tweetExplicit(tweetID, tweetUsername, trackName, artistName, tweepy):
    # create tweet to send
    tweetText = "@{} Your song may be explicit.  Don't worry, we have someone who will review it to see if it should be on the playlist".format(tweetUsername)
    tweepy.update_status(tweetText, tweetID)