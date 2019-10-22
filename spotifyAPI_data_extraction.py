import requests
import pandas as pd
import sys
import spotipy
import spotipy.util as util

#code for authenticating a user (needed to access spotify information about a specific user)

scope = 'user-library-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token(username, scope, client_id = 'aad38808a7a746109ec09ba4c75bd7b5',
                                  client_secret = '19af4190d41e4392a5ce461a370492e2', redirect_uri = 'http://google.com/')

#spotipy object to access specific user data
sp = spotipy.Spotify(auth=token)

#gets the first 50 tracks this user's saved library
user_tracks = sp.current_user_saved_tracks(limit=50,offset=0)

#puts the track information into a dataframe, minus the limit, next, offset, previous, and total
#attributes becuase they will not be useful in our later analysis
tracks_df = pd.DataFrame(user_tracks)
tracks_df = tracks_df.drop('limit',axis=1)
tracks_df = tracks_df.drop('next',axis=1)
tracks_df = tracks_df.drop('offset',axis=1)
tracks_df = tracks_df.drop('previous',axis=1)
tracks_df = tracks_df.drop('total',axis=1)

#lists to hold the ids and artists of a track
ids = []
artists = []

#iterates throught the items column in data frame to extract the id and artist
#the id of the track can be used to get other atributes about the track
for track in tracks_df["items"]:
    ids.append(track.get('track').get('album').get('artists')[0].get('id'))
    artists.append(track.get('track').get('album').get('artists')[0].get('name'))

#adds the ids and artists to the dataframe
tracks_df["ids"] = ids
tracks_df["artist"] = artists
#takes out the items column from the data frame
tracks_df = tracks_df.drop('items',axis=1)

#saves tracks data frame to csv
tracks_df.to_csv("DS3000_50_saved_songs_data.csv")
