from dataclasses import dataclass


@dataclass
class SpriteInfo:
    spritesheet_name: str
    sprite_name: str
    row: int
    column: int
    flipped: bool = False
