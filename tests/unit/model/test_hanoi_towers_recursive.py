import json

import pytest

from hanoitowers.config.constants import HANOY_MIN_DISCS, HANOY_MAX_DISCS
from hanoitowers.model.hanoi_towers_recursive import HanoiTowers, HanoiTowersException


class TestHanoiTowers:

    @pytest.mark.parametrize('n_discs', range(1, 8))
    def test_hanoi_towers(self, n_discs, hanoi_towers_moves_resource):
        disc_locations = {}
        hanoi_towers = HanoiTowers(n_discs, disc_locations, to_log_moves=False)
        hanoi_towers.move_discs_to_end_tower()
        for _ in hanoi_towers:
            pass
        result = json.dumps(hanoi_towers.moves)
        expected = json.dumps(hanoi_towers_moves_resource.get(str(n_discs), []))
        assert result == expected

    @pytest.mark.parametrize('n_discs', [
        None,
        HANOY_MIN_DISCS - 1,
        HANOY_MAX_DISCS + 1,
        ])
    def test_hanoi_towers_sad_paths(self, n_discs):
        with pytest.raises(HanoiTowersException):
            disc_locations = {}
            HanoiTowers(n_discs, disc_locations, to_log_moves=False)
