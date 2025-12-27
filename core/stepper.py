from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class Stepper(Generic[T]):
    steps: Sequence[T]
    index: int = 0

    def current(self) -> T:
        return self.steps[self.index]

    def can_prev(self) -> bool:
        return self.index > 0

    def can_next(self) -> bool:
        return self.index < len(self.steps) - 1

    def prev(self) -> None:
        if self.can_prev():
            self.index -= 1

    def next(self) -> None:
        if self.can_next():
            self.index += 1

    def reset(self) -> None:
        self.index = 0
