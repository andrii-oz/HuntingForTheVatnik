from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import pygame


@dataclass
class SceneSignal:
    next_scene: Optional[str] = None
    payload: Optional[dict] = None
    quit_game: bool = False


class BaseScene(ABC):
    scene_id: str = "base"

    def __init__(self, context: "SceneContext") -> None:
        self.context = context
        self.signal = SceneSignal()

    def on_enter(self) -> None:
        return

    def on_exit(self) -> None:
        return

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...

    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        ...

    def consume_signal(self) -> SceneSignal:
        current = self.signal
        self.signal = SceneSignal()
        return current


@dataclass
class SceneContext:
    screen_size: tuple[int, int]
    assets: "AssetManager"
    audio: "AudioManager"
    input_manager: "InputManager"
    level_registry: "LevelRegistry"


from game.assets import AssetManager
from game.audio import AudioManager
from game.input import InputManager
from game.levels.level_registry import LevelRegistry
