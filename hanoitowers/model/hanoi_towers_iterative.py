from collections import namedtuple

from hanoitowers.tools.logger.logger import log
from hanoitowers.model.stack import Stack
from hanoitowers.config.constants import HANOY_MIN_DISCS, HANOY_MAX_DISCS


HanoiTowers_Move = namedtuple('hanoi_towers_move',
                              ['move_n', 'disc_n', 'tower_from', 'tower_to', 'tower_to_len'])


class HanoiTowersException(Exception):
    pass


class HanoiTowers:
    """The Towers of Hanoi. This solver uses an iterative approach."""

    def __init__(self, n_discs, disc_locations, to_log_moves=False):
        self.n_discs = n_discs
        self.disc_locations = disc_locations  # dict. disc_num: tower, disc pos in tower
        self.to_log_moves = to_log_moves
        self.tower_start = None
        self.tower_tmp = None
        self.tower_end = None
        self.move = 1
        self.total_moves = None
        self.moves = []
        self.current_move = None

        if not isinstance(n_discs, int) and not isinstance(n_discs, float):
            raise HanoiTowersException("User Error. Invalid type for discs: must be integer or float")

        if not (HANOY_MIN_DISCS <= n_discs <= HANOY_MAX_DISCS):
            raise HanoiTowersException(f"User Error. Invalid number of discs: "
                                       f"must be between {HANOY_MIN_DISCS} and {HANOY_MAX_DISCS} .")

        self._setup()

    def _setup(self):
        self.tower_start = Stack('tower_start', 1)
        self.tower_tmp = Stack('tower_tmp', 2)
        self.tower_end = Stack('tower_end', 3)
        self.total_moves = int(pow(2, self.n_discs) - 1)

        for disc in range(self.n_discs, 0, -1):
            self.tower_start.push(disc)

        if self.n_discs % 2 == 0:
            self.tower_end, self.tower_tmp = self.tower_tmp, self.tower_end

    def __iter__(self):
        return self

    def __next__(self):
        if self.move > self.total_moves:
            raise StopIteration

        if self.move % 3 == 1:
            self.move_disc_between_towers(self.tower_start, self.tower_end, to_log=self.to_log_moves)
        elif self.move % 3 == 2:
            self.move_disc_between_towers(self.tower_start, self.tower_tmp, to_log=self.to_log_moves)
        elif self.move % 3 == 0:
            self.move_disc_between_towers(self.tower_tmp, self.tower_end, to_log=self.to_log_moves)

        self.move += 1
        self.current_move = self.moves[-1]

    def __str__(self):
        return f"HanoiTowers for n_discs: {self.n_discs}\n" \
               f"\ttower_start: {self.tower_start}\n" \
               f"\ttower_tmp: {self.tower_tmp if self.n_discs % 2 != 0 else self.tower_end}\n" \
               f"\ttower_end: {self.tower_end if self.n_discs % 2 != 0 else self.tower_tmp}"

    def move_disc_between_towers(self, tower1, tower2, to_log=False):
        no_disc_value = 0
        tower1_top_disc = tower1.peek() if not tower1.is_empty else no_disc_value
        tower2_top_disc = tower2.peek() if not tower2.is_empty else no_disc_value

        if tower1_top_disc == no_disc_value and tower2_top_disc == no_disc_value:
            raise Exception(f"No disc in towers: {tower1.name}, {tower2.name}")

        if tower1_top_disc == no_disc_value:
            ht_move = HanoiTowers_Move(self.move, tower2_top_disc, tower2.name, tower1.name, len(tower1) + 1)
            tower2.pop()
            tower1.push(tower2_top_disc)
            self.disc_locations[tower2_top_disc] = tower1.num, len(tower1)
        elif tower2_top_disc == no_disc_value:
            ht_move = HanoiTowers_Move(self.move, tower1_top_disc, tower1.name, tower2.name, len(tower2) + 1)
            tower1.pop()
            tower2.push(tower1_top_disc)
            self.disc_locations[tower1_top_disc] = tower2.num, len(tower2)
        elif tower1_top_disc <= tower2_top_disc:
            ht_move = HanoiTowers_Move(self.move, tower1_top_disc, tower1.name, tower2.name, len(tower2) + 1)
            tower1.pop()
            tower2.push(tower1_top_disc)
            self.disc_locations[tower1_top_disc] = tower2.num, len(tower2)
        else:
            ht_move = HanoiTowers_Move(self.move, tower2_top_disc, tower2.name, tower1.name, len(tower1) + 1)
            tower2.pop()
            tower1.push(tower2_top_disc)
            self.disc_locations[tower2_top_disc] = tower1.num, len(tower1)

        self.moves.append(ht_move)
        to_log and log.info(f"{ht_move.move_n:2}. Move disc {ht_move.disc_n} "
                            f"from {ht_move.tower_from} to {ht_move.tower_to}")

    def is_completed(self):
        return len(self.moves) >= self.total_moves


def main():
    from hanoitowers.tools.logger import logger

    disc_locations = {}  # disc_num: tower, disc pos in tower

    logger.add_stdout_handler()
    log.info("HanoiTowers - module text execution. Solver uses recursion")

    hanoi_towers = HanoiTowers(5, disc_locations, to_log_moves=True)
    log.info(f"Initial state:\n{hanoi_towers}")

    for _ in hanoi_towers:
        pass

    log.info(f"State after processing:\n{hanoi_towers}")


if __name__ == "__main__":
    main()
