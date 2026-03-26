from __future__ import annotations

import pygame

from game.assets import AssetManager
from game.audio import AudioManager
from game.config import DISPLAY, GAME
from game.input import InputManager
from game.levels import build_level_registry
from game.scenes.base import SceneContext
from game.scenes.end import EndScene
from game.scenes.gameplay import GameplayScene
from game.scenes.splash import SplashScene


def run_game() -> None:
    pygame.init()
    pygame.display.set_caption(DISPLAY.title)
    screen = pygame.display.set_mode((DISPLAY.width, DISPLAY.height))
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)

    assets = AssetManager(GAME.root_dir)
    audio = AudioManager(GAME.root_dir)
    input_manager = InputManager()
    level_registry = build_level_registry()

    context = SceneContext(
        screen_size=(DISPLAY.width, DISPLAY.height),
        assets=assets,
        audio=audio,
        input_manager=input_manager,
        level_registry=level_registry,
    )

    current_scene = SplashScene(context)
    current_scene.on_enter()
    running = True

    while running:
        dt = clock.tick(DISPLAY.fps) / 1000.0
        input_manager.begin_frame()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            input_manager.consume_event(event)
            current_scene.handle_event(event)

        current_scene.update(dt)
        current_scene.render(screen)
        pygame.display.flip()

        signal = current_scene.consume_signal()
        if signal.quit_game:
            current_scene.on_exit()
            running = False
            continue

        if signal.next_scene is not None:
            current_scene.on_exit()
            current_scene = _build_scene(signal.next_scene, context, signal.payload)
            current_scene.on_enter()

    pygame.quit()


def _build_scene(scene_id: str, context: SceneContext, payload: dict | None = None):
    if scene_id == SplashScene.scene_id:
        return SplashScene(context)
    if scene_id == GameplayScene.scene_id:
        return GameplayScene(context)
    if scene_id == EndScene.scene_id:
        return EndScene(context, payload=payload)
    raise KeyError(f"Unknown scene id: {scene_id}")
