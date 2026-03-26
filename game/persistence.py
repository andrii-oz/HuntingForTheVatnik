from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path

from game.settings import (
    DIFFICULTY_PRESETS,
    MAX_ENEMY_COUNT,
    MAX_REACTION_MS,
    MIN_ENEMY_COUNT,
    MIN_REACTION_MS,
    Difficulty,
    GameSettings,
)


@dataclass
class GameProgress:
    level: int = 1
    hits: int = 0
    misses: int = 0


@dataclass
class SaveSnapshot:
    difficulty: str
    music_enabled: bool
    effects_enabled: bool
    enemy_count: int
    reaction_ms: int
    level: int
    hits: int
    misses: int


class SaveManager:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> SaveSnapshot:
        if not self.path.exists():
            snapshot = self._default_snapshot()
            self.save(snapshot)
            return snapshot

        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            snapshot = self._default_snapshot()
            self.save(snapshot)
            return snapshot

        return self._sanitize(raw)

    def save(self, snapshot: SaveSnapshot) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(asdict(snapshot), ensure_ascii=False, indent=2), encoding="utf-8")

    def save_from_state(self, settings: GameSettings, progress: GameProgress) -> None:
        self.save(
            SaveSnapshot(
                difficulty=settings.difficulty.value,
                music_enabled=bool(settings.music_enabled),
                effects_enabled=bool(settings.effects_enabled),
                enemy_count=self._clamp_enemy_count(settings.enemy_count),
                reaction_ms=self._clamp_reaction_ms(settings.reaction_ms),
                level=max(1, int(progress.level)),
                hits=max(0, int(progress.hits)),
                misses=max(0, int(progress.misses)),
            )
        )

    def save_after_game_end(self, settings: GameSettings) -> None:
        self.save(
            SaveSnapshot(
                difficulty=settings.difficulty.value,
                music_enabled=bool(settings.music_enabled),
                effects_enabled=bool(settings.effects_enabled),
                enemy_count=self._clamp_enemy_count(settings.enemy_count),
                reaction_ms=self._clamp_reaction_ms(settings.reaction_ms),
                level=1,
                hits=0,
                misses=0,
            )
        )

    def _default_snapshot(self) -> SaveSnapshot:
        novice = DIFFICULTY_PRESETS[Difficulty.NOVICE]
        return SaveSnapshot(
            difficulty=Difficulty.NOVICE.value,
            music_enabled=True,
            effects_enabled=True,
            enemy_count=novice.enemy_count,
            reaction_ms=novice.reaction_ms,
            level=1,
            hits=0,
            misses=0,
        )

    def _sanitize(self, raw: dict) -> SaveSnapshot:
        difficulty_raw = str(raw.get("difficulty", Difficulty.NOVICE.value)).lower()
        allowed = {d.value for d in Difficulty}
        difficulty = difficulty_raw if difficulty_raw in allowed else Difficulty.NOVICE.value

        return SaveSnapshot(
            difficulty=difficulty,
            music_enabled=bool(raw.get("music_enabled", True)),
            effects_enabled=bool(raw.get("effects_enabled", True)),
            enemy_count=self._clamp_enemy_count(self._safe_int(raw.get("enemy_count"), DIFFICULTY_PRESETS[Difficulty.NOVICE].enemy_count)),
            reaction_ms=self._clamp_reaction_ms(self._safe_int(raw.get("reaction_ms"), DIFFICULTY_PRESETS[Difficulty.NOVICE].reaction_ms)),
            level=max(1, self._safe_int(raw.get("level"), 1)),
            hits=max(0, self._safe_int(raw.get("hits"), 0)),
            misses=max(0, self._safe_int(raw.get("misses"), 0)),
        )

    def _safe_int(self, raw, fallback: int) -> int:
        try:
            return int(raw)
        except (TypeError, ValueError):
            return fallback

    def _clamp_enemy_count(self, value: int) -> int:
        return max(MIN_ENEMY_COUNT, min(MAX_ENEMY_COUNT, value))

    def _clamp_reaction_ms(self, value: int) -> int:
        return max(MIN_REACTION_MS, min(MAX_REACTION_MS, value))
