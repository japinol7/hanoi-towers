"""Module selectors."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from hanoitowers.tools.logger.logger import log
from hanoitowers.config.constants import BM_SELECTORS_FOLDER
from hanoitowers.model.actor_type import ActorCategoryType, ActorType
from hanoitowers.model.actors.actor import ActorItem
from hanoitowers.tools.utils.color import Color
from hanoitowers.model.special_effects.light import Light, LightGrid
from hanoitowers.config.settings import Settings


class Selector(ActorItem):
    """Represents a selector.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        self.file_folder = BM_SELECTORS_FOLDER
        self.file_name_key = 'im_selectors'
        self.images_sprite_no = 1
        self.category_type = ActorCategoryType.SELECTOR
        self.stats = {}
        self.light_grid = None
        self.light_grid_surf_size = (34, 34)
        self.light_grid_surf_size_half = (self.light_grid_surf_size[0] // 2, self.light_grid_surf_size[1] // 2)
        self.light_color = Color.GREEN

        super().__init__(x, y, game, name=name)

        self._create_light()

    def update_sprite_image(self):
        pass

    def _create_light(self):
        self.light_grid = LightGrid(self.light_grid_surf_size)
        self.light_grid.add_light(
            Light((0, 0), radius=18, color=self.light_color, alpha=255),
            )

    def update_after_inc_index_hook(self):
        mx, my = self.game.mouse_pos
        self.rect.centerx, self.rect.centery = mx, my

        if Settings.has_selector_no_light:
            return

        # Create a surface with only the part of the screen that is needed for the light grid render
        sub_screen_rect = pg.Rect(
            mx - self.light_grid_surf_size_half[0],
            my - self.light_grid_surf_size_half[1],
            self.light_grid_surf_size[0],
            self.light_grid_surf_size[1])
        grid_surface = pg.Surface(sub_screen_rect.size)
        grid_surface.blit(self.game.screen, (0, 0), sub_screen_rect)

        # Render all the lights of the light grid
        for light in self.light_grid.lights.values():
            light.set_color(self.light_color, override_alpha=True)
            light.position = (self.light_grid_surf_size_half[0],
                              self.light_grid_surf_size_half[1])
        self.light_grid.render(grid_surface)
        self.game.screen.blit(grid_surface, sub_screen_rect)

    def update_when_hit(self):
        """Cannot be hit."""
        pass

    def get_pointed_disc_sprite(self):
        disc_hit_list = pg.sprite.spritecollide(self, self.game.disc_sprites, False)
        if disc_hit_list:
            for sprite_hit in disc_hit_list:
                if self.game.selected_disc and self.game.selected_disc.name == sprite_hit.name:
                    continue
                return sprite_hit
        return None

    def get_pointed_tower_sprite(self):
        tower_hit_list = pg.sprite.spritecollide(self, self.game.tower_sprites, False)
        if tower_hit_list:
            for sprite_hit in tower_hit_list:
                return sprite_hit
        return None

    def get_pointed_sprite(self):
        sprite = self.get_pointed_disc_sprite()

        if not sprite:
            sprite = self.get_pointed_tower_sprite()

        if sprite:
            log.debug(f"Mouse sprites: {sprite.id} {sprite.category_type} in pos: ({sprite.rect.x}, {sprite.rect.y})")

        return sprite


class SelectorA(Selector):
    """Represents a selector of type A."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.SELECTOR_A
        super().__init__(x, y, game, name=name)
