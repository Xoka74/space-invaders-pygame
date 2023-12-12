from dataclasses import dataclass


@dataclass
class Settings:
    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 600
    GAME_VOLUME: float = 0.15
