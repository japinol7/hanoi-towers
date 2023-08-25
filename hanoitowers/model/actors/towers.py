"""Module towers."""
__author__ = 'Joan A. Pinol  (japinol)'

from hanoitowers.config.constants import BITMAPS_FOLDER, TOWER_DISTANCE
from hanoitowers.model.actors.actor import ActorItem, ActorType
from hanoitowers.model.actor_type import ActorCategoryType

TOWER_TYPE = {
    1: ActorType.TOWER_1,
    2: ActorType.TOWER_2,
    3: ActorType.TOWER_3,
    }

TOWER_NUM_NAME_MAP = {
    1: 'tower_start',
    2: 'tower_tmp',
    3: 'tower_end',
    }

TOWER_NAME_NUM_MAP = {
    'tower_start': 1,
    'tower_tmp': 2,
    'tower_end': 3,
    }


def create_tower_sprites(x, y, game, n_towers):
    towers = []
    xx, yy = x, y
    for i in range(1, n_towers + 1):
        tower = TowerSprite(xx, yy, game, name=str(i), tower_number=i)
        towers += [tower]
        xx += TOWER_DISTANCE
    return towers


class Tower(ActorItem):
    """Represents a tower.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        self.file_folder = BITMAPS_FOLDER
        self.file_name_key = 'im_tower'
        self.images_sprite_no = 1
        self.category_type = ActorCategoryType.TOWER
        super().__init__(x, y, game, name=name)


class TowerSprite(Tower):
    """Represents a sprite tower."""

    def __init__(self, x, y, game, name=None, tower_number=0, long_name=None):
        self.file_mid_prefix = f"{tower_number:02d}"
        self.type = TOWER_TYPE[tower_number]
        self.number = tower_number
        self.long_name = long_name
        super().__init__(x, y, game, name=name)
