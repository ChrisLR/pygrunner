from enum import Enum


class AnchorType(Enum):
    Grounded = 0   # The bottom row anchors to ground level
    Column = 1  # Anchor takes up the entire column
    Underground = 2  # The top row anchors to ground level


class TmxPrefab(object):
    def __init__(self, name, anchor_type):
        self.name = name
        self.anchor_type = anchor_type
        self.level = None

    def loading_set(self, level):
        self.level = level
        return self


prefabs = [
    TmxPrefab("winter_brokenbridge_underground", anchor_type=AnchorType.Underground),
    TmxPrefab("winter_house_grounded", anchor_type=AnchorType.Grounded),
    TmxPrefab("winter_ravine_underground", anchor_type=AnchorType.Underground),
    TmxPrefab("winter_stretch_grounded", anchor_type=AnchorType.Grounded),
]
