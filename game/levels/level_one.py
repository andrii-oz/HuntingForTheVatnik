from __future__ import annotations

import math
import random

import pygame

from game.levels.base import BaseLevel, LevelResult


class LevelOne(BaseLevel):
    level_id = "level_one"

    def __init__(
        self,
        screen_size: tuple[int, int],
        reaction_time: float,
        enemy_count: int = 1,
        assets=None,
        level_number: int = 1,
    ) -> None:
        super().__init__(
            screen_size=screen_size,
            reaction_time=reaction_time,
            enemy_count=enemy_count,
            assets=assets,
            level_number=level_number,
        )

        self.hud_font = pygame.font.Font(None, 46)
        self.target_pos = (screen_size[0] // 2, screen_size[1] // 2)

        self.hits_count = 0
        self.misses_count = 0
        self.rounds_played = 0

        self.time_left = reaction_time
        self.enemy_ready_delay = 0.8
        self.enemy_visible = False

        self.background = self._load_background()
        self.hud_image, self.hud_rect = self._load_hud()

        self.enemy_image = self._load_enemy_sprite()

        self.spawn_locations = self._build_spawn_locations()
        self.hitbox_size = self._build_hitbox_size()
        self.current_hitbox = pygame.Rect(0, 0, self.hitbox_size, self.hitbox_size)
        self.enemy_rect = self.enemy_image.get_rect(midbottom=self.current_hitbox.midbottom)

        self._last_spawn_index: int | None = None

    def _load_background(self) -> pygame.Surface:
        width, height = self.screen_size
        if self.assets is None:
            bg = pygame.Surface((width, height))
            bg.fill((204, 177, 137))
            return bg

        bg = self.assets.load_image(
            key="level1_background",
            relative_path="assets/background/background_main_1.jpg",
            fallback_color=(204, 177, 137),
        )
        return pygame.transform.smoothscale(bg, (width, height))

    def _load_hud(self) -> tuple[pygame.Surface, pygame.Rect]:
        width, height = self.screen_size

        if self.assets is None:
            fallback_hud = pygame.Surface((width, 120), pygame.SRCALPHA)
            fallback_hud.fill((20, 20, 20, 180))
            return fallback_hud, fallback_hud.get_rect(bottomleft=(0, height))

        hud = self.assets.load_image(
            key="level1_hud",
            relative_path="assets/ui/HUD.png",
            fallback_color=(30, 30, 30),
        )

        scale = width / max(1, hud.get_width())
        hud_h = int(hud.get_height() * scale)
        hud_h = max(90, min(180, hud_h))
        hud_scaled = pygame.transform.smoothscale(hud, (width, hud_h))
        return hud_scaled, hud_scaled.get_rect(bottomleft=(0, height))

    def _load_enemy_sprite(self) -> pygame.Surface:
        if self.assets is None:
            sprite = pygame.Surface((100, 120), pygame.SRCALPHA)
            pygame.draw.ellipse(sprite, (173, 34, 34), (0, 0, 100, 120))
            return sprite

        sprite = self.assets.load_image(
            key="enemy_1_idle_level",
            relative_path="assets/sprites/enemy_1_idle.png",
            fallback_color=(173, 34, 34),
        )
        return pygame.transform.smoothscale(sprite, (110, 132))

    def _build_spawn_locations(self) -> list[tuple[int, int]]:
        width, height = self.screen_size

        relative_locations = [
            (0.115, 0.355),  # top-left window: center-x, bottom-y
            (0.115, 0.705),  # bottom-left window
            (0.885, 0.355),  # top-right window
            (0.885, 0.705),  # bottom-right window
            (0.505, 0.640),  # center dumpster
        ]

        locations: list[tuple[int, int]] = []
        min_bottom = 120
        max_bottom = height - self.hud_rect.height - 14

        for rel_x, rel_bottom_y in relative_locations:
            cx = int(width * rel_x)
            by = int(height * rel_bottom_y)
            by = max(min_bottom, min(max_bottom, by))
            locations.append((cx, by))

        return locations

    def _build_hitbox_size(self) -> int:
        width, height = self.screen_size

        # Base window size approximation from layout, then 80% area.
        avg_window_w = width * 0.18
        avg_window_h = height * 0.22
        avg_window_area = avg_window_w * avg_window_h

        hitbox_area = avg_window_area * 0.80
        side = int(math.sqrt(hitbox_area))
        return max(40, side)

    def start(self) -> None:
        self._start_next_enemy()

    def _spawn_target(self) -> None:
        if not self.spawn_locations:
            cx, by = self.screen_size[0] // 2, self.screen_size[1] // 2
        else:
            choices = list(range(len(self.spawn_locations)))
            if self._last_spawn_index is not None and len(choices) > 1:
                choices.remove(self._last_spawn_index)
            idx = random.choice(choices)
            self._last_spawn_index = idx
            cx, by = self.spawn_locations[idx]

        self.current_hitbox = pygame.Rect(0, 0, self.hitbox_size, self.hitbox_size)
        self.current_hitbox.midbottom = (cx, by)
        self.enemy_rect = self.enemy_image.get_rect(midbottom=(cx, by))

    def _start_next_enemy(self) -> None:
        self.enemy_visible = False
        self.enemy_ready_delay = 0.45
        self.time_left = self.reaction_time
        self._spawn_target()

    def _finish_if_needed(self) -> None:
        if self.rounds_played < self.enemy_count:
            self._start_next_enemy()
            return

        self.finished = True
        self.result = LevelResult(
            won=self.hits_count > self.misses_count,
            reason="rounds_completed",
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.finished:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.enemy_visible:
            if self.current_hitbox.collidepoint(event.pos):
                self.hits_count += 1
                self.rounds_played += 1
                self._finish_if_needed()

    def update(self, dt: float) -> None:
        if self.finished:
            return

        if self.enemy_ready_delay > 0:
            self.enemy_ready_delay -= dt
            if self.enemy_ready_delay <= 0:
                self.enemy_visible = True
            return

        self.time_left -= dt
        if self.time_left <= 0:
            self.misses_count += 1
            self.rounds_played += 1
            self._finish_if_needed()

    def render(self, surface: pygame.Surface) -> None:
        width, height = self.screen_size

        surface.blit(self.background, (0, 0))
        if self.enemy_visible:
            surface.blit(self.enemy_image, self.enemy_rect)

        surface.blit(self.hud_image, self.hud_rect)

        y = height - self.hud_rect.height // 2
        level_text = self.hud_font.render(str(self.level_number), True, (65, 120, 255))
        hits_text = self.hud_font.render(str(self.hits_count), True, (32, 202, 72))
        misses_text = self.hud_font.render(str(self.misses_count), True, (224, 58, 58))

        surface.blit(level_text, level_text.get_rect(center=(int(width * 0.17), y)))
        surface.blit(hits_text, hits_text.get_rect(center=(width // 2, y)))
        surface.blit(misses_text, misses_text.get_rect(center=(int(width * 0.83), y)))
