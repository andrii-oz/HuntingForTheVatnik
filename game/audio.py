from __future__ import annotations

from pathlib import Path

import pygame


class SilentSound:
    def play(self) -> None:
        return

    def stop(self) -> None:
        return


class AudioManager:
    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.enabled = False
        self._sounds: dict[str, pygame.mixer.Sound | SilentSound] = {}

        try:
            pygame.mixer.init()
            self.enabled = True
        except pygame.error:
            self.enabled = False

    def load_sound(self, key: str, relative_path: str) -> None:
        if key in self._sounds:
            return

        path = self.root_dir / relative_path
        if self.enabled and path.exists():
            self._sounds[key] = pygame.mixer.Sound(path.as_posix())
        else:
            self._sounds[key] = SilentSound()

    def play(self, key: str) -> None:
        sound = self._sounds.get(key)
        if sound is not None:
            sound.play()
