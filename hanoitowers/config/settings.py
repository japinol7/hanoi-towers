"""Module settings."""
__author__ = 'Joan A. Pinol  (japinol)'

from hanoitowers.tools.utils import utils
from hanoitowers.config.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    GAMES_TO_PLAY, TURN_MAX_TIME_SECS,
    HANOY_SOLVER_DEFAULT,
)

FPS_DEFAULT = 62  # Recommended: 62
FPS_MIN = 25
FPS_MAX = 900

CELL_DEFAULT_SIZE = 14


class Settings:
    """Settings of the game."""
    screen_width = None
    screen_height = None
    board_base_x = None
    board_base_y = None
    board_base_width = None
    board_base_height = None
    board_base_center = None
    board_x = None
    board_y = None
    board_width = None
    board_height = None
    screen_aspect_ratio = None
    screen_height_adjusted = None
    screen_width_adjusted = None
    display_start_width = None    # max. width of the user's initial display mode
    display_start_height = None   # max. height of the user's initial display mode
    cell_size = None
    fps = None
    fps_paused = None
    speed_pct = None
    has_selector_no_light = False
    is_full_screen_feature_activated = False
    is_full_screen = False
    im_screen_help = None
    im_bg_start_game = None
    score_to_win = None
    screen_near_top = None
    screen_near_bottom = None
    screen_near_right = None
    grid_width = None
    grid_height = None
    screen_bar_near_top = None
    player_position_ini = None
    are_bullets_allowed_to_collide = None
    sprite_health_bar_pos_rel = None   # Relative position for sprite health bar
    sprite_health_bar_size = None
    font_size1 = None
    font_size2 = None
    font_spc_btn_chars1 = None
    font_spc_btn_chars2 = None
    # scores tuple with label and value x positions
    score_pos_door_keys = None
    score_pos_label = None
    score_pos_x = None
    score_pos_score2 = None
    font_pos_factor = None
    font_pos_factor_t2 = None
    logo_jp_std_size = None
    help_key_size = None
    help_key_pos_factor = None
    text_y_distance = None
    games_to_play = None
    turn_max_time_secs = None
    can_games_be_paused = None
    hanoy_discs = None
    solver = None
    is_log_all_movements = None

    @classmethod
    def clean(cls):
        cls.screen_width = SCREEN_WIDTH
        cls.screen_height = SCREEN_HEIGHT
        cls.screen_aspect_ratio = cls.screen_width / cls.screen_height
        cls.screen_height_adjusted = None
        cls.screen_width_adjusted = None
        cls.board_base_x = 552
        cls.board_base_y = 50
        cls.board_base_width = 843
        cls.board_base_height = 725
        cls.board_base_center = (Settings.board_base_x + Settings.board_base_width // 2,
                                 Settings.board_base_y + Settings.board_base_height // 2)
        cls.board_x = None
        cls.board_y = None
        cls.board_width = None
        cls.board_height = None
        cls.cell_size = CELL_DEFAULT_SIZE
        cls.cell_size_ratio = cls.screen_width * cls.screen_height / CELL_DEFAULT_SIZE
        cls.fps = FPS_DEFAULT
        cls.fps_paused = 14
        cls.speed_pct = 100
        cls.has_selector_no_light = False
        cls.is_full_screen = False
        cls.im_screen_help = 'im_screen_help'
        cls.im_bg_start_game = 'im_background'
        cls.screen_near_top = None
        cls.screen_near_bottom = None
        cls.screen_near_right = None
        cls.grid_width = None
        cls.grid_height = None
        cls.screen_bar_near_top = None
        cls.player_position_ini = None
        cls.are_bullets_allowed_to_collide = False
        cls.font_size1 = None
        cls.font_size2 = None
        cls.font_spc_btn_chars1 = None
        cls.font_spc_btn_chars2 = None
        # scores tuple with label and value x positions
        cls.font_pos_factor = 0.91     # position or size factor for some text to render
        cls.font_pos_factor_t2 = 0.91  # position or size factor for some other text to render
        cls.logo_jp_std_size = utils.Size(w=244, h=55)
        cls.help_key_pos = 124, 832
        cls.help_key_size = utils.Size(w=168, h=44)
        cls.score_pos_label = 15, 70
        cls.score_pos_x = 230
        cls.text_y_distance = 30
        cls.can_games_be_paused = False
        cls.hanoy_discs = 0
        cls.solver = None
        cls.log_to_file = True

    @classmethod
    def calculate_settings(cls, games_to_play=None, full_screen=None, turn_max_secs=None,
                           speed_pct=None, hanoy_discs=None, solver=None):
        cls.clean()
        cls.hanoy_discs = hanoy_discs
        cls.games_to_play = games_to_play or GAMES_TO_PLAY
        cls.turn_max_time_secs = turn_max_secs or TURN_MAX_TIME_SECS
        cls.solver = solver or HANOY_SOLVER_DEFAULT
        # Define screen values to resize the screen and images if necessary
        cls.screen_width_adjusted = int(cls.screen_height * cls.screen_aspect_ratio)
        cls.screen_height_adjusted = cls.screen_height
        # Set full screen or windowed screen
        cls.is_full_screen = True if full_screen else False
        # Set fps
        if speed_pct and speed_pct.isdigit():
            cls.speed_pct = speed_pct
            cls.fps = int(cls.fps * int(speed_pct) / 100)
            if cls.fps < FPS_MIN:
                cls.fps = FPS_MIN
            elif cls.fps > FPS_MAX:
                cls.fps = FPS_MAX
        # Set positions for images and text
        cls.screen_near_bottom = cls.screen_height - cls.cell_size + 1
        cls.screen_near_right = cls.screen_width - cls.cell_size + 1
        cls.screen_near_bottom = cls.screen_height - cls.cell_size + 1
        cls.screen_near_right = cls.screen_width - cls.cell_size + 1
        cls.screen_bar_near_top = 10

        # Font sizes for scores, etc
        cls.font_size1 = 24
        cls.font_size2 = 36
        cls.font_spc_btn_chars1 = 15
        cls.font_spc_btn_chars2 = 21

        # Adapt size of images and text for some tested scenarios
        cls.font_pos_factor_t2 = cls.font_pos_factor
        cls.screen_bar_near_top = int(cls.screen_bar_near_top * cls.font_pos_factor)

        # Set score text and images positions and size
        cls.font_size1 = int(cls.font_size1 * cls.font_pos_factor)
        cls.font_size2 = int(cls.font_size2 * cls.font_pos_factor)
        cls.font_spc_btn_chars1 = int(cls.font_spc_btn_chars1 * cls.font_pos_factor)
        cls.font_spc_btn_chars2 = int(cls.font_spc_btn_chars2 * cls.font_pos_factor)
