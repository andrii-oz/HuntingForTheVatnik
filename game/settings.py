from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import tkinter as tk
from tkinter import ttk


class Difficulty(str, Enum):
    NOVICE = "novice"
    AMATEUR = "amateur"
    PROFESSIONAL = "professional"


DIFFICULTY_LABELS: dict[Difficulty, str] = {
    Difficulty.NOVICE: "Новачок",
    Difficulty.AMATEUR: "Любитель",
    Difficulty.PROFESSIONAL: "Професіонал",
}


@dataclass(frozen=True)
class DifficultyPreset:
    enemy_count: int
    reaction_ms: int

    @property
    def reaction_seconds(self) -> float:
        return self.reaction_ms / 1000.0


DIFFICULTY_PRESETS: dict[Difficulty, DifficultyPreset] = {
    Difficulty.NOVICE: DifficultyPreset(enemy_count=20, reaction_ms=1000),
    Difficulty.AMATEUR: DifficultyPreset(enemy_count=45, reaction_ms=600),
    Difficulty.PROFESSIONAL: DifficultyPreset(enemy_count=75, reaction_ms=300),
}


@dataclass
class GameSettings:
    difficulty: Difficulty = Difficulty.NOVICE
    music_enabled: bool = True
    effects_enabled: bool = True

    @property
    def preset(self) -> DifficultyPreset:
        return DIFFICULTY_PRESETS[self.difficulty]


def open_settings_window(current: GameSettings) -> GameSettings | None:
    result: GameSettings | None = None

    root = tk.Tk()
    root.title("Налаштування")
    root.resizable(False, False)

    difficulty_var = tk.StringVar(value=current.difficulty.value)
    music_var = tk.BooleanVar(value=current.music_enabled)
    effects_var = tk.BooleanVar(value=current.effects_enabled)

    container = ttk.Frame(root, padding=12)
    container.grid(row=0, column=0, sticky="nsew")

    difficulty_group = ttk.LabelFrame(container, text="Складність гри", padding=10)
    difficulty_group.grid(row=0, column=0, sticky="ew")

    row = 0
    for difficulty in Difficulty:
        ttk.Radiobutton(
            difficulty_group,
            text=DIFFICULTY_LABELS[difficulty],
            value=difficulty.value,
            variable=difficulty_var,
        ).grid(row=row, column=0, sticky="w", pady=2)
        row += 1

    advanced_group = ttk.LabelFrame(container, text="Розширені налаштування", padding=10)
    advanced_group.grid(row=1, column=0, sticky="ew", pady=(10, 0))

    ttk.Button(
        advanced_group,
        text="Відкрити розширені налаштування",
        command=lambda: _open_advanced_window(root),
    ).grid(row=0, column=0, sticky="w")

    audio_group = ttk.LabelFrame(container, text="Звук", padding=10)
    audio_group.grid(row=2, column=0, sticky="ew", pady=(10, 0))

    ttk.Checkbutton(audio_group, text="Музика", variable=music_var).grid(row=0, column=0, sticky="w", pady=2)
    ttk.Checkbutton(audio_group, text="Ефекти", variable=effects_var).grid(row=1, column=0, sticky="w", pady=2)

    actions = ttk.Frame(container)
    actions.grid(row=3, column=0, sticky="e", pady=(12, 0))

    def on_apply() -> None:
        nonlocal result
        result = GameSettings(
            difficulty=Difficulty(difficulty_var.get()),
            music_enabled=bool(music_var.get()),
            effects_enabled=bool(effects_var.get()),
        )
        root.destroy()

    def on_cancel() -> None:
        root.destroy()

    ttk.Button(actions, text="Застосувати", command=on_apply).grid(row=0, column=0, padx=(0, 8))
    ttk.Button(actions, text="Скасувати", command=on_cancel).grid(row=0, column=1)

    root.protocol("WM_DELETE_WINDOW", on_cancel)
    _center_window(root, width=430, height=390)
    root.mainloop()

    return result


def _open_advanced_window(parent: tk.Tk) -> None:
    advanced = tk.Toplevel(parent)
    advanced.title("Розширені налаштування")
    advanced.resizable(False, False)

    frame = ttk.Frame(advanced, padding=12)
    frame.grid(row=0, column=0, sticky="nsew")

    ttk.Label(
        frame,
        text="Тут будуть детальні параметри керування і геймплею.\n"
        "Підключимо їх на наступному кроці.",
        justify="left",
    ).grid(row=0, column=0, sticky="w")

    ttk.Button(frame, text="Закрити", command=advanced.destroy).grid(row=1, column=0, sticky="e", pady=(12, 0))

    _center_window(advanced, width=430, height=160)
    advanced.transient(parent)
    advanced.grab_set()


def _center_window(window: tk.Misc, width: int, height: int) -> None:
    window.update_idletasks()
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
