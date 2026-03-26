from __future__ import annotations

import pygame

from game.config import GAME
from game.persistence import GameProgress
from game.scenes.base import BaseScene


class GameplayScene(BaseScene):
    scene_id = "gameplay"

    def __init__(self, context) -> None:
        super().__init__(context)
        self.level_id = GAME.default_level_id
        self.start_level = context.progress.level
        self.base_hits = context.progress.hits
        self.base_misses = context.progress.misses

        self.level = self.context.level_registry.create(
            self.level_id,
            screen_size=self.context.screen_size,
            reaction_time=self.context.settings.reaction_ms / 1000.0,
            enemy_count=self.context.settings.enemy_count,
        )
        self.level.start()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.signal.next_scene = "splash"
            return

        self.level.handle_event(event)

    def update(self, dt: float) -> None:
        self.level.update(dt)
        if self.level.finished:
            hits = self.base_hits + self.level.hits_count
            misses = self.base_misses + self.level.misses_count
            self.signal.next_scene = "end"
            self.signal.payload = {
                "won": self.level.result.won,
                "reason": self.level.result.reason,
                "level": self.start_level,
                "hits": hits,
                "misses": misses,
            }

    def render(self, surface: pygame.Surface) -> None:
        self.level.render(surface)

    def runtime_progress_snapshot(self) -> GameProgress:
        return GameProgress(
            level=self.start_level,
            hits=self.base_hits + self.level.hits_count,
            misses=self.base_misses + self.level.misses_count,
        )
