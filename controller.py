from spotify_helper import SpotifyHelper
from spotify_preview import get_spotify_preview_url
from preview_player import PreviewPlayer
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
        self.current_song_index = 0

        self.line_num = 0
        self.playlist_list_start = 0
        self.selection_symbol = '$'
        self.lines = []
        self.selected = []
        self.name = ""

        PreviewPlayer.init()
        self.load_spotify_data()

    def load_spotify_data(self):
        def worker():
            self.username = self.sh.get_username()
            self.recent = self.sh.get_recently_played_tracks()
            self.playlists = self.sh.get_user_playlist()
            self.selected = [False] * len(self.playlists)
            self.on_done()
            # add error handling

        threading.Thread(target=worker, daemon=True).start()

    def on_done(self):
        self.data_loaded = True

    def select_playlist(self):
        index = self.list_playlists_names().index(self.name)
        self.selected[index] = False if self.selected[index] else True

    def current_track_title(self):
        if len(self.recent) == 0:
            return ""
        return self.recent[self.current_song_index]['track']['name']

    def list_playlists_names(self):
        names = []

        for p in self.playlists:
            names.append(p['name'])

        return names

    def list_tracks_in_playlists(self):
        # for each playlist do 'playlist_id' -> ['song1_id', 'song2_id', ...]
        pass

    def play_current_track(self):
        preview_url = get_spotify_preview_url(self.recent[self.current_song_index]['track']['id'])
        PreviewPlayer.play_preview(preview_url)

    def next_track(self):
        self.current_song_index = min(self.current_song_index + 1, len(self.recent) - 1)
        self.play_current_track()

    def prev_track(self):
        self.current_song_index = max(self.current_song_index - 1, 0)
        self.play_current_track()

    # find which playlists is the song in
