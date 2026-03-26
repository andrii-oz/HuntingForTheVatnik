from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DisplayConfig:
    width: int = 1280
    height: int = 720
    title: str = "Hunting For The Vatnik"
    fps: int = 60


@dataclass(frozen=True)
class GameConfig:
    root_dir: Path = Path(__file__).resolve().parent.parent
    assets_dir: str = "assets"
    sound_dir: str = "sound"
    default_level_id: str = "level_one"
    reaction_time_sec: float = 1.8


DISPLAY = DisplayConfig()
GAME = GameConfig()
