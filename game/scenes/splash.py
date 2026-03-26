from __future__ import annotations

import pygame

from game.scenes.base import BaseScene
from game.settings import GameSettings, open_settings_window


class SplashScene(BaseScene):
    scene_id = "splash"

    def __init__(self, context) -> None:
        super().__init__(context)
        w, h = context.screen_size

        self.background = self.context.assets.load_image(
            key="intro_background",
            relative_path="assets/background/intro.jpg",
            fallback_color=(28, 35, 44),
        )
        self.background = pygame.transform.smoothscale(self.background, (w, h))

        start_img = self.context.assets.load_image(
            key="start_button_img",
            relative_path="assets/ui/start.png",
            fallback_color=(30, 90, 210),
        )
        settings_img = self.context.assets.load_image(
            key="settings_button_img",
            relative_path="assets/ui/setting.png",
            fallback_color=(210, 220, 230),
        )

        # Keep consistent visual size on different source assets.
        self.button_w = 420
        self.button_h = 98
        self.start_button_image = pygame.transform.smoothscale(start_img, (self.button_w, self.button_h)).convert_alpha()
        self.settings_button_image = pygame.transform.smoothscale(settings_img, (self.button_w, self.button_h)).convert_alpha()

        gap = 24
        top_y = h // 2 - self.button_h - (gap // 2)
        self.start_button_rect = pygame.Rect(w // 2 - self.button_w // 2, top_y, self.button_w, self.button_h)
        self.settings_button_rect = pygame.Rect(w // 2 - self.button_w // 2, top_y + self.button_h + gap, self.button_w, self.button_h)

    def on_enter(self) -> None:
        self.context.audio.play_music("sound/musics/intro.wav", loop=-1, volume=0.55)

    def on_exit(self) -> None:
        self.context.audio.stop_music()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.signal.quit_game = True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.start_button_rect.collidepoint(pos):
                self.signal.next_scene = "gameplay"
            elif self.settings_button_rect.collidepoint(pos):
                self._open_settings_dialog()

    def update(self, dt: float) -> None:
        _ = dt

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.background, (0, 0))

        mouse_pos = self.context.input_manager.mouse_pos
        self._draw_image_button(
            surface,
            self.start_button_image,
            self.start_button_rect,
            hovered=self.start_button_rect.collidepoint(mouse_pos),
        )
        self._draw_image_button(
            surface,
            self.settings_button_image,
            self.settings_button_rect,
            hovered=self.settings_button_rect.collidepoint(mouse_pos),
        )

    def _draw_image_button(
        self,
        surface: pygame.Surface,
        image: pygame.Surface,
        rect: pygame.Rect,
        hovered: bool,
    ) -> None:
        surface.blit(image, rect.topleft)
        if hovered:
            hover_overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            hover_overlay.fill((255, 255, 255, 28))
            surface.blit(hover_overlay, rect.topleft)

    def _open_settings_dialog(self) -> None:
        def persist_settings(settings: GameSettings) -> None:
            self._apply_settings(settings)
            self.context.save_manager.save_from_state(self.context.settings, self.context.progress)

        updated = open_settings_window(
            self.context.settings,
            on_save_to_file=persist_settings,
        )
        if updated is None:
            return

        self._apply_settings(updated)

    def _apply_settings(self, updated: GameSettings) -> None:
        self.context.settings.difficulty = updated.difficulty
        self.context.settings.music_enabled = updated.music_enabled
        self.context.settings.effects_enabled = updated.effects_enabled
        self.context.settings.enemy_count = updated.enemy_count
        self.context.settings.reaction_ms = updated.reaction_ms

        self.context.audio.set_toggles(
            music_enabled=self.context.settings.music_enabled,
            effects_enabled=self.context.settings.effects_enabled,
        )

        if self.context.settings.music_enabled:
            self.context.audio.play_music("sound/musics/intro.wav", loop=-1, volume=0.55)
