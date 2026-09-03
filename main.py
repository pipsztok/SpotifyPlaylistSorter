import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotify_helper import SpotifyHelper
from spotify_preview import get_spotify_preview_url
from preview_player import PreviewPlayer
from textual_app import SpotifyPlaylistSorterApp

scope = ["user-library-read",
         "playlist-read-private",
         "playlist-read-collaborative",
         "playlist-modify-private",
         "playlist-modify-public",
         "user-read-recently-played"]

sh = SpotifyHelper(debug=True)

# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])

recent = sh.get_recently_played_tracks()
# print("\n\n")
# print(recent)
# for idx, item in enumerate(recent['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])

print("\n\n")
# playlists = sp.current_user_playlists(limit=50)
playlists = sh.get_user_playlist()
print(playlists)
# me = sp.me()
# print(playlists['items'][0])
# for i, item in enumerate(playlists['items']):
#     if item['owner']['display_name'] == me['display_name']:
#         print("%d %s" % (i, item['name']))
    # print("%s" % ())

preview_url = get_spotify_preview_url('1301WleyT98MSxVHPZCA6M')
print(preview_url)
PreviewPlayer.init()
PreviewPlayer.play_preview(preview_url)


if __name__ == "__main__":
    pass
    # app = SpotifyPlaylistSorterApp()
    # app.run()
