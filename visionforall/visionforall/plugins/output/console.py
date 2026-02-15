"""Console output renderer."""

from __future__ import annotations


class ConsoleOutput:
    """Render assistant responses in terminal."""

    def render(self, text: str) -> None:
        print(text)
