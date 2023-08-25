import os
import json
import pytest

os.environ['LOG_LEVEL'] = 'ERROR'

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__), '..')
)


@pytest.fixture(scope='session')
def hanoi_towers_moves_resource():
    with open(os.path.join(__location__, 'fixtures', 'hanoi_towers_data.json'), 'r') as fin:
        hanoi_towers_data = json.loads(fin.read())
    return hanoi_towers_data
