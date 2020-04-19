from enum import Enum


class AnchorType(Enum):
    Grounded = 0   # The bottom row anchors to ground level
    Column = 1  # Anchor takes up the entire column
    Underground = 2  # The top row anchors to ground level


class TextPrefab(object):
    anchor_type = None
    value = []
    links = {}

    @classmethod
    def get_width(cls):
        return len(cls.value[0])

    @classmethod
    def get_height(cls):
        return len(cls.value)


class SmallBuilding(TextPrefab):
    anchor_type = AnchorType.Grounded
    value = [
        "##########",
        "=........=",
        "..........",
        "==========",
    ]
    links = {
        "#": "Rocky Dirt Top",
        "=": "Rocky Dirt Middle",
        ".": "Rocky Dirt Middle Shadow",
    }


class TwoStoryBuilding(TextPrefab):
    anchor_type = AnchorType.Grounded
    value = [
        "##############",
        "#............#",
        "#............#",
        "#------------#",
        "#............#",
        "..............",
        "##############",
    ]
    links = {
        "#": "Rocky Dirt Top",
        "=": "Rocky Dirt Middle",
        ".": "Rocky Dirt Middle Shadow",
        "-": "Red Block Top"
    }


class Ravine(TextPrefab):
    anchor_type = AnchorType.Underground
    value = [
        ".            .",
        ",            ,",
        ",            ,",
        ",            ,",
        ",            ,",
        ",            ,",
        ",            ,",
        ",            ,",
        ",            ,",
        ",            ,",
        ",            ,",
        ",111111111111,",
        ",............,",
    ]
    links = {
        ".": "Rocky Dirt Top",
        ",": "Rocky Dirt Middle",
        "1": "Brown Spikes Bottom",
        " ": "Rocky Dirt Middle Shadow"
    }


class Bridge(TextPrefab):
    anchor_type = AnchorType.Underground
    value = [
        ".------------.",
        ",            ,",
        ",            ,",
        ",            ,",
        ",            ,",
        ",            ,",
        ",            ,",
        ",            ,",
        ",            ,",
        ",            ,",
        ",            ,",
        ",111111111111,",
        ",............,",
    ]
    links = {
        ".": "Rocky Dirt Top",
        ",": "Rocky Dirt Middle",
        "1": "Brown Spikes Bottom",
        "-": "Old Bridge Top",
        " ": "Rocky Dirt Middle Shadow"
    }
