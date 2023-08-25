"""Module player."""
__author__ = 'Joan A. Pinol  (japinol)'

from abc import ABC, abstractmethod

from hanoitowers.model.actors.towers import TOWER_NUM_NAME_MAP
from hanoitowers.model.experience_points import ExperiencePoints
from hanoitowers.resources import Resource
from hanoitowers.tools.logger.logger import log


class PlayerBase(ABC):
    players = []

    def __init__(self, name):
        self.name = name
        self.turn_played = False
        self.stats = {
            'completed': 0,
            'uncompleted': 0,
            'games_started': 0,
            'score': 0,
            'total_games_played': 0,
            }
        self.stats_old = {key: None for key in self.stats}
        self.__class__.players.append(self)
        log.info(f"Create {self}")

    def update_stats_for_new_game(self, game):
        if self.stats['score'] > game.__class__.stats_gen['score_max']:
            game.__class__.stats_gen['score_max'] = self.stats['score']
        self.stats['score'] = 0

    @abstractmethod
    def update(self, board):
        pass

    def move_disc(self, game, disc, tower):
        if TOWER_NUM_NAME_MAP[disc.tower] == tower.long_name:
            return

        log.info(f"Player tries to move disc {disc.disc_number} from tower {TOWER_NUM_NAME_MAP[disc.tower]} "
                 f"to tower {tower.long_name}")
        xp_points_state = 'bad_move'
        move_auto = game.next_movement_auto(update_disc_position=False)
        if all((disc.disc_number == move_auto.disc_n,
                TOWER_NUM_NAME_MAP[disc.tower] == move_auto.tower_from,
                tower.long_name == move_auto.tower_to
                )):
            xp_points_state = 'good_move'
            game.sound_effects and Resource.sound_move.play()
        else:
            game.is_completed_without_help = False
            game.sound_effects and Resource.sound_move_failed.play()

        game.update_disc_position(move_auto)
        self.stats['score'] += ExperiencePoints.xp_points[xp_points_state]

    def __str__(self):
        return f"Player: {self.name}. Class: {self.__class__.__name__}"

    def __repr__(self):
        return f"{self.__class__.__name__}" \
               f"({self.name})"


class Player(PlayerBase):

    def __init__(self, name):
        super().__init__(name)

    def update(self, board):
        super().update(board)
