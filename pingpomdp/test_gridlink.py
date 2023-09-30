import numpy as np
import numpy.testing as npt
import gridlink as g

class ModelPatch():
    def __init__(self):
        self.observations = []

    def observe(self, observation):
        obs = observation.copy()
        self.observations.append(obs)

class GridTest(g.Gridlink):
    def _active_cell_index(self, env_state):
        """"Mock function just to test sensory feedback"""
        #env_state: status, rally, paddle_y, ball_x, ball_y 
        return env_state[4]
    
class Game():
    def step(self,env_state):
        return env_state

def test_grid_basic():
    test_grid = g.Gridlink(None, None, (4,8))
    assert test_grid.grid_array.shape == (4,8)

def test_grid_write():
    test_grid = g.Gridlink(None, None, (4,8))
    test_grid.write([1,2,3],[1,2,3])
    exp = np.array([0,1,2,3,0,0,0,0])   
    npt.assert_array_equal(test_grid.grid_array[0], exp)

def test_grid_read():
    test_grid = g.Gridlink(None, None, (4,8))
    test_grid.write([1,2,3],[1,2,3])
    exp = np.array([2,3])   
    npt.assert_array_equal(test_grid.read_cells([2,3]), exp)

def test_predictable_feedback():
    agent = ModelPatch()
    test_grid = g.Gridlink(agent, None, (1,4),(1,2), observation_mode="sensory_cells")

    ones = np.ones(len(test_grid.sensory_cells))
    zeros = np.zeros(len(test_grid.sensory_cells))

    exp_obs = [ones,zeros]*g.N_PREDICTABLE_CYCLES
    test_grid._predictable_feedback()

    npt.assert_array_equal(agent.observations, exp_obs)

def test_unpredictable_feedback():
    agent = ModelPatch()
    test_grid = g.Gridlink(agent, None, (1,4),(1,2), observation_mode="sensory_cells")

    exp_obs_shape = (g.N_UNPREDICTABLE_CYCLES, test_grid.n_sensory_cells)
    rng = np.random.default_rng(seed=42) 
    exp_obs = rng.integers(0,2,exp_obs_shape)

    test_grid._unpredictable_feedback()

    npt.assert_array_equal(agent.observations, exp_obs)

def test_sensory_feedback_01():
    agent = ModelPatch()
    grid = GridTest(agent, None, (1,4),(1,2), observation_mode="sensory_cells")

    #env_state = status, rally, paddle_y, ball_x, ball_y 
    env_state = [0,0,0,0,1]
    grid._sensory_feedback(env_state)
    obs = agent.observations

    exp_obs = np.array([0,1])

    npt.assert_array_equal(obs[0], exp_obs)

def test_sensory_feedback_10():
    agent = ModelPatch()
    grid = GridTest(agent, None, (1,4),(1,2), observation_mode="sensory_cells")

    #env_state = status, rally, paddle_y, ball_x, ball_y 
    env_state = [0,0,0,0,0]
    grid._sensory_feedback(env_state)
    obs = agent.observations

    exp_obs = np.array([1,0])

    npt.assert_array_equal(obs[0], exp_obs)