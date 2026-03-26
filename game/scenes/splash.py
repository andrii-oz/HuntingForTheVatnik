from __future__ import annotations

import pygame

from game.ui import Button
from game.scenes.base import BaseScene


class SplashScene(BaseScene):
    scene_id = "splash"

    def __init__(self, context) -> None:
        super().__init__(context)
        w, h = context.screen_size
        self.title_font = pygame.font.Font(None, 90)
        self.menu_font = pygame.font.Font(None, 42)
        self.show_settings = False

        self.start_button = Button("Start", pygame.Rect(w // 2 - 120, h // 2 - 30, 240, 52))
        self.settings_button = Button("Settings", pygame.Rect(w // 2 - 120, h // 2 + 36, 240, 52))
        self.quit_button = Button("Quit", pygame.Rect(w // 2 - 120, h // 2 + 102, 240, 52))

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.signal.quit_game = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            self.show_settings = not self.show_settings

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.start_button.hit_test(pos):
                self.signal.next_scene = "gameplay"
            elif self.settings_button.hit_test(pos):
                self.show_settings = not self.show_settings
            elif self.quit_button.hit_test(pos):
                self.signal.quit_game = True

    def update(self, dt: float) -> None:
        _ = dt

    def render(self, surface: pygame.Surface) -> None:
        width, _ = self.context.screen_size
        surface.fill((236, 217, 188))

        title = self.title_font.render("Hunting For The Vatnik", True, (35, 28, 22))
        surface.blit(title, title.get_rect(center=(width // 2, 160)))

        mouse_pos = self.context.input_manager.mouse_pos
        self.start_button.draw(surface, self.menu_font, self.start_button.hit_test(mouse_pos))
        self.settings_button.draw(surface, self.menu_font, self.settings_button.hit_test(mouse_pos))
        self.quit_button.draw(surface, self.menu_font, self.quit_button.hit_test(mouse_pos))

        hint = self.menu_font.render("S - toggle settings", True, (70, 60, 48))
        surface.blit(hint, (24, 24))

        if self.show_settings:
            self._render_settings(surface)

    def _render_settings(self, surface: pygame.Surface) -> None:
        w, h = self.context.screen_size
        panel = pygame.Rect(w // 2 - 260, h // 2 - 130, 520, 240)
        pygame.draw.rect(surface, (255, 248, 236), panel, border_radius=14)
        pygame.draw.rect(surface, (68, 58, 46), panel, width=2, border_radius=14)

        lines = [
            "Settings (stub for future modules)",
            "- Mouse sensitivity: default",
            "- Sound volume: 100%",
            "- Difficulty: normal",
        ]

        y = panel.top + 24
        for line in lines:
            text = self.menu_font.render(line, True, (40, 34, 28))
            surface.blit(text, (panel.left + 24, y))
            y += 42
