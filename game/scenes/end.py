from __future__ import annotations

import pygame

from game.scenes.base import BaseScene


class EndScene(BaseScene):
    scene_id = "end"

    def __init__(self, context, payload: dict | None = None) -> None:
        super().__init__(context)
        payload = payload or {}
        self.won = bool(payload.get("won", False))

        w, h = context.screen_size
        self.lose_background = self.context.assets.load_image(
            key="end_lose_background",
            relative_path="assets/background/background_lose.jpg",
            fallback_color=(40, 40, 40),
        )
        self.lose_background = pygame.transform.smoothscale(self.lose_background, (w, h))

        self.win_background = self.context.assets.load_image(
            key="end_win_background",
            relative_path="assets/background/background_win.jpg",
            fallback_color=(175, 220, 185),
        )
        self.win_background = pygame.transform.smoothscale(self.win_background, (w, h))

    def on_enter(self) -> None:
        if self.won:
            self.context.audio.play_music("sound/musics/end_win.wav", loop=-1, volume=0.6)
        else:
            self.context.audio.play_music("sound/musics/end_lose.wav", loop=-1, volume=0.6)

    def on_exit(self) -> None:
        self.context.audio.stop_music()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.signal.next_scene = "splash"

    def update(self, dt: float) -> None:
        _ = dt

    def render(self, surface: pygame.Surface) -> None:
        if self.won:
            surface.blit(self.win_background, (0, 0))
        else:
            surface.blit(self.lose_background, (0, 0))
