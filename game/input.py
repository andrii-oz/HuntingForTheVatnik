from __future__ import annotations

import pygame


class InputManager:
    def __init__(self) -> None:
        self.mouse_pos = (0, 0)
        self.left_clicked = False
        self.left_button_down = False
        self._click_flash_timer = 0.0

    def begin_frame(self) -> None:
        self.left_clicked = False

    def update(self, dt: float) -> None:
        if self._click_flash_timer > 0:
            self._click_flash_timer = max(0.0, self._click_flash_timer - dt)

    def consume_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.left_clicked = True
            self.left_button_down = True
            self._click_flash_timer = 0.12
            self.mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.left_button_down = False
            self.mouse_pos = event.pos

    @property
    def is_click_flash_active(self) -> bool:
        return self._click_flash_timer > 0
