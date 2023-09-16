import numpy as np

class Gridlink:
    def __init__(self, model, grid_shape = (4,8)):
        self.shape = grid_shape
        self.grid_array = np.zeros(grid_shape)
        self.model = model

    def read_cells(self, cells_to_read):
        rows, cols = self._cells_to_rows_cols(cells_to_read)
        return self.grid_array[rows, cols]

    def read_all(self):
        return self.grid_array

    def write(self, cells_to_write, values):
        rows, cols = self._cells_to_rows_cols(cells_to_write)
        self.grid_array[rows, cols] = values

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

