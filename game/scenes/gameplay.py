from __future__ import annotations

import pygame

from game.config import GAME
from game.scenes.base import BaseScene


class GameplayScene(BaseScene):
    scene_id = "gameplay"

    def __init__(self, context) -> None:
        super().__init__(context)
        self.level_id = GAME.default_level_id
        self.level = self.context.level_registry.create(
            self.level_id,
            screen_size=self.context.screen_size,
            reaction_time=GAME.reaction_time_sec,
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
            self.signal.next_scene = "end"
            self.signal.payload = {
                "won": self.level.result.won,
                "reason": self.level.result.reason,
            }

    def render(self, surface: pygame.Surface) -> None:
        self.level.render(surface)
        self._draw_crosshair(surface)

    def _draw_crosshair(self, surface: pygame.Surface) -> None:
        x, y = self.context.input_manager.mouse_pos
        pygame.draw.circle(surface, (20, 20, 20), (x, y), 20, width=2)
        pygame.draw.line(surface, (20, 20, 20), (x - 26, y), (x + 26, y), width=2)
        pygame.draw.line(surface, (20, 20, 20), (x, y - 26), (x, y + 26), width=2)
