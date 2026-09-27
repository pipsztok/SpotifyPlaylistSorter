from spotify_helper import SpotifyHelper
from spotify_preview import get_spotify_preview_url
from preview_player import PreviewPlayer
# from simpleUI_screens import MainScreen
import threading
import json
import os


class Controller:
    __data_dir = "data"

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
        self.preview_url = None
        self.current_song_index = 0
        self.current_song_playlists = []
        self.selected_playlists = [] # indexes

        self.screen = None
        self.selected = []
        self.name = ""

        PreviewPlayer.init()

    def __load_preview(self):
        self.preview_url = get_spotify_preview_url(self.recent[self.current_song_index]['track']['id'])
        PreviewPlayer.load_preview(self.preview_url)

    def load_spotify_data(self, next_screen):
        def worker():
            self.username = self.sh.get_username()
            self.recent = self.sh.get_recently_played_tracks()
            self.playlists = self.sh.get_user_playlist()
            self.selected = [False] * len(self.playlists)

            try:
                with open(os.path.join(Controller.__data_dir, "selected_playlists.json"), "r") as f:
                    self.selected_playlists = json.load(f)
            except FileNotFoundError:
                self.selected_playlists = [x for x in range(len(self.playlists))]

            for p in self.selected_playlists:
                name = (self.playlists[p])['name']
                self.playlists_tracks[name] = []
                track_names = self.sh.get_playlist_tracks_names((self.playlists[p])['id'])
                for t in track_names:
                    print(t)
                    (self.playlists_tracks[name]).append(t)

            print(self.playlists_tracks)

            self.__load_preview()
            self.on_done(next_screen)
            # add error handling

        threading.Thread(target=worker, daemon=True).start()

    def on_done(self, next_screen):
        self.screen = next_screen
        self.data_loaded = True

    def select_playlist(self):
        index = self.list_playlists_names().index(self.name)
        self.selected[index] = False if self.selected[index] else True

    def toggle_select_playlist(self, name):
        i = self.list_playlists_names().index(name)
        if i in self.selected_playlists:
            self.selected_playlists.remove(i)
        else:
            self.selected_playlists.append(i)

    def toggle_add_to_playlist(self, playlist_name):
        i = self.list_playlists_names().index(playlist_name)
        playlist = self.playlists[i]
        if playlist_name in self.current_song_playlists:
            try:

                self.sh.remove_from_playlist(playlist['id'], self.recent[self.current_song_index]['track']['id'])
                self.current_song_playlists.remove(playlist_name)
                self.playlists_tracks[playlist].remove(self.recent[self.current_song_index]['track']['name'])
            except:
                pass
                #add error handling
        else:
            try:
                self.sh.add_to_playlist(playlist['id'], self.recent[self.current_song_index]['track']['id'])
                self.current_song_playlists.append(playlist_name)
                self.playlists_tracks[playlist].append(self.recent[self.current_song_index]['track']['name'])
            except:
                pass

    def save_selected_playlists(self):
        self.selected_playlists.sort()

    def current_track_title(self):
        if len(self.recent) == 0:
            return ""
        return self.recent[self.current_song_index]['track']['name']

    def list_playlists_names(self, selected = False):
        names = []

        for i, p in enumerate(self.playlists):
            if selected:
                if i not in self.selected_playlists:
                    continue
            names.append(p['name'])

        return names

    def list_tracks_in_playlists(self):
        # for each playlist do 'playlist_id' -> ['song1_id', 'song2_id', ...]
        pass

    def play_current_track(self):
        PreviewPlayer.play_pause_preview()

    def next_track(self):
        PreviewPlayer.stop_preview()

        self.current_song_index = min(self.current_song_index + 1, len(self.recent) - 1)
        current_song_name = self.recent[self.current_song_index]['track']['name']
        self.current_song_playlists.clear()
        for key in self.playlists_tracks.keys():
            if current_song_name in self.playlists_tracks[key]:
                self.current_song_playlists.append(key)
        # self.play_current_track()

        self.__load_preview()

    def prev_track(self):
        PreviewPlayer.stop_preview()

        self.current_song_index = max(self.current_song_index - 1, 0)
        # self.play_current_track()
        current_song_name = self.recent[self.current_song_index]['track']['name']
        self.current_song_playlists.clear()
        for key in self.playlists_tracks.keys():
            if current_song_name in self.playlists_tracks[key]:
                self.current_song_playlists.append(key)

        self.__load_preview()

    def on_close(self):
        os.makedirs(Controller.__data_dir, exist_ok=True)
        with open(os.path.join(Controller.__data_dir, "selected_playlists.json"), "w") as f:
            json.dump(self.selected_playlists, f)

    # find which playlists is the song in


# playlist_add_items(playlist_id, items, position=None)
# Adds tracks/episodes to a playlist
#
# Parameters:
# playlist_id - the id of the playlist
# items - a list of track/episode URIs or URLs
# position - the position to add the tracks

# playlist_remove_all_occurrences_of_items(playlist_id, items, snapshot_id=None)
# Removes all occurrences of the given tracks/episodes from the given playlist
#
# Parameters:
# playlist_id - the id of the playlist
# items - list of track/episode ids to remove from the playlist
# snapshot_id - optional id of the playlist snapshot