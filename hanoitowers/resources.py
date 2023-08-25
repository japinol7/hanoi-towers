"""Module resources."""
__author__ = 'Joan A. Pinol  (japinol)'

import os

import pygame as pg

from hanoitowers.tools.utils.color import Color
from hanoitowers.config import constants as consts
from hanoitowers.tools.utils import utils_graphics as libg_jp
from hanoitowers.config.settings import Settings


def file_name_get(name, subname='', folder=consts.BITMAPS_FOLDER):
    return os.path.join(
        folder,
        f"{consts.FILE_NAMES['%s%s' % (name, subname)][0]}"
        f".{consts.FILE_NAMES['%s%s' % (name, subname)][1]}")


class Resource:
    """Some resources used in the game that do not have their own class."""
    action_sound_move = None
    images = {}
    txt_surfaces = {'game_paused': None, 'player_wins': None,
                    'game_turn_time_out': None, 'game_turn_time_out_2': None,
                    'press_intro_to_continue_center': None,
                    'press_intro_to_continue': None, 'press_intro_to_continue_2': None,
                    'game_start': None, 'game_start_2': None,
                    }

    @classmethod
    def load_sound_resources(cls):
        cls.sound_move = pg.mixer.Sound(file_name_get(name='snd_move', folder=consts.SOUNDS_FOLDER))
        cls.sound_move_failed = pg.mixer.Sound(file_name_get(name='snd_move_failed', folder=consts.SOUNDS_FOLDER))

    @classmethod
    def render_text_frequently_used(cls, game):
        libg_jp.render_text('– PAUSED –',*Settings.board_base_center,
                            cls.txt_surfaces, 'game_paused', color=Color.CYAN,
                            size=int(148*Settings.font_pos_factor), align="center")

        libg_jp.render_text('– Press Escape to Exit this Game  –', Settings.screen_width // 2,
                            (Settings.screen_height // 2.6) - int(6 * Settings.font_pos_factor_t2),
                            cls.txt_surfaces, 'exit_current_game_confirm', color=Color.CYAN,
                            size=int(78*Settings.font_pos_factor_t2), align="center")

        libg_jp.render_text('– Press Enter to Continue –', Settings.screen_width // 2,
                            (Settings.screen_height // 1.764) + int(82 * Settings.font_pos_factor_t2),
                            cls.txt_surfaces, 'press_intro_to_continue_center', color=Color.CYAN,
                            size=int(82*Settings.font_pos_factor_t2), align="center")

        libg_jp.render_text("TIME OUT", Settings.screen_width // 1.99,
                            Settings.screen_height // 2.484,
                            cls.txt_surfaces, 'game_turn_time_out', color=Color.BLUE,
                            size=int(120*Settings.font_pos_factor), align="center")
        libg_jp.render_text("TIME OUT", Settings.screen_width // 2,
                            Settings.screen_height // 2.5,
                            cls.txt_surfaces, 'game_turn_time_out_2', color=Color.CYAN,
                            size=int(120*Settings.font_pos_factor), align="center")

        libg_jp.render_text('Press Enter to Continue', Settings.board_base_center[0],
                            (Settings.screen_height // 1.88) + int(82 * Settings.font_pos_factor_t2),
                            cls.txt_surfaces, 'press_intro_to_continue', color=Color.BLUE,
                            size=int(82*Settings.font_pos_factor_t2), align="center")
        libg_jp.render_text('Press Enter to Continue', Settings.board_base_center[0] / 1.002,
                            (Settings.screen_height // 1.896) + int(82 * Settings.font_pos_factor_t2),
                            cls.txt_surfaces, 'press_intro_to_continue_2', color=Color.CYAN,
                            size=int(82*Settings.font_pos_factor_t2), align="center")

    @classmethod
    def load_and_render_background_images(cls):
        """Load and render background images and effects."""
        img = pg.Surface((Settings.screen_width, Settings.screen_height)).convert_alpha()
        img.fill((0, 0, 0, 55))
        cls.images['dim_screen'] = img

        img = pg.image.load(file_name_get(folder=consts.BM_BACKGROUNDS_FOLDER,
                                          name='im_background', subname='')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width, Settings.screen_height))
        cls.images['background'] = img

        img = pg.image.load(file_name_get(folder=consts.BM_BACKGROUNDS_FOLDER,
                                          name='bg_blue_t1_big_logo', subname='')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width, Settings.screen_height))
        cls.images['bg_blue_t1'] = img

        img = pg.image.load(file_name_get(folder=consts.BM_BACKGROUNDS_FOLDER,
                                          name='im_screen_help', subname='')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width, Settings.screen_height))
        cls.images['screen_help'] = img

        img = pg.image.load(file_name_get(folder=consts.BM_BACKGROUNDS_FOLDER,
                                          name=Settings.im_bg_start_game)).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width, Settings.screen_height))
        cls.images['screen_start'] = img

        img = pg.image.load(file_name_get(name='im_help_key')).convert()
        img = pg.transform.smoothscale(img, (int((Settings.help_key_size.w)
                                                 * Settings.font_pos_factor_t2),
                                             int(Settings.help_key_size.h
                                                 * Settings.font_pos_factor_t2)))
        cls.images['help_key'] = img

        img = pg.image.load(file_name_get(folder=consts.BM_LOGOS_FOLDER,
                                          name='im_logo_japinol')).convert()
        img = pg.transform.smoothscale(img, (173, 39))
        cls.images['logo_jp'] = img

        img = pg.image.load(file_name_get(folder=consts.BITMAPS_FOLDER,
                                          name='im_text_aux_tower')).convert()
        img.set_colorkey(Color.BLACK)
        img = pg.transform.smoothscale(img, (170, 27))
        cls.images['text_aux_tower'] = img

        img = pg.image.load(file_name_get(name='im_board')).convert_alpha()
        cls.images['board'] = img
        Settings.board_width = Resource.images['board'].get_width()
        Settings.board_height = Resource.images['board'].get_height()
        Settings.board_x = Settings.board_base_x - Settings.board_width // 2 + Settings.board_base_width // 2
        Settings.board_y = Settings.board_base_y - Settings.board_height // 2 + Settings.board_base_height // 2

    @classmethod
    def load_and_render_score_bar_images_and_txt(cls):
        libg_jp.render_text('v.', 1360, 16,
                            cls.txt_surfaces, 'sb_version', color=Color.BLACK_SAFE)

        y = Settings.score_pos_label[1]
        libg_jp.render_text('Hanoy discs:', Settings.score_pos_label[0], y,
                            cls.txt_surfaces, 'hanoy_discs', color=Color.GREEN_DARK)
        y += Settings.text_y_distance * 2
        libg_jp.render_text('Games to Play:', Settings.score_pos_label[0], y,
                            cls.txt_surfaces, 'sb_games_to_play', color=Color.GREEN_DARK)
        y += Settings.text_y_distance
        libg_jp.render_text('Turn Max Seconds:', Settings.score_pos_label[0], y,
                            cls.txt_surfaces, 'sb_turn_max_time_secs', color=Color.GREEN_DARK)

        y += Settings.text_y_distance * 2
        libg_jp.render_text('Current Game:', Settings.score_pos_label[0], y,
                            cls.txt_surfaces, 'sb_current_game', color=Color.GREEN_DARK)
        y += Settings.text_y_distance
        libg_jp.render_text('Games Played:', Settings.score_pos_label[0], y,
                            cls.txt_surfaces, 'sb_games_played', color=Color.GREEN_DARK)

        y += Settings.text_y_distance * 2
        libg_jp.render_text('Max Score:', Settings.score_pos_label[0], y,
                            cls.txt_surfaces, 'sb_score_max', color=Color.GREEN_DARK)

        y += Settings.text_y_distance * 2
        libg_jp.render_text('Score:', Settings.score_pos_label[0], y,
                            cls.txt_surfaces, 'sb_score', color=Color.GREEN_DARK)

        y += Settings.text_y_distance * 3
        libg_jp.render_text('Completed without mistakes:', Settings.score_pos_label[0], y,
                            cls.txt_surfaces, 'sb_completed', color=Color.GREEN_DARK)

    @staticmethod
    def load_music_song(current_song):
        pg.mixer.music.load(os.path.join(consts.MUSIC_FOLDER, consts.MUSIC_BOX[current_song]))
