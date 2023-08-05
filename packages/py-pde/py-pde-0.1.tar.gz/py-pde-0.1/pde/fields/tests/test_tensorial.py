'''
.. codeauthor:: David Zwicker <david.zwicker@ds.mpg.de>
'''

import numpy as np
import pytest

from .test_generic import iter_grids
from ..tensorial import Tensor2Field
from ..base import FieldBase
from ...grids import CartesianGrid



def test_tensors():
    """ test some tensor calculations """
    grid = CartesianGrid([[0.1, 0.3], [-2, 3]], [3, 4])
    
    t1 = Tensor2Field(grid, np.full((2, 2) + grid.shape, 1))
    t2 = Tensor2Field(grid, np.full((2, 2) + grid.shape, 2))
    np.testing.assert_allclose(t2.average, [[2, 2], [2, 2]])
    assert t1.magnitude == pytest.approx(2)
    
    t3 = t1 + t2
    assert t3.grid == grid
    np.testing.assert_allclose(t3.data, 3)
    t1 += t2
    np.testing.assert_allclose(t1.data, 3)
    
    field = Tensor2Field.random_uniform(grid)
    trace = field.trace()
    from ..scalar import ScalarField
    assert isinstance(trace, ScalarField)
    np.testing.assert_allclose(trace.data, field.data.trace())
    
    t1 = Tensor2Field(grid)
    t1.data[0, 0, :] = 1
    t1.data[0, 1, :] = 2
    t1.data[1, 0, :] = 3
    t1.data[1, 1, :] = 4
    for method, value in [('min', 1), ('max', 4),
                          ('norm', np.linalg.norm([[1, 2], [3, 4]])),
                          ('squared_sum', 30), ('trace', 5),
                          ('invariant1', 5), ('invariant2', -1)]:
        p1 = t1.to_scalar(method)
        assert p1.data.shape == grid.shape
        np.testing.assert_allclose(p1.data, value)

    t2 = FieldBase.from_state(t1.state_serialized, grid=grid, data=t1.data)
    assert t1 == t2



def test_tensor_symmetrize():
    """ test advanced tensor calculations """
    grid = CartesianGrid([[0.1, 0.3], [-2, 3]], [2, 2])
    t1 = Tensor2Field(grid)
    t1.data[0, 0, :] = 1
    t1.data[0, 1, :] = 2
    t1.data[1, 0, :] = 3
    t1.data[1, 1, :] = 4
    
    # traceless = False
    t2 = t1.copy()
    t1.symmetrize(make_traceless=False, inplace=True)
    tr = t1.trace()
    assert np.all(tr.data == 5)
    t1_trans = np.swapaxes(t1.data, 0, 1)
    np.testing.assert_allclose(t1.data, t1_trans.data)
    
    ts = t1.copy()
    ts.symmetrize(make_traceless=False, inplace=True)
    np.testing.assert_allclose(t1.data, ts.data)
    
    # traceless = True
    t2.symmetrize(make_traceless=True, inplace=True)
    tr = t2.trace()
    assert np.all(tr.data == 0)
    t2_trans = np.swapaxes(t2.data, 0, 1)
    np.testing.assert_allclose(t2.data, t2_trans.data)

    ts = t2.copy()
    ts.symmetrize(make_traceless=True, inplace=True)
    np.testing.assert_allclose(t2.data, ts.data)
    
    

@pytest.mark.parametrize("grid", iter_grids())
def test_add_interpolated_tensor(grid):
    """ test the `add_interpolated` method """
    f = Tensor2Field(grid)
    a = np.random.random(f.data_shape)
    
    c = tuple(grid.point_to_cell(grid.get_random_point()))
    c_data = (Ellipsis,) + c
    p = grid.cell_to_point(c, cartesian=False)
    f.add_interpolated(p, a)
    np.testing.assert_almost_equal(f.data[c_data],
                                   a / grid.cell_volumes[c])
    
    f.add_interpolated(grid.get_random_point(cartesian=False), a)
    np.testing.assert_almost_equal(f.integral, 2 * a)
    
    f.data = 0  # reset
    add_interpolated = grid.make_add_interpolated_compiled()
    c = tuple(grid.point_to_cell(grid.get_random_point()))
    c_data = (Ellipsis,) + c
    p = grid.cell_to_point(c, cartesian=False)
    add_interpolated(f.data, p, a)
    np.testing.assert_almost_equal(f.data[c_data],
                                   a / grid.cell_volumes[c])

    add_interpolated(f.data, grid.get_random_point(cartesian=False), a)
    np.testing.assert_almost_equal(f.integral, 2 * a)

