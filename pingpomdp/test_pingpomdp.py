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


    