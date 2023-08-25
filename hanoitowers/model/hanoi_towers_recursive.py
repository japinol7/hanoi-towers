from collections import namedtuple

from hanoitowers.model.actors.towers import TOWER_NAME_NUM_MAP
from hanoitowers.tools.logger.logger import log
from hanoitowers.model.stack import Stack
from hanoitowers.config.constants import HANOY_MIN_DISCS, HANOY_MAX_DISCS


HanoiTowers_Move = namedtuple('hanoi_towers_move',
                              ['move_n', 'disc_n', 'tower_from', 'tower_to', 'tower_to_len'])


class HanoiTowersException(Exception):
    pass


class HanoiTowers:
    """The Towers of Hanoi. This solver uses a recursive approach."""

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
        self.iter_move = 0

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

    def __iter__(self):
        return self

    def __next__(self):
        if self.iter_move >= self.total_moves:
            raise StopIteration

        ht_move = self.moves[self.iter_move]
        self.to_log_moves and log.info(f"{ht_move.move_n:2}. Move disc {ht_move.disc_n} "
                                       f"from {ht_move.tower_from} to {ht_move.tower_to}")

        self.disc_locations[ht_move.disc_n] = TOWER_NAME_NUM_MAP[ht_move.tower_to], ht_move.tower_to_len

        self.current_move = ht_move
        self.iter_move += 1

    def __str__(self):
        return f"HanoiTowers for n_discs: {self.n_discs}\n" \
               f"\ttower_start: {self.tower_start}\n" \
               f"\ttower_tmp: {self.tower_tmp}\n" \
               f"\ttower_end: {self.tower_end}"

    def move_disc_between_towers(self, start, end, tmp, disc, to_log=False):
        if disc == 1:
            ht_move = HanoiTowers_Move(self.move, start.peek(), start.name, end.name, len(end) + 1)
            self.moves.append(ht_move)
            to_log and log.info(f"{ht_move.move_n:2}. Move disc {ht_move.disc_n} "
                                f"from {ht_move.tower_from} to {ht_move.tower_to}")
            self.move += 1
            end.push(start.pop())
            return

        self.move_disc_between_towers(start, tmp, end, disc - 1)
        self.move_disc_between_towers(start, end, tmp, 1)
        self.move_disc_between_towers(tmp, end, start, disc - 1)

    def move_discs_to_end_tower(self):
        self.move_disc_between_towers(self.tower_start, self.tower_end, self.tower_tmp,
                                      self.n_discs, to_log=self.to_log_moves)

    def is_completed(self):
        return self.iter_move >= self.total_moves


def main():
    from hanoitowers.tools.logger import logger

    disc_locations = {}  # disc_num: tower, disc pos in tower

    logger.add_stdout_handler()
    log.info("HanoiTowers - module text execution. Solver uses recursion")

    hanoi_towers = HanoiTowers(5, disc_locations, to_log_moves=True)
    log.info(f"Initial state:\n{hanoi_towers}")

    hanoi_towers.move_discs_to_end_tower()
    for _ in hanoi_towers:
        pass

    log.info(f"State after processing:\n{hanoi_towers}")


if __name__ == "__main__":
    main()
