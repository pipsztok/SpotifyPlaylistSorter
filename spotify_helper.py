from operator import indexOf
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyHelper:
    def __init__(self, debug=False):
        load_dotenv()

        self.scope = ["user-library-read",
                 "playlist-read-private",
                 "playlist-read-collaborative",
                 "playlist-modify-private",
                 "playlist-modify-public",
                 "user-read-recently-played"]

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scope,
                client_id=os.getenv("SPOTIFY_CLIENT_ID"), client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                redirect_uri=os.getenv("REDIRECT_URI")))
        
        self.me = self.sp.me()
        self.debug = debug

    def get_user_playlist(self):
        playlists = self.sp.current_user_playlists(limit=50)
        my_playlists = []
        i = 0

        while True:
            my_playlists.extend([item for item in playlists['items'] if item['owner']['display_name'] == self.me['display_name']])
            if self.debug:
                print(playlists)
                for item in my_playlists:
                    if item['owner']['display_name'] == self.me['display_name']:
                        print("%d %s" % (indexOf(my_playlists, item), item['name']))

            if len(playlists['items']) == 0 or playlists['next'] is None:
                break

            playlists = self.sp.current_user_playlists(limit=50, offset=50*(i := i+1))

        return my_playlists

    def get_recently_played_tracks(self):
        results = self.sp.current_user_saved_tracks()
        if self.debug:
            for idx, item in enumerate(results['items']):
                track = item['track']
                print(idx, track['artists'][0]['name'], " – ", track['name'])
        return results