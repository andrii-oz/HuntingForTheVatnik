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


DIFFICULTY_PRESETS: dict[Difficulty, DifficultyPreset] = {
    Difficulty.NOVICE: DifficultyPreset(enemy_count=20, reaction_ms=1000),
    Difficulty.AMATEUR: DifficultyPreset(enemy_count=45, reaction_ms=600),
    Difficulty.PROFESSIONAL: DifficultyPreset(enemy_count=75, reaction_ms=300),
}


MIN_ENEMY_COUNT = 9
MAX_ENEMY_COUNT = 99
MIN_REACTION_MS = 100
MAX_REACTION_MS = 2000


@dataclass
class GameSettings:
    difficulty: Difficulty = Difficulty.NOVICE
    music_enabled: bool = True
    effects_enabled: bool = True
    enemy_count: int = DIFFICULTY_PRESETS[Difficulty.NOVICE].enemy_count
    reaction_ms: int = DIFFICULTY_PRESETS[Difficulty.NOVICE].reaction_ms


def open_settings_window(current: GameSettings) -> GameSettings | None:
    result: GameSettings | None = None

    root = tk.Tk()
    root.title("Налаштування")
    root.resizable(False, False)

    difficulty_var = tk.StringVar(value=current.difficulty.value)
    music_var = tk.BooleanVar(value=current.music_enabled)
    effects_var = tk.BooleanVar(value=current.effects_enabled)
    enemy_count_var = tk.StringVar(value=str(_clamp_enemy_count(current.enemy_count)))
    reaction_ms_var = tk.IntVar(value=_clamp_reaction_ms(current.reaction_ms))

    container = ttk.Frame(root, padding=12)
    container.grid(row=0, column=0, sticky="nsew")

    difficulty_group = ttk.LabelFrame(container, text="Складність гри", padding=10)
    difficulty_group.grid(row=0, column=0, sticky="ew")

    def on_difficulty_change() -> None:
        selected = Difficulty(difficulty_var.get())
        preset = DIFFICULTY_PRESETS[selected]
        enemy_count_var.set(str(preset.enemy_count))
        reaction_ms_var.set(preset.reaction_ms)

    row = 0
    for difficulty in Difficulty:
        ttk.Radiobutton(
            difficulty_group,
            text=DIFFICULTY_LABELS[difficulty],
            value=difficulty.value,
            variable=difficulty_var,
            command=on_difficulty_change,
        ).grid(row=row, column=0, sticky="w", pady=2)
        row += 1

    advanced_group = ttk.LabelFrame(container, text="Розширені налаштування", padding=10)
    advanced_group.grid(row=1, column=0, sticky="ew", pady=(10, 0))

    ttk.Button(
        advanced_group,
        text="Відкрити розширені налаштування",
        command=lambda: _open_advanced_window(root, enemy_count_var, reaction_ms_var),
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
            enemy_count=_clamp_enemy_count(_safe_int(enemy_count_var.get(), current.enemy_count)),
            reaction_ms=_clamp_reaction_ms(reaction_ms_var.get()),
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


def _open_advanced_window(parent: tk.Tk, enemy_count_var: tk.StringVar, reaction_ms_var: tk.IntVar) -> None:
    advanced = tk.Toplevel(parent)
    advanced.title("Розширені налаштування")
    advanced.resizable(False, False)

    frame = ttk.Frame(advanced, padding=12)
    frame.grid(row=0, column=0, sticky="nsew")

    gameplay_group = ttk.LabelFrame(frame, text="Геймплей", padding=10)
    gameplay_group.grid(row=0, column=0, sticky="ew")

    ttk.Label(gameplay_group, text="Кількість ватників").grid(row=0, column=0, columnspan=3, sticky="w")

    def normalize_enemy_count() -> None:
        value = _clamp_enemy_count(_safe_int(enemy_count_var.get(), MIN_ENEMY_COUNT))
        enemy_count_var.set(str(value))

    def decrease_enemy() -> None:
        value = _clamp_enemy_count(_safe_int(enemy_count_var.get(), MIN_ENEMY_COUNT) - 1)
        enemy_count_var.set(str(value))

    def increase_enemy() -> None:
        value = _clamp_enemy_count(_safe_int(enemy_count_var.get(), MIN_ENEMY_COUNT) + 1)
        enemy_count_var.set(str(value))

    ttk.Button(gameplay_group, text="-", width=4, command=decrease_enemy).grid(
        row=1,
        column=0,
        sticky="ew",
        padx=(0, 0),
        pady=(4, 0),
        ipady=6,
    )

    enemy_entry = ttk.Entry(gameplay_group, textvariable=enemy_count_var, width=4, justify="center")
    enemy_entry.grid(row=1, column=1, sticky="ew", padx=(0, 0), pady=(4, 0), ipady=6)

    ttk.Button(gameplay_group, text="+", width=4, command=increase_enemy).grid(
        row=1,
        column=2,
        sticky="ew",
        padx=(0, 0),
        pady=(4, 0),
        ipady=6,
    )

    enemy_entry.bind("<FocusOut>", lambda _event: normalize_enemy_count())
    enemy_entry.bind("<Return>", lambda _event: normalize_enemy_count())
    enemy_entry.bind("<KeyRelease>", lambda _event: _sanitize_enemy_entry(enemy_count_var))

    ttk.Label(
        gameplay_group,
        text=f"Допустимий діапазон: {MIN_ENEMY_COUNT} - {MAX_ENEMY_COUNT}",
    ).grid(row=2, column=0, columnspan=3, sticky="w", pady=(6, 8))

    ttk.Label(gameplay_group, text="Швидкість реакції (мс)").grid(row=3, column=0, columnspan=3, sticky="w")

    value_label_var = tk.StringVar(value=f"{_clamp_reaction_ms(reaction_ms_var.get())} мс")

    def on_scale_change(raw_value: str) -> None:
        value = _clamp_reaction_ms(int(float(raw_value)))
        reaction_ms_var.set(value)
        value_label_var.set(f"{value} мс")

    reaction_scale = ttk.Scale(
        gameplay_group,
        from_=MIN_REACTION_MS,
        to=MAX_REACTION_MS,
        orient="horizontal",
        command=on_scale_change,
    )
    reaction_scale.set(_clamp_reaction_ms(reaction_ms_var.get()))
    reaction_scale.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(4, 0))

    ttk.Label(gameplay_group, textvariable=value_label_var).grid(row=5, column=0, columnspan=3, sticky="w", pady=(4, 0))

    ttk.Label(
        gameplay_group,
        text=f"Діапазон: {MIN_REACTION_MS} - {MAX_REACTION_MS}",
    ).grid(row=6, column=0, columnspan=3, sticky="w", pady=(2, 0))

    buttons = ttk.Frame(frame)
    buttons.grid(row=1, column=0, sticky="e", pady=(10, 0))
    ttk.Button(buttons, text="Закрити", command=lambda: _close_advanced(advanced, enemy_count_var, reaction_ms_var)).grid(
        row=0,
        column=0,
    )

    _center_window(advanced, width=470, height=320)
    advanced.transient(parent)
    advanced.grab_set()
    advanced.focus_set()


def _sanitize_enemy_entry(enemy_count_var: tk.StringVar) -> None:
    raw = enemy_count_var.get()
    digits_only = "".join(ch for ch in raw if ch.isdigit())
    if digits_only != raw:
        enemy_count_var.set(digits_only)


def _close_advanced(window: tk.Toplevel, enemy_count_var: tk.StringVar, reaction_ms_var: tk.IntVar) -> None:
    enemy_count_var.set(str(_clamp_enemy_count(_safe_int(enemy_count_var.get(), MIN_ENEMY_COUNT))))
    reaction_ms_var.set(_clamp_reaction_ms(reaction_ms_var.get()))
    window.destroy()


def _safe_int(raw: str, fallback: int) -> int:
    try:
        return int(raw)
    except (TypeError, ValueError):
        return fallback


def _clamp_enemy_count(value: int) -> int:
    return max(MIN_ENEMY_COUNT, min(MAX_ENEMY_COUNT, value))


def _clamp_reaction_ms(value: int) -> int:
    return max(MIN_REACTION_MS, min(MAX_REACTION_MS, int(value)))


def _center_window(window: tk.Misc, width: int, height: int) -> None:
    window.update_idletasks()
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
