from __future__ import annotations

import pygame

from game.scenes.base import BaseScene
from game.ui import Button


class EndScene(BaseScene):
    scene_id = "end"

    def __init__(self, context, payload: dict | None = None) -> None:
        super().__init__(context)
        payload = payload or {}
        self.won = bool(payload.get("won", False))
        self.reason = str(payload.get("reason", ""))

        w, h = context.screen_size
        self.title_font = pygame.font.Font(None, 92)
        self.body_font = pygame.font.Font(None, 40)
        self.restart_button = Button("Play Again", pygame.Rect(w // 2 - 130, h // 2 + 36, 260, 54))
        self.menu_button = Button("Main Menu", pygame.Rect(w // 2 - 130, h // 2 + 102, 260, 54))

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.signal.next_scene = "splash"
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.restart_button.hit_test(pos):
                self.signal.next_scene = "gameplay"
            elif self.menu_button.hit_test(pos):
                self.signal.next_scene = "splash"

    def update(self, dt: float) -> None:
        _ = dt

    def render(self, surface: pygame.Surface) -> None:
        if self.won:
            surface.fill((186, 224, 174))
            title = "YOU WIN"
            subtitle = "Fast reaction"
        else:
            surface.fill((228, 170, 160))
            title = "YOU LOSE"
            subtitle = f"Reason: {self.reason or 'unknown'}"

        w, _ = self.context.screen_size
        title_img = self.title_font.render(title, True, (34, 30, 26))
        surface.blit(title_img, title_img.get_rect(center=(w // 2, 180)))

        subtitle_img = self.body_font.render(subtitle, True, (34, 30, 26))
        surface.blit(subtitle_img, subtitle_img.get_rect(center=(w // 2, 250)))

        mouse_pos = self.context.input_manager.mouse_pos
        self.restart_button.draw(surface, self.body_font, self.restart_button.hit_test(mouse_pos))
        self.menu_button.draw(surface, self.body_font, self.menu_button.hit_test(mouse_pos))
