from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import pygame


@dataclass
class LevelResult:
    won: bool
    reason: str = ""


class BaseLevel(ABC):
    level_id: str = "base_level"

    def __init__(self, screen_size: tuple[int, int], reaction_time: float, enemy_count: int = 1) -> None:
        self.screen_size = screen_size
        self.reaction_time = reaction_time
        self.enemy_count = enemy_count
        self.finished = False
        self.result = LevelResult(won=False, reason="unfinished")

    @abstractmethod
    def start(self) -> None:
        ...

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...

    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        ...
