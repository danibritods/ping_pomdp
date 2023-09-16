import numpy as np
import numpy.testing as npt
import gridlink as g

def test_grid_basic():
    test_grid = g.Gridlink(None, (4,8))
    assert test_grid.grid_array.shape == (4,8)

def test_grid_write():
    test_grid = g.Gridlink(None, (4,8))
    test_grid.write([1,2,3],[1,2,3])
    exp = np.array([0,1,2,3,0,0,0,0])   
    npt.assert_array_equal(test_grid.grid_array[0], exp)

def test_grid_read():
    test_grid = g.Gridlink(None, (4,8))
    test_grid.write([1,2,3],[1,2,3])
    exp = np.array([2,3])   
    npt.assert_array_equal(test_grid.read_cells([2,3]), exp)

