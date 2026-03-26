from game.levels.level_one import LevelOne
from game.levels.level_registry import LevelRegistry


def build_level_registry() -> LevelRegistry:
    registry = LevelRegistry()
    registry.register(LevelOne.level_id, LevelOne)
    return registry
