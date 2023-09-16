import numpy as np

GRID_SHAPE = (8,4)

class Gridlink:
    def __init__(self, model):
        self.grid_array = np.zeros(GRID_SHAPE)
        self.model = model

    def read_grid(self, cells_to_read):
        return self.grid_array[cells_to_read]

    def read_all(self):
        return self.grid_array

    def write_grid(self, cells_to_write, values):
        self.grid_array[cells_to_write] = values


    def observe(self, env_state):# -> encoded_observation:
        if self.env_state_is_undesirable(env_state):
            self._unpredictable_feedback()

        elif self.env_state_is_desirable(env_state):
            self._predictable_feedback()
        
        self._sensory_feedback(env_state)

    def act(self): #-> env_action:
        self.model.act()


    def _env_state_is_undesirable(self, env_state):
        pass

    def env_state_is_desirable(self, env_state):
        pass

    def _sensory_feedback(env_state):
        pass

    def _predictable_feedback(self):
        print("predictable")

    def _unpredictable_feedback(self):
        print("unpredictable")



