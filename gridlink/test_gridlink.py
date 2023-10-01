import numpy as np
import numpy.testing as npt
import gridlink.gridlink as g


class ModelPatch():
    def __init__(self):
        self.observations = []

    def observe(self, observation):
        obs = observation.copy()
        self.observations.append(obs)

    def act(self, mock_return = [0]):
        return mock_return


class GridTest(g.Gridlink):
    def _active_cell_index(self, env_state):
        """"Mock function just to test sensory feedback"""
        #env_state: status, rally, paddle_y, ball_x, ball_y 
        return env_state[4]
    
    def _map_agent_action_to_env(self, agent_action):
        return agent_action
    
class GridObserve(GridTest):
        """
        This function:
            - Defines both desirable and undesirable states to false. 
                This ensures neutra state to apply only sensory feedback
            - Defines sensory feedback simply to isolate test
        """
        def _is_env_state_desirable(self, env_state):
            return False
        def _is_env_state_undesirable(self, env_state):
            return False
        def _sensory_feedback(self, env_state):
            self.agent.observe(env_state)

    
class Game():
    def step(self,env_state):
        return env_state

def test_grid_basic():
    test_grid = g.Gridlink(None, None, (4,8))
    assert test_grid.grid_array.shape == (4,8)

def test_grid_write():
    test_grid = g.Gridlink(None, None, (4,8))
    test_grid._write_cells([1,2,3],[1,2,3])
    exp = np.array([0,1,2,3,0,0,0,0])   
    npt.assert_array_equal(test_grid.grid_array[0], exp)

def test_grid_read():
    test_grid = g.Gridlink(None, None, (4,8))
    test_grid._write_cells([1,2,3],[1,2,3])
    exp = np.array([2,3])   
    npt.assert_array_equal(test_grid._read_cells([2,3]), exp)

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

def test_env_access_through_grid():
    environment = Game()
    grid = GridTest(None, environment)
    assert grid.env.step("test") == "test"

def test_agent_act_through_grid():
    agent = ModelPatch()
    grid = GridTest(agent, None)
    assert grid.agent.act() == [0]

def test_grid_act():
    agent = ModelPatch()
    grid = GridTest(agent, None)
    assert grid.act() == [0]

def test_grid_observe():
    agent = ModelPatch()
    environment = Game()
    grid = GridObserve(agent, environment)

    action = grid.act()
    grid.observe(action)
    
    obs = agent.observations
    exp_obs = [[0]]
    assert obs == exp_obs

def test_grid_step():
    agent = ModelPatch()
    environment = Game()
    grid = GridObserve(agent, environment)

    grid.step()

    obs = agent.observations
    exp_obs = [[0]]
    assert obs == exp_obs