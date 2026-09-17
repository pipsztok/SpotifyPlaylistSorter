import os
import requests
import pygame


class PreviewPlayer:
    preview_dir = "previews"
    _paused = False
    _initialized = False

    @classmethod
    def init(cls):
        if not cls._initialized:
            pygame.mixer.init()
            os.makedirs(cls.preview_dir, exist_ok=True)
            cls._initialized = True

    @staticmethod
    def play_preview(url):
        response = requests.get(url)

        with open(os.path.join(PreviewPlayer.preview_dir, "preview.mp3"), "wb") as f:
            f.write(response.content)

        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(PreviewPlayer.preview_dir, "preview.mp3"))
        pygame.mixer.music.play()

        # Poczekaj aż odtwarzanie się skończy
        # while pygame.mixer.music.get_busy():
        #     pygame.time.Clock().tick(10)

    @staticmethod
    def pause_preview():
        if not PreviewPlayer._paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.play()

# url = "https://p.scdn.co/mp3-preview/9f6b0748625b642efa50078f9a9c11e88ef5e6c2"
