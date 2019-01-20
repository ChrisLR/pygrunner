from pygrunner.core.spriteinfo import SpriteInfo
from pygrunner.gamedata.factory import Factory
from pygrunner.gamedata.recipes.collectibles.base import Collectible


@Factory.register
class SilverCoin(Collectible):
    name = "Silver Coin"
    animations = {'idle': [SpriteInfo('packed', 'silver_coin', 12, 15)]}
