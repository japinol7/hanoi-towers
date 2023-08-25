"""Module help_info."""
__author__ = 'Joan A. Pinol  (japinol)'


class HelpInfo:
    """Manages information used for help purposes."""

    @staticmethod
    def print_help_keys():
        print('  F1: \t show a help screen while playing the game'
              '  L_Ctrl + R_Alt + g:  grid\n'
              '   p: \t pause\n'
              ' ESC: exit game\n'
              '  ^m: \t pause/resume music\n'
              '  ^s: \t sound effects on/off\n'
              '  L_Alt + R_Alt + Enter: change full screen / normal screen mode\n'
              '  ^h: \t shows this help\n'
              )
