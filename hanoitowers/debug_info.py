"""Module debug_info."""
__author__ = 'Joan A. Pinol  (japinol)'

from datetime import datetime
from collections import OrderedDict

from hanoitowers.tools.logger.logger import log
from hanoitowers.tools.utils.utils import pretty_dict_to_string


class DebugInfo:

    def __init__(self, game):
        self.game = game

    @staticmethod
    def print_help_keys():
        print('  ^ numpad_divide: \t interactive debug output\n'
              '  ^n: \t print a list of all NPCs in all levels, ordered by level\n'
              '  ^ Shift + n: \t print a list of all NPCs in all levels, ordered by NPC name\n'
              '  ^d: \t print debug information to console\n'
              '  ^l: \t write debug information to a log file\n'
              )

    def print_debug_info(self):
        debug_dict = OrderedDict([
            ('Time', "No datetime" if self.game.no_log_datetime else str(datetime.now())),
            ('Full screen', self.game.is_full_screen_switch),
            ('------', '------'),
            ('Games to play', self.game.stats_gen['games_to_play']),
            ('Turn max time in secs', self.game.stats_gen['turn_max_time_secs']),
            ('-------', '------'),
            ('Current Game', self.game.stats_gen['current_game']),
            ('--------', '-------'),
            ('Completed without mistakes', self.game.stats_gen['completed']),
            ('--------', '------------'),
            ('Score Max', self.game.stats_gen['score_max']),
            ('---------', '-------------'),
        ])
        debug_info_title = 'Current game stats:'
        debug_info = f"{debug_info_title}\n"

        debug_info = f"{debug_info}{pretty_dict_to_string(debug_dict, with_last_new_line=True)}" \
                     f"{'-' * 62}"
        log.info(debug_info)
