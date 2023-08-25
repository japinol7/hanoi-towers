from collections import namedtuple

from hanoitowers.tools.logger.logger import log
from hanoitowers.config.settings import Settings
from hanoitowers.model import hanoi_towers_iterative, hanoi_towers_recursive


HanoiSolverMapping = namedtuple('hanoi_solver_mapping', ['name', 'class_'])
HANOY_SOLVER_MAPPING = {
    'iterative': HanoiSolverMapping('iterative', hanoi_towers_iterative.HanoiTowers),
    'recursive': HanoiSolverMapping('recursive', hanoi_towers_recursive.HanoiTowers),
    }

HanoiTowers_Move = namedtuple('hanoi_towers_move', ['move_n', 'disc_n', 'tower_from', 'tower_to'])


def get_hanoi_towers_instance(disc_locations):
    hanoy_solver = Settings.solver
    log.info(f"Get instance for solver: {hanoy_solver}")
    hanoi_towers_cls = HANOY_SOLVER_MAPPING[hanoy_solver].class_
    hanoi_towers = hanoi_towers_cls(Settings.hanoy_discs, disc_locations=disc_locations)
    hanoi_towers.to_log_moves = True
    if hanoy_solver == 'recursive':
        hanoi_towers.move_discs_to_end_tower()
    return hanoi_towers
