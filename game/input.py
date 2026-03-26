from __future__ import annotations

import pygame


class InputManager:
    def __init__(self) -> None:
        self.mouse_pos = (0, 0)
        self.left_clicked = False

    def begin_frame(self) -> None:
        self.left_clicked = False

    def consume_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.left_clicked = True
            self.mouse_pos = event.pos
