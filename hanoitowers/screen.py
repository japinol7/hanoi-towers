"""Module screen."""
__author__ = 'Joan A. Pinol  (japinol)'

from hanoitowers.tools.utils.color import Color
from hanoitowers.tools.utils import utils_graphics as libg_jp
from hanoitowers.resources import Resource
from hanoitowers.config.settings import Settings
from hanoitowers.tools.screen import screen


class Screen(screen.Screen):

    def __init__(self, game):
        super().__init__(game)


class ExitCurrentGame(screen.ExitCurrentGame):

    def __init__(self, game):
        super().__init__(game)

    def _draw(self):
        super()._draw()
        self.game.screen.blit(Resource.images['bg_blue_t1'], (0, 0))
        self.game.screen.blit(*Resource.txt_surfaces['exit_current_game_confirm'])
        self.game.screen.blit(*Resource.txt_surfaces['press_intro_to_continue_center'])


class GameOver(screen.GameOver):

    def _draw(self):
        super()._draw()
        if self.game.is_over and not self.game.winner:
            self.game.screen.blit(*Resource.txt_surfaces['game_turn_time_out'])
            self.game.screen.blit(*Resource.txt_surfaces['game_turn_time_out_2'])

        self.game.screen.blit(*Resource.txt_surfaces['press_intro_to_continue'])
        self.game.screen.blit(*Resource.txt_surfaces['press_intro_to_continue_2'])


class Pause(screen.Pause):

    def __init__(self, game):
        super().__init__(game)

    def _draw(self):
        super()._draw()
        if self.is_full_screen_switch:
            self.game.screen.blit(self.background_screenshot, (0, 0))
        self.game.screen.blit(*Resource.txt_surfaces['game_paused'])
        self.game.screen.blit(Resource.images['dim_screen'], (0, 0))


class Help(screen.Help):

    def _draw(self):
        super()._draw()
        self.game.screen.blit(Resource.images['bg_blue_t1'], (0, 0))
        self.game.screen.blit(Resource.images['screen_help'],
                              (Settings.screen_width // 2 - Resource.images['screen_help'].get_width() // 2,
                               Settings.screen_height // 2 - Resource.images['screen_help'].get_height() // 2))


class StartGame(screen.StartGame):

    def __init__(self, game):
        super().__init__(game)

        libg_jp.render_text('– Press Enter to Start –', Settings.board_base_center[0],
                            Settings.board_base_center[1] - 40,
                            Resource.txt_surfaces, 'game_start', color=Color.BLUE,
                            size=int(78*Settings.font_pos_factor_t2), align="center")
        libg_jp.render_text('– Press Enter to Start –', Settings.board_base_center[0] / 1.002,
                            Settings.board_base_center[1] / 1.006 - 40,
                            Resource.txt_surfaces, 'game_start_2', color=Color.CYAN,
                            size=int(78*Settings.font_pos_factor_t2), align="center")

        libg_jp.render_text('– A New Tournament –', Settings.board_base_center[0],
                            Settings.board_base_center[1] + 40,
                            Resource.txt_surfaces, 'tournament_start', color=Color.BLUE,
                            size=int(78*Settings.font_pos_factor_t2), align="center")
        libg_jp.render_text('– A New Tournament –', Settings.board_base_center[0] / 1.002,
                            Settings.board_base_center[1] / 1.006 + 40,
                            Resource.txt_surfaces, 'tournament_start_2', color=Color.CYAN,
                            size=int(78*Settings.font_pos_factor_t2), align="center")

        libg_jp.render_text('– A New Game –', Settings.board_base_center[0],
                            Settings.board_base_center[1] + 40,
                            Resource.txt_surfaces, 'game_start_game', color=Color.BLUE,
                            size=int(78*Settings.font_pos_factor_t2), align="center")
        libg_jp.render_text('– A New Game –', Settings.board_base_center[0] / 1.002,
                            Settings.board_base_center[1] / 1.006 + 40,
                            Resource.txt_surfaces, 'game_start_game_2', color=Color.CYAN,
                            size=int(78*Settings.font_pos_factor_t2), align="center")

    def _draw(self):
        super()._draw()
        self.game.screen.blit(Resource.images['screen_start'],
                              (Settings.screen_width // 2 - Resource.images['screen_start'].get_width() // 2, 0))
        self.game.screen.blit(Resource.images['help_key'], (Settings.help_key_pos[0], Settings.help_key_pos[1]))
        self.game.screen.blit(Resource.images['logo_jp'],
                              (Settings.screen_width - Resource.images['logo_jp'].get_width()
                              - 36 * Settings.font_pos_factor,
                              Settings.screen_height - Resource.images['logo_jp'].get_height()
                              - 9 * Settings.font_pos_factor))
        self.game.screen.blit(Resource.images['board'], (Settings.board_x, Settings.board_y))

        self.game.screen.blit(*Resource.txt_surfaces['game_start'])
        self.game.screen.blit(*Resource.txt_surfaces['game_start_2'])
        self.game.screen.blit(*Resource.txt_surfaces['game_start_game'])
        self.game.screen.blit(*Resource.txt_surfaces['game_start_game_2'])
