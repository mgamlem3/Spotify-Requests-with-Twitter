# coding=utf-8
#  File Name:  getPlaylistID
#  Project Name:  Spotify-Requests-with-Twitter
#
#  Created by Michael Gamlem III on January 03, 2018
#  Copyright © 2018 Michael Gamlem III. All rights reserved.

import spotipy
import spotipy.util as util

# stores secret information
authInfo = [None] * 9


def getPlaylistID(token, username):
    if token:
        # authorize with Spotify
        sp = spotipy.Spotify(auth=token)

    ###From Spotipy documentation###
        playlists = sp.user_playlists(username)
        while playlists:
            for i, playlist in enumerate(playlists['items']):
                print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'], playlist['name']))
            if playlists['next']:
                playlists = sp.next(playlists)
            else:
                playlists = None
    ###
    else:
        print("Can't get token for", username)


# will get secret information from file
# will store in an array to be accessed that variables will be set from
def getAuthInfo():
    info = open("authentication.txt")
    i = 0
    while i < 9:
        line = info.readline().split()
        # print(line[2])
        authInfo[i] = str(line[2])
        i = i + 1
    info.close()


def authenticate():
    # Authenticate to Spotify
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
    getPlaylistID(token, username)


getAuthInfo()
authenticate()
