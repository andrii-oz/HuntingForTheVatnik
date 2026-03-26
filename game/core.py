from __future__ import annotations

import tkinter as tk

import pygame

from game.assets import AssetManager
from game.audio import AudioManager
from game.config import DISPLAY, GAME
from game.cursor import CursorManager
from game.input import InputManager
from game.levels import build_level_registry
from game.persistence import GameProgress, SaveManager
from game.scenes.base import SceneContext
from game.scenes.end import EndScene
from game.scenes.gameplay import GameplayScene
from game.scenes.splash import SplashScene
from game.settings import Difficulty, GameSettings


def run_game() -> None:
    pygame.init()
    pygame.display.set_caption(DISPLAY.title)
    screen = pygame.display.set_mode((DISPLAY.width, DISPLAY.height))
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)

    assets = AssetManager(GAME.root_dir)
    audio = AudioManager(GAME.root_dir)
    input_manager = InputManager()
    cursor_manager = CursorManager(assets, input_manager)
    level_registry = build_level_registry()

    save_manager = SaveManager(GAME.root_dir / GAME.save_file)
    snapshot = save_manager.load()

    settings = GameSettings(
        difficulty=Difficulty(snapshot.difficulty),
        music_enabled=snapshot.music_enabled,
        effects_enabled=snapshot.effects_enabled,
        enemy_count=snapshot.enemy_count,
        reaction_ms=snapshot.reaction_ms,
    )
    progress = GameProgress(level=snapshot.level, hits=snapshot.hits, misses=snapshot.misses)

    audio.set_toggles(music_enabled=settings.music_enabled, effects_enabled=settings.effects_enabled)

    context = SceneContext(
        screen_size=(DISPLAY.width, DISPLAY.height),
        assets=assets,
        audio=audio,
        input_manager=input_manager,
        level_registry=level_registry,
        settings=settings,
        progress=progress,
        save_manager=save_manager,
    )

    current_scene = SplashScene(context)
    current_scene.on_enter()
    running = True

    while running:
        dt = clock.tick(DISPLAY.fps) / 1000.0
        input_manager.begin_frame()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if _confirm_save_before_exit():
                    context.save_manager.save_from_state(context.settings, _runtime_progress_snapshot(current_scene, context.progress))
                current_scene.on_exit()
                running = False
                break

            input_manager.consume_event(event)
            current_scene.handle_event(event)

        if not running:
            continue

        cursor_manager.update(dt)
        current_scene.update(dt)
        current_scene.render(screen)
        cursor_manager.render(screen)
        pygame.display.flip()

        signal = current_scene.consume_signal()
        if signal.quit_game:
            current_scene.on_exit()
            running = False
            continue

        if signal.next_scene is not None:
            if signal.next_scene == "end" and signal.payload is not None:
                context.progress.level = max(1, int(signal.payload.get("level", context.progress.level)))
                context.progress.hits = max(0, int(signal.payload.get("hits", context.progress.hits)))
                context.progress.misses = max(0, int(signal.payload.get("misses", context.progress.misses)))

                context.save_manager.save_after_game_end(context.settings)
                context.progress.level = 1
                context.progress.hits = 0
                context.progress.misses = 0

            current_scene.on_exit()
            current_scene = _build_scene(signal.next_scene, context, signal.payload)
            current_scene.on_enter()

    pygame.quit()


def _runtime_progress_snapshot(current_scene, progress: GameProgress) -> GameProgress:
    if isinstance(current_scene, GameplayScene):
        return current_scene.runtime_progress_snapshot()
    return GameProgress(level=progress.level, hits=progress.hits, misses=progress.misses)


def _confirm_save_before_exit() -> bool:
    root = tk.Tk()
    root.title("Збереження")
    root.resizable(False, False)

    answer = {"save": False}

    frame = tk.Frame(root, padx=14, pady=12)
    frame.pack(fill="both", expand=True)

    label = tk.Label(frame, text="Чи бажаєте зберігти гру?")
    label.pack(anchor="w")

    buttons = tk.Frame(frame)
    buttons.pack(anchor="e", pady=(12, 0))

    def on_yes() -> None:
        answer["save"] = True
        root.destroy()

    def on_no() -> None:
        answer["save"] = False
        root.destroy()

    tk.Button(buttons, text="Так", width=10, command=on_yes).pack(side="left", padx=(0, 8))
    tk.Button(buttons, text="Ні", width=10, command=on_no).pack(side="left")

    root.protocol("WM_DELETE_WINDOW", on_no)
    root.update_idletasks()
    x = (root.winfo_screenwidth() - 280) // 2
    y = (root.winfo_screenheight() - 130) // 2
    root.geometry(f"280x130+{x}+{y}")
    root.mainloop()

    return answer["save"]


def _build_scene(scene_id: str, context: SceneContext, payload: dict | None = None):
    if scene_id == SplashScene.scene_id:
        return SplashScene(context)
    if scene_id == GameplayScene.scene_id:
        return GameplayScene(context)
    if scene_id == EndScene.scene_id:
        return EndScene(context, payload=payload)
    raise KeyError(f"Unknown scene id: {scene_id}")
