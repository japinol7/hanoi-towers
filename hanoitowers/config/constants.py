"""Module constants."""
__author__ = 'Joan A. Pinol  (japinol)'

from datetime import datetime
import os
import sys

from hanoitowers.version import version

APP_NAME = 'hanoitowers'

GAMES_TO_PLAY = 0  # 0 means: infinite games
TURN_MAX_TIME_SECS = 15

HANOY_DISCS_DEFAULT = 5
HANOY_MIN_DISCS = 1
HANOY_MAX_DISCS = 7

HANOY_TOWERS = 3

HANOY_SOLVERS = ['iterative', 'recursive']
HANOY_SOLVER_DEFAULT = 'iterative'

DISC_POS_Y = 605
DISC_1_POS_X = 588
TOWER_POS_Y = 311
TOWER_1_POS_X = 575
TOWER_WIDTH = 28
TOWER_1_POS_X_CENTER = TOWER_1_POS_X + TOWER_WIDTH // 2
TOWER_DISTANCE = 383

DISC_WIDTH_BASE = 60
DISC_WIDTH_ADDED_PGE = 0.65
DISC_HEIGHT = 34

GAMES_TO_PLAY_MAX = 5000
TURN_MAX_TIME_SECS_MIN = 5
TURN_MAX_TIME_SECS_MAX = 900

SCREEN_WIDTH = 1536
SCREEN_HEIGHT = 900
SCROLL_NEAR_LEFT_SIDE = 380
SCROLL_NEAR_RIGHT_SIDE = SCREEN_WIDTH - SCROLL_NEAR_LEFT_SIDE
NEAR_LEFT_SIDE = 25

SCROLL_NEAR_TOP = 300
SCROLL_NEAR_BOTTOM = SCREEN_HEIGHT - SCROLL_NEAR_TOP

NEAR_TOP = 40
NEAR_BOTTOM = SCREEN_HEIGHT - NEAR_TOP
NEAR_EARTH = 40
SCREEN_NEAR_EARTH = SCREEN_HEIGHT - NEAR_EARTH
NEAR_BOTTOM_WHEN_PLATFORM = SCREEN_HEIGHT - NEAR_EARTH

NEAR_RIGHT_SIDE = SCREEN_WIDTH - NEAR_LEFT_SIDE

SCREEN_BAR_NEAR_TOP = 10
SCREEN_BAR_NEAR_BOTTOM = SCREEN_HEIGHT - 25

LOG_START_APP_MSG = f"Start app {APP_NAME} version: {version.get_version()}"
LOG_END_APP_MSG = f"End app {APP_NAME}"

LOG_FILE = os.path.join('logs', f"log_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S_%f')}.log")
LOG_FILE_UNIQUE = os.path.join('logs', "log.log")
SYS_STDOUT = sys.stdout

LOG_INPUT_ERROR_PREFIX_MSG = "User input error. "

SOUND_FORMAT = 'ogg'
MUSIC_FORMAT = 'ogg'

CURRENT_PATH = '.'
BITMAPS_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'img')
SOUNDS_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'snd', SOUND_FORMAT)
MUSIC_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'music')
FONT_DEFAULT_NAME = os.path.join(CURRENT_PATH, 'assets', 'data', 'sans.ttf')
FONT_FIXED_DEFAULT_NAME = os.path.join(CURRENT_PATH, 'assets', 'data', 'fixed.ttf')

BM_BACKGROUNDS_FOLDER = os.path.join(BITMAPS_FOLDER, 'backgrounds')
BM_LIVES_BASE_FOLDER = os.path.join(BITMAPS_FOLDER, 'lives')
BM_LOGOS_FOLDER = os.path.join(BITMAPS_FOLDER, 'logos')
BM_CLOCKS_FOLDER = os.path.join(BITMAPS_FOLDER, 'clocks')
BM_SELECTORS_FOLDER = os.path.join(BITMAPS_FOLDER, 'selectors')
BM_SPECIAL_EFFECTS_FOLDER = os.path.join(BITMAPS_FOLDER, 'special_effects')
BM_LIGHTS_FOLDER = os.path.join(BM_SPECIAL_EFFECTS_FOLDER, 'lights')

MUSIC_BOX = (
    f'action_song__192b.{MUSIC_FORMAT}',
    )

FILE_NAMES = {
    'im_background': ('background', 'png'),
    'im_screen_help': ('screen_help', 'png'),
    'im_logo_japinol': ('logo_japinol_ld', 'png'),
    'im_help_key': ('help_key', 'png'),
    'bg_blue_t1_big_logo': ('bg_blue_t1_big_logo', 'png'),
    'im_bg_blue_t1': ('bg_blue_t1', 'png'),
    'im_bg_blue_t2': ('bg_blue_t2', 'png'),
    'im_bg_black_t1': ('bg_black_t1', 'png'),
    'im_board': ('board', 'png'),
    'im_disc': ('disc_size', 'png'),
    'im_tower': ('tower', 'png'),
    'im_clocks': ('clock', 'png'),
    'im_lightS': ('im_light', 'png'),
    'im_selectors': ('im_selector', 'png'),
    'im_lights': ('im_light', 'png'),
    'im_text_aux_tower': ('text_aux_tower', 'png'),
    'snd_move': ('move', SOUND_FORMAT),
    'snd_move_failed': ('move_failed', SOUND_FORMAT),
    }
