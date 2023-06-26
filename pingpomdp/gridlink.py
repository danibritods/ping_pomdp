import numpy as np

GRID_SHAPE = (8,4)

class Gridlink:
    def __init__(self):
        self.grid_array = np.zeros(GRID_SHAPE)

    def read_grid(self, cells_to_read):
        return self.grid_array[cells_to_read]

    def read_all(self):
        return self.grid_array

    def write_grid(self, cells_to_write, values):
        self.grid_array[cells_to_write] = values


    def observe(self, env_state) -> encoded_observation:
        pass
    
    def act(self, agent_action) -> env_action:
        pass

