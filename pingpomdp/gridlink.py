import numpy as np
RNG = np.random.default_rng(seed=42)

GRID_SHAPE = (4,8)
SENSORY_CELLS = (0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20)
OBSERVATION_MODE = "whole_grid" #agent can observe "whole_grid" or just "sensory_cells"
N_PREDICTABLE_CYCLES = 200
N_UNPREDICTABLE_CYCLES = 5

class Gridlink:
    def __init__(self, agent, grid_shape = GRID_SHAPE, sensory_cells = SENSORY_CELLS, observation_mode = OBSERVATION_MODE):
        self.agent = agent
        self.shape = grid_shape
        self.grid_array = np.zeros(grid_shape)

        self.sensory_cells = sensory_cells
        self.n_sensory_cells = len(sensory_cells)

        if observation_mode == "whole_grid":
            self.send_observation = self.read_all
        elif observation_mode == "sensory_cells":
            self.send_observation = self.read_sensory_cells
        else:
            raise ValueError("observation_mode invalid! It can be either 'whole_grid' or 'sensory_cells'")
        #add the option of sensory AREA instead of only sensory CELLS

        #later will be more efficient use the grid just as a interface, 
        # without actually updating and reading the grid all the time.
        #I'll work on it another, less day

    def read_cells(self, cells_to_read):
        rows, cols = self._cells_to_rows_cols(cells_to_read)
        return self.grid_array[rows, cols]

    def read_all(self):
        return self.grid_array
    
    def read_sensory_cells(self):
        rows, cols = self._cells_to_rows_cols(self.sensory_cells)
        return self.grid_array[rows, cols]

    def write(self, cells_to_write, values):
        rows, cols = self._cells_to_rows_cols(cells_to_write)
        self.grid_array[rows, cols] = values

    def write_sensory_cells(self, values):
        rows, cols = self._cells_to_rows_cols(self.sensory_cells)
        self.grid_array[rows, cols] = values

    def write_motor_region(self, values):
        pass

    def observe(self, env_state):# -> encoded_observation:
        if self.env_state_is_undesirable(env_state):
            self._unpredictable_feedback()

        elif self.env_state_is_desirable(env_state):
            self._predictable_feedback()
        
        self._sensory_feedback(env_state)

    def act(self): #-> env_action:
       return self.agent.act()


    def _env_state_is_undesirable(self, env_state):
        raise NotImplementedError("Undesired state must be defined for each environment.")

    def env_state_is_desirable(self, env_state):
        raise NotImplementedError("Desired state must be defined for each environment.")

    def _sensory_feedback(env_state):
        raise NotImplementedError("Sensory feedback must implemented for each environment.")

    def _predictable_feedback(self):
        for i in range(N_PREDICTABLE_CYCLES):
            ones = np.ones(self.n_sensory_cells)
            self.write_sensory_cells(ones)
            self.agent.observe(self.send_observation())

            zeros = np.zeros(self.n_sensory_cells)
            self.write_sensory_cells(zeros)
            self.agent.observe(self.send_observation())

    def _unpredictable_feedback(self):
        for i in range(N_UNPREDICTABLE_CYCLES):
            rand_obs = RNG.integers(0,2,self.n_sensory_cells)
            self.write_sensory_cells(rand_obs)
            self.agent.observe(self.send_observation())
            
        

    def _oneD_to_twoD(self,index):
        n = self.shape[1]
        row = index // n
        column = index % n
        return (row, column)

    def _cells_to_rows_cols(self,cells_index):
        if isinstance(cells_index[0], int):
            rows, cols = zip (*map(self._oneD_to_twoD, cells_index))
        elif isinstance(cells_index[0], tuple):
            rows, cols = zip (*cells_index)
        else:
            # Raise an error if the cells are not valid indexes
            raise ValueError("The cells_index must be either a list of ints or a list of tuples")
        return rows, cols
