"""Module disc_sprite."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from hanoitowers.config.constants import (
    BITMAPS_FOLDER,
    DISC_WIDTH_BASE,
    DISC_HEIGHT,
    DISC_WIDTH_ADDED_PGE,
    TOWER_DISTANCE,
    TOWER_1_POS_X_CENTER,
    DISC_POS_Y,
)
from hanoitowers.config.settings import Settings
from hanoitowers.model.actors.actor import Actor, ActorItem, ActorType
from hanoitowers.model.actor_type import ActorCategoryType

DISC_TYPE = {
    1: ActorType.DISC_1,
    2: ActorType.DISC_2,
    3: ActorType.DISC_3,
    4: ActorType.DISC_4,
    5: ActorType.DISC_5,
    6: ActorType.DISC_6,
    7: ActorType.DISC_7,
    }


def create_disc_sprites(x, y, game, n_discs):
    discs = []
    xx, yy = x, y
    for i in range(n_discs, 0, -1):
        discs += [DiscSprite(xx, yy, game, name=str(i), disc_number=i, tower=1)]
        yy -= DISC_HEIGHT
        game.disc_locations[i] = 1, Settings.hanoy_discs - i + 1
    return discs


class DiscBase(ActorItem):
    """Represents a Sprite Disc.
    It is not intended to be instantiated.
    """

    def __init__(self, x, y, game, name=None, disc_number=0, tower=0):
        self.file_folder = BITMAPS_FOLDER
        self.file_name_key = 'im_disc'
        self.disc_number = disc_number
        self.images_sprite_no = 1
        self.width = round(DISC_WIDTH_BASE + (DISC_WIDTH_BASE * DISC_WIDTH_ADDED_PGE * (self.disc_number - 1)), 2)
        x = x - self.width // 2
        self.category_type = ActorCategoryType.DISC
        self.tower = tower
        super().__init__(x, y, game, name=name)

    def _load_sprites(self):
        if Actor.sprite_images.get(self.type.name):
            self.image = Actor.sprite_images[self.type.name][0]
            return
        self.image = pg.image.load(self.file_name_im_get(
            self.file_folder, self.file_name_key,
            self.file_mid_prefix, suffix_index=1
            )).convert()
        self.image = pg.transform.smoothscale(self.image, (self.width, DISC_HEIGHT))
        Actor.sprite_images[self.type.name] = (self.image, [self.image])

    def update(self):
        self.update_sprite_image()


class DiscSprite(DiscBase):
    """Represents a sprite disc."""
    discs_map = {}

    def __init__(self, x, y, game, name=None, disc_number=0, tower=0):
        self.file_mid_prefix = f"{disc_number:02d}"
        self.type = DISC_TYPE[disc_number]
        super().__init__(x, y, game, name=name, disc_number=disc_number, tower=tower)

        DiscSprite.discs_map[disc_number] = self

    def update(self):
        if self.game.selected_disc and self.game.selected_disc.name == self.name:
            self.rect.x = self.game.mouse_pos[0] - self.rect.width // 2
            self.rect.y = self.game.mouse_pos[1] - self.rect.height // 2
        elif self.game.disc_locations[self.disc_number]:
            x_delta = (self.game.disc_locations[self.disc_number][0] - 1) * TOWER_DISTANCE
            self.rect.x = TOWER_1_POS_X_CENTER + x_delta - self.rect.width // 2
            self.rect.y = DISC_POS_Y - self.rect.height * (self.game.disc_locations[self.disc_number][1] - 1)

        super().update()
