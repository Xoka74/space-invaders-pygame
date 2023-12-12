from dataclasses import dataclass


@dataclass
class HighScore:
    name: str
    value: int


@dataclass
class LevelHighScores:
    name: str
    high_scores: list[HighScore]
