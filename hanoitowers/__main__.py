"""Module __main__. Entry point."""
__author__ = 'Joan A. Pinol  (japinol)'

from argparse import ArgumentParser
import gc
import traceback
import sys

import pygame as pg

from hanoitowers.config.constants import (
    GAMES_TO_PLAY_MAX, GAMES_TO_PLAY,
    TURN_MAX_TIME_SECS, TURN_MAX_TIME_SECS_MAX,
    TURN_MAX_TIME_SECS_MIN,
    LOG_START_APP_MSG, LOG_END_APP_MSG,
    HANOY_DISCS_DEFAULT, HANOY_MIN_DISCS, HANOY_MAX_DISCS,
    HANOY_SOLVERS,
)
from hanoitowers.game_entry_point import Game
from hanoitowers.validator.validator import InputValidator
from hanoitowers.tools.logger import logger
from hanoitowers.tools.logger.logger import log, LOGGER_FORMAT, LOGGER_FORMAT_NO_DATE
from hanoitowers import screen


def main():
    """Entry point of The Towers of Hanoi program."""
    # Parse optional arguments from the command line
    parser = ArgumentParser(description="The Towers of Hanoi",
                            prog="hanoitowers",
                            usage="%(prog)s usage: hanoitowers [-h] [-a] [-g GAMESTOPLAY] [-i DISCS] "
                                  "[-l] [-m] [-n] [-s] [-u TURNMAXSECS] [-d] [-t]")
    parser.add_argument('-a', '--auto', default=False, action='store_true',
                        help='Auto mode. It does not stop between games. '
                             'Only when it needs a user input')
    parser.add_argument('-g', '--gamestoplay', default=GAMES_TO_PLAY,
                        help=f"Games to play. Must be between 0 and {GAMES_TO_PLAY_MAX}")
    parser.add_argument('-i', '--discs', default=HANOY_DISCS_DEFAULT,
                        help=f"Number of hanoi discs. Must be between {HANOY_MIN_DISCS} and {HANOY_MAX_DISCS}")
    parser.add_argument('-l', '--multiplelogfiles', default=False, action='store_true',
                        help='A log file by app execution, instead of one unique log file')
    parser.add_argument('-m', '--stdoutlog', default=False, action='store_true',
                        help='Print logs to the console along with writing them to the log file')
    parser.add_argument('-n', '--nologdatetime', default=False, action='store_true',
                        help='Logs will not print a datetime')
    parser.add_argument('-s', '--solver', default=None,
                        help=f"solver algorithm. Available solvers: {', '.join(HANOY_SOLVERS)}")
    parser.add_argument('-u', '--turnmaxsecs', default=TURN_MAX_TIME_SECS,
                        help=f"Turn max seconds before the player loses some score points. "
                             f"Must be between {TURN_MAX_TIME_SECS_MIN} and {TURN_MAX_TIME_SECS_MAX}")
    parser.add_argument('-d', '--debug', default=None, action='store_true',
                        help='Debug actions when pressing the right key, information and traces')
    parser.add_argument('-t', '--debugtraces', default=None, action='store_true',
                        help='Show debug back traces information when something goes wrong')
    args = parser.parse_args()

    logger_format = LOGGER_FORMAT_NO_DATE if args.nologdatetime else LOGGER_FORMAT
    args.stdoutlog and logger.add_stdout_handler(logger_format)
    logger.add_file_handler(args.multiplelogfiles, logger_format)

    games_to_play = args.gamestoplay and int(args.gamestoplay) or 0
    turn_max_secs = args.turnmaxsecs and int(args.turnmaxsecs) or 0
    hanoy_discs = args.discs and int(args.discs) or 0
    auto = args.auto
    solver = args.solver
    semi_auto = True
    input_validator = InputValidator(games_to_play, turn_max_secs, hanoy_discs=hanoy_discs, solver=solver)
    validate_input_errors = input_validator.validate_input()
    if validate_input_errors:
        for input_error in validate_input_errors:
            log.error(input_error)
            not args.stdoutlog and print(input_error)
        return

    pg.init()
    pg.mouse.set_visible(True)
    is_music_paused = False
    log.info(LOG_START_APP_MSG)
    not args.stdoutlog and print(LOG_START_APP_MSG)
    log.info(f"App arguments: {' '.join(sys.argv[1:])}")
    # Multiple games loop
    while not Game.is_exit_game:
        try:
            game = Game(is_debug=args.debug, games_to_play=games_to_play,
                        turn_max_secs=turn_max_secs, auto=auto, semi_auto=semi_auto,
                        no_log_datetime=args.nologdatetime, stdout_log=args.stdoutlog,
                        hanoy_discs=hanoy_discs, solver=solver)
            Game.stats_gen.update({'games_played': Game.current_game})
            game.is_music_paused = is_music_paused
            screen_start_game = screen.StartGame(game)
            if 0 < Game.stats_gen['games_to_play'] <= Game.current_game:
                game.set_is_exit_game(True)
                break
            while not auto and not semi_auto and game.is_start_screen:
                screen_start_game.start_up()
            if not Game.is_exit_game:
                game.start()
                is_music_paused = game.is_music_paused
                del screen_start_game
                del game
                gc.collect()
        except FileNotFoundError as e:
            if args.debugtraces or args.debug:
                traceback.print_tb(e.__traceback__)
            log.critical(f'File not found error: {e}')
            break
        except Exception as e:
            if args.debugtraces or args.debug:
                traceback.print_tb(e.__traceback__)
            log.critical(f'ERROR. Abort execution: {e}')
            not args.stdoutlog and print(f'CRITICAL ERROR. Abort execution: {e}')
            break
    log.info(LOG_END_APP_MSG)
    not args.stdoutlog and print(LOG_END_APP_MSG)
    pg.quit()


if __name__ == '__main__':
    main()
