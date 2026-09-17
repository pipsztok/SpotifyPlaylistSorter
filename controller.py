from spotify_helper import SpotifyHelper
import threading


class Controller:
    def __init__(self):
        self.sh = SpotifyHelper()
        # self.username = self.sh.get_username()
        # self.recent = self.sh.get_recently_played_tracks()
        # self.playlists = self.sh.get_user_playlist()
        self.data_loaded = False
        self.username = ""
        self.recent = []
        self.playlists = []
        self.playlists_to_add = []
        self.playlists_to_remove = []
        self.playlists_tracks = {}

        self.line_num = 0
        self.playlist_list_start = 0

        self.load_spotify_data()

    def load_spotify_data(self):
        def worker():
            self.username = self.sh.get_username()
            self.recent = self.sh.get_recently_played_tracks()
            self.playlists = self.sh.get_user_playlist()
            self.on_done()

        threading.Thread(target=worker, daemon=True).start()

    def on_done(self):
        self.data_loaded = True

    def recent_track_title(self):
        if len(self.recent) == 0:
            return ""
        return self.recent[0]['track']['name']

    def list_playlists_names(self):
        names = []

        for p in self.playlists:
            names.append(p['name'])

        return names

    def list_tracks_in_playlists(self):
        # for each playlist do 'playlist_id' -> ['song1_id', 'song2_id', ...]
        pass

    # find which playlists is the song in
