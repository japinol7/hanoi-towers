"""Module score_bar."""
__author__ = 'Joan A. Pinol  (japinol)'

from hanoitowers.tools.utils.color import Color
from hanoitowers.tools.utils import utils_graphics as libg_jp
from hanoitowers.resources import Resource
from hanoitowers.config.settings import Settings
from hanoitowers.version import version


class ScoreBar:
    """Represents a score bar."""

    def __init__(self, game, screen):
        self.game = game
        self.game_cls = game.__class__
        # self.player1 = self.game_cls.stats_gen['players'][0]
        self.screen = screen

    def draw_chars_render_text(self, text, x, y, color=Color.YELLOW):
        libg_jp.draw_text_rendered(text, x, y, self.screen, color)

    def render_stats_if_necessary(self, x, y, stats_name, color=Color.BLUE_VIOLET):
        libg_jp.draw_text_rendered(text=f'{self.game.stats[stats_name]}',
                                   x=x, y=y, screen=self.screen, color=color)
        if self.game.stats[stats_name] != self.game.stats_old[stats_name]:
            self.game.stats_old[stats_name] = self.game.stats[stats_name]

    def render_stats_gen_if_necessary(self, x, y, stats_name, color=Color.BLUE_VIOLET):
        libg_jp.draw_text_rendered(text=f'{self.game_cls.stats_gen[stats_name]}',
                                   x=x, y=y, screen=self.screen, color=color)
        if self.game_cls.stats_gen[stats_name] != self.game_cls.stats_gen_old[stats_name]:
            self.game_cls.stats_gen_old[stats_name] = self.game_cls.stats_gen[stats_name]

    def render_player_stats_if_necessary(self, x, y, player, stats_name, color=Color.BLUE_VIOLET):
        libg_jp.draw_text_rendered(text=f'{player.stats[stats_name]}',
                                   x=x, y=y, screen=self.screen, color=color)
        if player.stats[stats_name] != player.stats_old[stats_name]:
            player.stats_old[stats_name] = player.stats[stats_name]

    def render_player_attributes_if_necessary(self, x, y, player, stats_name, color=Color.BLUE_VIOLET):
        libg_jp.draw_text_rendered(text=f'{player.__dict__[stats_name]}',
                                   x=x, y=y, screen=self.screen, color=color)

    def draw_general_stats(self):
        # Draw score titles
        self.screen.blit(*Resource.txt_surfaces['hanoy_discs'])
        if self.game.stats_gen['games_to_play'] > 0:
            self.screen.blit(*Resource.txt_surfaces['sb_games_to_play'])
        self.screen.blit(*Resource.txt_surfaces['sb_current_game'])
        self.screen.blit(*Resource.txt_surfaces['sb_games_played'])
        self.screen.blit(*Resource.txt_surfaces['sb_turn_max_time_secs'])
        self.screen.blit(*Resource.txt_surfaces['sb_score_max'])
        self.screen.blit(*Resource.txt_surfaces['sb_score'])
        self.screen.blit(*Resource.txt_surfaces['sb_completed'])
        self.screen.blit(*Resource.txt_surfaces['sb_version'])
        self.screen.blit(Resource.images['help_key'], (Settings.help_key_pos[0], Settings.help_key_pos[1]))

        # Draw score stats and render them if needed
        libg_jp.draw_text_rendered(text=f"{version.get_version()}",
                                   x=1390, y=16, screen=self.screen, color=Color.BLACK_SAFE,
                                   space_btw_chars=12, is_font_fixed=False)
        y = 0
        self.render_stats_gen_if_necessary(Settings.score_pos_x, Settings.score_pos_label[1] + y, 'hanoy_discs')

        y += Settings.text_y_distance * 2
        if self.game.stats_gen['games_to_play'] > 0:
            self.render_stats_gen_if_necessary(Settings.score_pos_x, Settings.score_pos_label[1] + y, 'games_to_play')

        y += Settings.text_y_distance
        self.render_stats_gen_if_necessary(Settings.score_pos_x, Settings.score_pos_label[1] + y, 'turn_max_time_secs')

        y += Settings.text_y_distance * 2
        self.render_stats_gen_if_necessary(Settings.score_pos_x, Settings.score_pos_label[1] + y, 'current_game')
        y += Settings.text_y_distance
        self.render_stats_gen_if_necessary(Settings.score_pos_x, Settings.score_pos_label[1] + y, 'games_played')

        y += Settings.text_y_distance * 2
        self.render_stats_gen_if_necessary(Settings.score_pos_x, Settings.score_pos_label[1] + y, 'score_max')

        y += Settings.text_y_distance * 2
        self.render_player_stats_if_necessary(Settings.score_pos_x, Settings.score_pos_label[1] + y,
                                              self.game.player, 'score')

        y += Settings.text_y_distance * 3
        self.render_stats_gen_if_necessary(Settings.score_pos_x + 90, Settings.score_pos_label[1] + y, 'completed')

    def update(self):
        self.draw_general_stats()
