from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass
class Button:
    text: str
    rect: pygame.Rect

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, hovered: bool = False) -> None:
        bg = (35, 35, 35) if not hovered else (62, 62, 62)
        fg = (245, 245, 245)
        pygame.draw.rect(surface, bg, self.rect, border_radius=10)
        label = font.render(self.text, True, fg)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)

    def hit_test(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)
