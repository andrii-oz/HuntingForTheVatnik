from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass(frozen=True)
class ButtonStyle:
    base_color: tuple[int, int, int]
    hover_color: tuple[int, int, int]
    text_color: tuple[int, int, int]
    border_color: tuple[int, int, int]


@dataclass
class Button:
    text: str
    rect: pygame.Rect
    style: ButtonStyle

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, hovered: bool = False) -> None:
        fill = self.style.hover_color if hovered else self.style.base_color

        pygame.draw.rect(surface, fill, self.rect, border_radius=14)
        pygame.draw.rect(surface, self.style.border_color, self.rect, width=3, border_radius=14)

        gloss_rect = pygame.Rect(self.rect.left + 4, self.rect.top + 4, self.rect.width - 8, self.rect.height // 3)
        pygame.draw.rect(surface, (255, 255, 255, 40), gloss_rect, border_radius=12)

        label = font.render(self.text, True, self.style.text_color)
        shadow = font.render(self.text, True, (0, 0, 0))
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(shadow, (label_rect.x + 2, label_rect.y + 2))
        surface.blit(label, label_rect)

    def hit_test(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)
