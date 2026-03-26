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
        self.music_enabled = True
        self.effects_enabled = True
        self._sounds: dict[str, pygame.mixer.Sound | SilentSound] = {}
        self._current_music_path: str | None = None

        try:
            pygame.mixer.init()
            self.enabled = True
        except pygame.error:
            self.enabled = False

    def set_toggles(self, music_enabled: bool, effects_enabled: bool) -> None:
        self.music_enabled = music_enabled
        self.effects_enabled = effects_enabled

        if not self.music_enabled:
            self.stop_music()

    def load_sound(self, key: str, relative_path: str) -> None:
        if key in self._sounds:
            return

        path = self.root_dir / relative_path
        if self.enabled and path.exists():
            self._sounds[key] = pygame.mixer.Sound(path.as_posix())
        else:
            self._sounds[key] = SilentSound()

    def play(self, key: str) -> None:
        if not self.effects_enabled:
            return

        sound = self._sounds.get(key)
        if sound is not None:
            sound.play()

    def play_music(self, relative_path: str, loop: int = -1, volume: float = 0.7) -> None:
        if not self.enabled or not self.music_enabled:
            return

        path = self.root_dir / relative_path
        if not path.exists():
            return

        normalized = path.as_posix()
        if self._current_music_path == normalized and pygame.mixer.music.get_busy():
            return

        pygame.mixer.music.load(normalized)
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))
        pygame.mixer.music.play(loop)
        self._current_music_path = normalized

    def stop_music(self) -> None:
        if not self.enabled:
            return

        pygame.mixer.music.stop()
        self._current_music_path = None
