from __future__ import annotations

import pygame

from game.assets import AssetManager
from game.input import InputManager


class CursorManager:
    def __init__(self, assets: AssetManager, input_manager: InputManager, size: int = 44) -> None:
        self.input_manager = input_manager

        green = assets.load_image(
            key="cursor_green",
            relative_path="assets/ui/crosshair_green.png",
            fallback_color=(24, 220, 24),
        )
        red = assets.load_image(
            key="cursor_red",
            relative_path="assets/ui/crosshair_red.png",
            fallback_color=(220, 24, 24),
        )

        self.green_cursor = pygame.transform.smoothscale(green, (size, size))
        self.red_cursor = pygame.transform.smoothscale(red, (size, size))
        self.hotspot = (size // 2, size // 2)

    def update(self, dt: float) -> None:
        self.input_manager.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        if not pygame.mouse.get_focused():
            return

        x, y = self.input_manager.mouse_pos
        use_red = self.input_manager.left_button_down or self.input_manager.is_click_flash_active
        cursor = self.red_cursor if use_red else self.green_cursor
        surface.blit(cursor, (x - self.hotspot[0], y - self.hotspot[1]))
