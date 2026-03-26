from __future__ import annotations

from pathlib import Path

import pygame


class AssetManager:
    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self._images: dict[str, pygame.Surface] = {}

    def load_image(self, key: str, relative_path: str, fallback_color: tuple[int, int, int]) -> pygame.Surface:
        if key in self._images:
            return self._images[key]

        path = self.root_dir / relative_path
        if path.exists():
            image = pygame.image.load(path.as_posix()).convert_alpha()
        else:
            image = pygame.Surface((128, 128), pygame.SRCALPHA)
            image.fill((*fallback_color, 255))
        self._images[key] = image
        return image

    def get_image(self, key: str) -> pygame.Surface | None:
        return self._images.get(key)
