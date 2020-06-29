from pyg2d.core.spriteinfo import SpriteInfo
from pyg2d.gamedata import Factory
from pyg2d.gamedata.recipes.collectibles.base import Collectible


@Factory.register
class SilverCoin(Collectible):
    name = "Silver Coin"
    animations = {'idle': [SpriteInfo('packed', 'silver_coin', 12, 15)]}
