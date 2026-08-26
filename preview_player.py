import os
import requests
import pygame


class PreviewPlayer:
    preview_dir = "previews"

    def __init__(self):
        self.mixer = pygame.mixer
        self.mixer.init()

        os.makedirs(PreviewPlayer.preview_dir, exist_ok=True)

    def play_preview(self, url):
        response = requests.get(url)

        with open(os.path.join(PreviewPlayer.preview_dir, "preview.mp3"), "wb") as f:
            f.write(response.content)

        self.mixer.music.load(os.path.join(PreviewPlayer.preview_dir, "preview.mp3"))
        self.mixer.music.play()

        # Poczekaj aż odtwarzanie się skończy
        while self.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

# url = "https://p.scdn.co/mp3-preview/9f6b0748625b642efa50078f9a9c11e88ef5e6c2"
