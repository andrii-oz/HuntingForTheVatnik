from __future__ import annotations

import pygame

from game.scenes.base import BaseScene
from game.settings import open_settings_window
from game.ui import Button, ButtonStyle


class SplashScene(BaseScene):
    scene_id = "splash"

    def __init__(self, context) -> None:
        super().__init__(context)
        w, h = context.screen_size

        self.menu_font = pygame.font.Font(None, 64)

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
                self._open_settings_dialog()

    def update(self, dt: float) -> None:
        _ = dt

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.background, (0, 0))

        mouse_pos = self.context.input_manager.mouse_pos
        self.start_button.draw(surface, self.menu_font, self.start_button.hit_test(mouse_pos))
        self.settings_button.draw(surface, self.menu_font, self.settings_button.hit_test(mouse_pos))

    def _open_settings_dialog(self) -> None:
        updated = open_settings_window(self.context.settings)
        if updated is None:
            return

        self.context.settings.difficulty = updated.difficulty
        self.context.settings.music_enabled = updated.music_enabled
        self.context.settings.effects_enabled = updated.effects_enabled

        self.context.audio.set_toggles(
            music_enabled=self.context.settings.music_enabled,
            effects_enabled=self.context.settings.effects_enabled,
        )

        if self.context.settings.music_enabled:
            self.context.audio.play_music("sound/musics/intro.wav", loop=-1, volume=0.55)
