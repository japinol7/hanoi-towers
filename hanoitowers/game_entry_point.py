"""Module game_entry_point."""
__author__ = 'Joan A. Pinol  (japinol)'
__all__ = ['Game']

import pygame as pg

from hanoitowers.model.actor_type import ActorCategoryType
from hanoitowers.model.actors.clock import ClockTimerA
from hanoitowers.model.actors.disc_sprite import create_disc_sprites, DiscSprite
from hanoitowers.model.actors.towers import create_tower_sprites, TOWER_NAME_NUM_MAP
from hanoitowers.model.experience_points import ExperiencePoints
from hanoitowers.model import hanoi_towers
from hanoitowers.model.player import Player
from hanoitowers.score_bar import ScoreBar

from hanoitowers.config.constants import (
    FONT_DEFAULT_NAME,
    FONT_FIXED_DEFAULT_NAME,
    DISC_1_POS_X,
    DISC_POS_Y,
    TOWER_1_POS_X,
    TOWER_POS_Y,
    HANOY_TOWERS,
)
from hanoitowers.debug_info import DebugInfo
from hanoitowers.help_info import HelpInfo
from hanoitowers.tools.utils import utils_graphics as libg_jp
from hanoitowers.resources import Resource
from hanoitowers import screen
from hanoitowers.tools.logger.logger import log
from hanoitowers.config.settings import Settings
from hanoitowers.model.sprite_selectors import SelectorA


class Game:
    """Represents a 'The Towers of Hanoi' game."""
    is_exit_game = False
    is_over = False
    is_first_game = True
    current_game = 0
    current_time = None
    turn_time_out = False
    size = None
    screen = None
    screen_flags = None
    normal_screen_flags = None
    full_screen_flags = None
    no_log_datetime = False
    stdout_log = False
    stats_gen = {
        'current_game': 0,
        'games_played': 0,
        'turn_max_time_secs': 0,
        'games_to_play': 0,
        'hanoy_discs': 0,
        'score_max': 0,
        'completed': 0,
        }
    stats_gen_old = {key: None for key in stats_gen}

    def __init__(self, is_debug=None, games_to_play=None, turn_max_secs=None,
                 speed_pct=None, auto=None, semi_auto=None, no_log_datetime=None,
                 stdout_log=None, hanoy_discs=None, solver=None,
                 is_no_display_scaled=None):
        self.name = "The Towers of Hanoi v 0.01"
        self.name_short = "The Towers of Hanoi"
        self.name_long = "The Towers of Hanoi"
        self.name_desc = "The Towers of Hanoi  (c) 2020, 2023."
        self.hanoi_towers = None
        self.auto = auto
        self.semi_auto = semi_auto
        self.stats = {}
        self.stats_old = {}
        self.start_time = None
        self.done = None
        self.is_hanoi_completed = False
        self.is_completed_without_help = True
        self.player = None
        self.winner = None
        self.is_debug = is_debug
        self.is_paused = False
        self.is_start_screen = True
        self.is_full_screen_switch = False
        self.is_help_screen = False
        self.is_exit_curr_game_confirm = False
        self.is_music_paused = False
        self.sound_effects = True
        self.show_fps = False
        self.current_position = False
        self.clock = False
        self.active_sprites = None
        self.clock_in_game = None
        self.clock_sprites = None
        self.disc_sprites = None
        self.disc_locations = {}  # disc_num: tower, disc pos in tower
        self.tower_sprites = None
        self.selector_sprites = pg.sprite.Group()
        self.score_bars = None
        self.help_info = None
        self.debug_info = None
        self.current_song = 0
        self.screen_exit_current_game = None
        self.screen_game_over = None
        self.screen_pause = None
        self.screen_help = None
        self.selected_disc = None
        self.selected_tower = None
        self.mouse_pos = (0, 0)

        if not Game.current_game:
            self._first_game_setup(
                no_log_datetime, stdout_log, games_to_play,
                turn_max_secs, speed_pct, hanoy_discs,
                solver, is_no_display_scaled)
        else:
            self.player = Player.players[0]
        self.hanoi_towers = hanoi_towers.get_hanoi_towers_instance(self.disc_locations)
        self._score_bars_setup()
        self._screens_setup()

    def _first_game_setup(self, no_log_datetime, stdout_log, games_to_play,
                          turn_max_secs, speed_pct, hanoy_discs,
                          solver, is_no_display_scaled=None):
        Game.is_first_game = True
        Game.no_log_datetime = no_log_datetime
        Game.stdout_log = stdout_log

        # Calculate settings
        pg_display_info = pg.display.Info()
        Settings.display_start_width = pg_display_info.current_w
        Settings.display_start_height = pg_display_info.current_h
        Settings.calculate_settings(games_to_play=games_to_play, turn_max_secs=turn_max_secs,
                                    speed_pct=speed_pct, hanoy_discs=hanoy_discs, solver=solver)
        Game.stats_gen.update({'turn_max_time_secs': Settings.turn_max_time_secs})
        Game.stats_gen.update({'games_to_play': Settings.games_to_play})

        # Set screen to the settings configuration
        Game.size = [Settings.screen_width, Settings.screen_height]
        Game.full_screen_flags = pg.FULLSCREEN if is_no_display_scaled else pg.FULLSCREEN | pg.SCALED
        Game.normal_screen_flags = pg.SHOWN if is_no_display_scaled else pg.SHOWN | pg.SCALED
        Game.screen_flags = Game.full_screen_flags if Settings.is_full_screen else Game.normal_screen_flags
        Game.screen = pg.display.set_mode(Game.size, Game.screen_flags)

        # Load and render resources
        Resource.load_and_render_background_images()
        Resource.load_and_render_score_bar_images_and_txt()
        Resource.load_sound_resources()
        Resource.load_music_song(self.current_song)

        # Render characters in some colors to use it as a cache
        libg_jp.chars_render_text_tuple(font_name=FONT_DEFAULT_NAME)
        libg_jp.chars_render_text_tuple(font_name=FONT_FIXED_DEFAULT_NAME)

        self.player = Player("Player 1")

        # Initialize music
        pg.mixer.music.set_volume(0.7)
        pg.mixer.music.play(loops=-1)
        if self.is_music_paused:
            pg.mixer.music.pause()

    def _score_bars_setup(self):
        self.score_bars = ScoreBar(self, Game.screen)

    def _screens_setup(self):
        self.screen_exit_current_game = screen.ExitCurrentGame(self)
        self.screen_help = screen.Help(self)
        self.screen_pause = screen.Pause(self)
        self.screen_game_over = screen.GameOver(self)

    @staticmethod
    def set_is_exit_game(is_exit_game):
        Game.is_exit_game = is_exit_game

    def create_clock_in_game(self):
        if self.clock_in_game:
            self.clock_in_game.kill()

        self.clock_in_game = ClockTimerA(x=1180, y=Settings.board_base_y - 35,
                                         game=self, time_in_secs=Settings.turn_max_time_secs,
                                         trigger_method=self.clock_in_game_trigger_method)
        self.clock_sprites.add([self.clock_in_game])

    def clock_in_game_trigger_method(self):
        log.info(f"Timer off. Add turn timer penalty to the player score: "
                 f"{ExperiencePoints.xp_points['turn_timer_penalty']}")
        self.player.stats['score'] += ExperiencePoints.xp_points['turn_timer_penalty']
        self.create_clock_in_game()

    def write_game_over_info_to_file(self):
        self.debug_info.print_debug_info()

    def next_movement_auto(self, update_disc_position=True):
        self.selected_disc = None
        self.selected_tower = None
        try:
            next(self.hanoi_towers)
        except StopIteration:
            self.is_hanoi_completed = True

        move = self.hanoi_towers.current_move
        update_disc_position and self.update_disc_position(move)

        self.create_clock_in_game()
        if self.hanoi_towers.is_completed():
            self.is_hanoi_completed = True

        return move

    def update_disc_position(self, move):
        DiscSprite.discs_map[move.disc_n].tower = TOWER_NAME_NUM_MAP[move.tower_to]
        log.info('Discs positions:\n     ' + '\n     '.join(
            [f"Disc {disc.name} is in tower {disc.tower}" for disc in self.disc_sprites]
        ))

    def handle_sprite_selector(self):
        sprite = None
        for selector in self.selector_sprites:
            sprite = selector.get_pointed_sprite()
        if sprite and sprite.category_type == ActorCategoryType.DISC:
            self.selected_disc = sprite
            self.selected_tower = None
        elif self.selected_disc and sprite and sprite.category_type == ActorCategoryType.TOWER:
            self.selected_tower = sprite
        else:
            self.selected_disc = None
            self.selected_tower = None
        if self.selected_disc and self.selected_tower:
            self.player.move_disc(self, self.selected_disc, self.selected_tower)

    def put_initial_actors_on_the_board(self):
        self.active_sprites = pg.sprite.Group()
        self.clock_sprites = pg.sprite.Group()
        self.selector_sprites = pg.sprite.Group()

        self.tower_sprites = pg.sprite.Group()
        tower_sprites = create_tower_sprites(x=TOWER_1_POS_X, y=TOWER_POS_Y, game=self, n_towers=HANOY_TOWERS)
        tower_sprites[0].long_name = 'tower_start'
        tower_sprites[1].long_name = 'tower_tmp'
        tower_sprites[2].long_name = 'tower_end'
        self.tower_sprites.add(tower_sprites)
        self.active_sprites.add(self.tower_sprites)

        self.disc_sprites = pg.sprite.Group()
        Game.stats_gen['hanoy_discs'] = Settings.hanoy_discs
        disc_sprites = create_disc_sprites(x=DISC_1_POS_X, y=DISC_POS_Y, game=self, n_discs=Settings.hanoy_discs)
        self.disc_sprites.add(disc_sprites)
        self.active_sprites.add(self.disc_sprites)

        log.info("Waiting input from player")
        self.create_clock_in_game()

        self.selector_sprites.add(
            SelectorA(0, 0, self),
            )

    def update_screen(self):
        # Handle game screens
        if self.is_paused or self.is_full_screen_switch:
            self.screen_pause.start_up(is_full_screen_switch=self.is_full_screen_switch)
        if self.is_help_screen:
            self.screen_help.start_up()
        elif self.is_exit_curr_game_confirm:
            self.screen_exit_current_game.start_up()
        elif Game.is_over and not self.auto and not self.semi_auto:
            self.screen_game_over.start_up()
        else:
            if not Game.is_over:
                Game.screen.blit(Resource.images['background'], (0, 0))
                Game.screen.blit(Resource.images['board'], (Settings.board_x, Settings.board_y))
                Game.screen.blit(Resource.images['text_aux_tower'], (890, 686))
            elif not self.auto and not self.semi_auto:
                Game.screen.blit(Resource.images['bg_blue_t2'], (0, 0))
            # Update score bars
            self.score_bars.update()

            if not Game.is_over:
                # Draw active sprites
                self.disc_sprites.update()
                self.active_sprites.draw(Game.screen)
                for clock in self.clock_sprites:
                    clock.draw_text()
                self.clock_sprites.update()

                for selector in self.selector_sprites:
                    selector.update()
                self.selector_sprites.draw(Game.screen)

        self.show_fps and pg.display.set_caption(f"{self.clock.get_fps():.2f}")

    def update_status(self):
        if self.is_hanoi_completed:
            self.update_status_if_game_over()

    def update_status_if_game_over(self):
        self.is_over = True
        self.done = True
        self.clock_in_game.clock.set_off()

    def start(self):
        Game.is_exit_game = False
        Game.is_over = False

        Game.current_game += 1
        Game.stats_gen.update({'current_game': Game.current_game})
        self.player.update_stats_for_new_game(game=self)
        pg.display.set_caption(self.name_short)
        self.clock = pg.time.Clock()
        self.start_time = pg.time.get_ticks()

        self.put_initial_actors_on_the_board()

        self.help_info = HelpInfo()
        self.debug_info = DebugInfo(self)

        if Game.is_first_game:
            Resource.render_text_frequently_used(self)
            self.debug_info.print_debug_info()

        # Current game loop
        self.done = False
        while not self.done:
            self.current_time = pg.time.get_ticks()
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.is_exit_curr_game_confirm = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        if Settings.can_games_be_paused and not self.auto:
                            self.is_paused = True
                    elif event.key == pg.K_d and not self.auto:
                        if self.is_debug and pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.debug_info.print_debug_info()
                    elif event.key == pg.K_s:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.sound_effects = not self.sound_effects
                    elif event.key == pg.K_m:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.is_music_paused = not self.is_music_paused
                            if self.is_music_paused:
                                pg.mixer.music.pause()
                            else:
                                pg.mixer.music.unpause()
                    elif event.key == pg.K_F1:
                        if not self.is_exit_curr_game_confirm:
                            self.is_help_screen = not self.is_help_screen
                    elif event.key in (pg.K_KP_ENTER, pg.K_RETURN) and not self.auto:
                        if pg.key.get_mods() & pg.KMOD_LALT:
                            self.is_full_screen_switch = True
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_n:
                        self.next_movement_auto()
                        self.player.stats['score'] += ExperiencePoints.xp_points['bad_move']
                        self.is_completed_without_help = False
                    elif event.key == pg.K_F5:
                        self.show_fps = not self.show_fps
                elif event.type == pg.MOUSEBUTTONDOWN \
                     and pg.mouse.get_pressed(num_buttons=3)[0]:
                    self.mouse_pos = pg.mouse.get_pos()
                    self.handle_sprite_selector()

                self.mouse_pos = pg.mouse.get_pos()

            if not self.is_over:
                self.update_screen()
                self.update_status()
                if self.is_over:
                    if self.is_completed_without_help:
                        Game.stats_gen['completed'] += 1
                    self.write_game_over_info_to_file()

            self.is_paused and self.clock.tick(Settings.fps_paused) or self.clock.tick(Settings.fps)
            pg.display.flip()
