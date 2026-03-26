from __future__ import annotations

import random

import pygame

from game.levels.base import BaseLevel, LevelResult


class LevelOne(BaseLevel):
    level_id = "level_one"

    def __init__(self, screen_size: tuple[int, int], reaction_time: float) -> None:
        super().__init__(screen_size, reaction_time)
        self.font = pygame.font.Font(None, 42)
        self.target_radius = 36
        self.target_pos = (screen_size[0] // 2, screen_size[1] // 2)
        self.time_left = reaction_time
        self.enemy_ready_delay = 0.8
        self.enemy_visible = False
        self.state_text = "Get ready..."

    def start(self) -> None:
        self._spawn_target()

    def _spawn_target(self) -> None:
        margin = 120
        x = random.randint(margin, self.screen_size[0] - margin)
        y = random.randint(margin, self.screen_size[1] - margin)
        self.target_pos = (x, y)

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.finished:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.enemy_visible:
            dx = event.pos[0] - self.target_pos[0]
            dy = event.pos[1] - self.target_pos[1]
            if dx * dx + dy * dy <= self.target_radius * self.target_radius:
                self.finished = True
                self.result = LevelResult(won=True, reason="enemy_down")
            else:
                self.finished = True
                self.result = LevelResult(won=False, reason="missed_shot")

    def update(self, dt: float) -> None:
        if self.finished:
            return

        if self.enemy_ready_delay > 0:
            self.enemy_ready_delay -= dt
            if self.enemy_ready_delay <= 0:
                self.enemy_visible = True
                self.state_text = "SHOOT!"
            return

        self.time_left -= dt
        if self.time_left <= 0:
            self.finished = True
            self.result = LevelResult(won=False, reason="too_slow")

    def render(self, surface: pygame.Surface) -> None:
        width, height = self.screen_size
        surface.fill((204, 177, 137))

        status = self.font.render(self.state_text, True, (20, 20, 20))
        surface.blit(status, (32, 24))

        timer_text = self.font.render(f"Time: {max(self.time_left, 0):.2f}", True, (20, 20, 20))
        surface.blit(timer_text, (width - 220, 24))

        if self.enemy_visible:
            pygame.draw.circle(surface, (173, 34, 34), self.target_pos, self.target_radius)
            pygame.draw.circle(surface, (255, 240, 230), self.target_pos, self.target_radius - 8)

        pygame.draw.rect(surface, (153, 104, 67), (0, height - 120, width, 120))
