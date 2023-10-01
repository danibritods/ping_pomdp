import pingpomdp.pingpomdp as ppm
from collections import namedtuple

def test_is_env_state_undesirable():
    grid = ppm.PongGridlink(None,None)

    EnvState = namedtuple('GameState', ['status'])
    
    assert grid._is_env_state_undesirable(EnvState(status=-1)) is True
    assert grid._is_env_state_undesirable(EnvState(status=0)) is False
    assert grid._is_env_state_undesirable(EnvState(status=1)) is False

def test_is_env_state_desirable():
    grid = ppm.PongGridlink(None,None)

    EnvState = namedtuple('GameState', ['status'])
    
    assert grid._is_env_state_desirable(EnvState(status=-1)) is False
    assert grid._is_env_state_desirable(EnvState(status=0)) is False
    assert grid._is_env_state_desirable(EnvState(status=1)) is True

def test_active_cell_index():
    class environment():
        screen_height = 100

    grid = ppm.PongGridlink(None, environment)
    grid.n_sensory_cells = 5

    EnvState = namedtuple('GameState', ['ball_x', 'ball_y', 'paddle_y'])

    assert grid._active_cell_index(EnvState(10,10,2_000)) == 4
    assert grid._active_cell_index(EnvState(10,10,40)) == 4
    assert grid._active_cell_index(EnvState(10,10,30)) == 4
    assert grid._active_cell_index(EnvState(10,10,20)) == 3
    assert grid._active_cell_index(EnvState(10,10,10)) == 2
    assert grid._active_cell_index(EnvState(10,10,0)) == 2
    assert grid._active_cell_index(EnvState(10,10,-10)) == 2
    assert grid._active_cell_index(EnvState(10,10,-20)) == 1
    assert grid._active_cell_index(EnvState(10,10,-30)) == 0
    assert grid._active_cell_index(EnvState(10,10,-40)) == 0
    assert grid._active_cell_index(EnvState(10,10,-2_000)) == 0
