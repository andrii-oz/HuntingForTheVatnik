from __future__ import annotations

from collections.abc import Callable

from game.levels.base import BaseLevel


class LevelRegistry:
    def __init__(self) -> None:
        self._registry: dict[str, Callable[..., BaseLevel]] = {}

    def register(self, level_id: str, factory: Callable[..., BaseLevel]) -> None:
        self._registry[level_id] = factory

    def create(self, level_id: str, **kwargs) -> BaseLevel:
        if level_id not in self._registry:
            known = ", ".join(self._registry.keys())
            raise KeyError(f"Unknown level '{level_id}'. Known levels: {known}")
        return self._registry[level_id](**kwargs)

    def list_levels(self) -> list[str]:
        return list(self._registry.keys())
