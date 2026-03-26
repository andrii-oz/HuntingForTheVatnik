from __future__ import annotations

import pygame

from game.scenes.base import BaseScene
from game.ui import Button, ButtonStyle


class SplashScene(BaseScene):
    scene_id = "splash"

    def __init__(self, context) -> None:
        super().__init__(context)
        w, h = context.screen_size

        self.menu_font = pygame.font.Font(None, 64)
        self.panel_font = pygame.font.Font(None, 42)
        self.show_settings = False

        self.background = self.context.assets.load_image(
            key="intro_background",
            relative_path="assets/background/intro.jpg",
            fallback_color=(28, 35, 44),
        )
        self.background = pygame.transform.smoothscale(self.background, (w, h))

        blue_style = ButtonStyle(
            base_color=(23, 92, 214),
            hover_color=(34, 115, 243),
            text_color=(245, 249, 255),
            border_color=(10, 58, 150),
        )
        gray_style = ButtonStyle(
            base_color=(214, 223, 233),
            hover_color=(231, 238, 245),
            text_color=(35, 49, 74),
            border_color=(112, 132, 154),
        )

        button_w = 420
        button_h = 98
        gap = 24
        top_y = h // 2 - button_h - (gap // 2)
        self.start_button = Button("ПОЧАЛИ!", pygame.Rect(w // 2 - button_w // 2, top_y, button_w, button_h), blue_style)
        self.settings_button = Button(
            "НАЛАШТУВАННЯ",
            pygame.Rect(w // 2 - button_w // 2, top_y + button_h + gap, button_w, button_h),
            gray_style,
        )

    def on_enter(self) -> None:
        self.context.audio.play_music("sound/musics/intro.wav", loop=-1, volume=0.55)

    def on_exit(self) -> None:
        self.context.audio.stop_music()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.signal.quit_game = True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.start_button.hit_test(pos):
                self.signal.next_scene = "gameplay"
            elif self.settings_button.hit_test(pos):
                self.show_settings = not self.show_settings

    def update(self, dt: float) -> None:
        _ = dt

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.background, (0, 0))

        mouse_pos = self.context.input_manager.mouse_pos
        self.start_button.draw(surface, self.menu_font, self.start_button.hit_test(mouse_pos))
        self.settings_button.draw(surface, self.menu_font, self.settings_button.hit_test(mouse_pos))

        if self.show_settings:
            self._render_settings_stub(surface)

    def _render_settings_stub(self, surface: pygame.Surface) -> None:
        w, h = self.context.screen_size
        panel = pygame.Rect(w // 2 - 280, h // 2 - 180, 560, 160)

        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 110))
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, (248, 251, 255), panel, border_radius=16)
        pygame.draw.rect(surface, (70, 84, 110), panel, width=3, border_radius=16)

        title = self.panel_font.render("Settings menu: next step", True, (28, 39, 58))
        hint = self.panel_font.render("Click НАЛАШТУВАННЯ again to close", True, (50, 62, 84))

        surface.blit(title, title.get_rect(center=(w // 2, h // 2 - 120)))
        surface.blit(hint, hint.get_rect(center=(w // 2, h // 2 - 72)))
