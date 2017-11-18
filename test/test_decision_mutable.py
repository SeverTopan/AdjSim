import sys
import os
import pytest
import itertools
import math

import numpy as np

from . import common

class InvalidClass(object):
    pass

@pytest.mark.parametrize("mutable_min,mutable_max", [(0, 1.6), (-1.4, 0.5), (0.0, 7.0), (-7, 0.4), (300.7, 400.9), (-300.5, 400.2), (-400.5, -300.6)])
def test_float(mutable_min, mutable_max):
    import adjsim

    d = adjsim.decision.DecisionMutableFloat(mutable_min, mutable_max)

    # Test parameters.
    assert d.max_val == mutable_max
    assert d.min_val == mutable_min

    # Test valid inputs.
    valid_values = [(mutable_max - mutable_min)/2 + mutable_min, mutable_min, mutable_max]

    for value in valid_values:
        d._set_value(value)
        assert d.value == value

    # Test invalid inputs.
    invalid_types = [None, InvalidClass()]
    
    for value in invalid_types:
        with pytest.raises(TypeError):
            d._set_value(value)

    invalid_values = [mutable_min - 1, mutable_max + 1]

    for value in invalid_values:
        with pytest.raises(ValueError):
            d._set_value(value)

    # Test random generation.

    for _ in range(50):
        d._set_value_random()
        assert d.value <= d.max_val and d.value >= d.min_val

    for _ in range(50):
        d._perturb_around_locus((mutable_max - mutable_min)/2 + mutable_min)
        assert d.value <= d.max_val and d.value >= d.min_val

    for _ in range(50):
        d._perturb_locally()
        assert d.value <= d.max_val and d.value >= d.min_val

@pytest.mark.parametrize("mutable_min,mutable_max", [(0, 1), (-1, 0), (0.0, 7.0), (-7, 0), (300, 400), (-300, 400), (-400, -300)])
def test_int(mutable_min, mutable_max):
    import adjsim

    d = adjsim.decision.DecisionMutableInt(mutable_min, mutable_max)

    # Test parameters.
    assert d.max_val == int(mutable_max)
    assert d.min_val == int(mutable_min)

    # Test valid inputs.
    valid_values = [(mutable_max - mutable_min)/2 + mutable_min, mutable_min, mutable_max]

    for value in valid_values:
        d._set_value(value)
        assert d.value == int(value)

    # Test invalid inputs.
    invalid_types = [None, InvalidClass()]

    for value in invalid_types:
        with pytest.raises(TypeError):
            d._set_value(value)

    invalid_values = [mutable_min - 1, mutable_max + 1]

    for value in invalid_values:
        with pytest.raises(ValueError):
            d._set_value(value)

    # Test random generation.

    for _ in range(50):
        d._set_value_random()
        assert d.value <= d.max_val and d.value >= d.min_val

    for _ in range(50):
        d._perturb_around_locus(int((mutable_max - mutable_min)/2 + mutable_min))
        assert d.value <= d.max_val and d.value >= d.min_val

    for _ in range(50):
        d._perturb_locally()
        assert d.value <= d.max_val and d.value >= d.min_val

    
def test_bool():
    import adjsim

    d = adjsim.decision.DecisionMutableBool()

    # Test valid inputs.
    valid_values = [True, False, 1, 0, 5, -4, None, InvalidClass()]

    for value in valid_values:
        d._set_value(value)
        assert d.value == bool(value)

    for _ in range(50):
        d._set_value_random()
        assert d.value == True or d.value == False

    for _ in range(50):
        d._perturb_around_locus(False)
        assert d.value == True or d.value == False

    for _ in range(50):
        d._perturb_locally()
        assert d.value == True or d.value == False


def test_sum_constraint():
    import adjsim

    with pytest.raises(ValueError):
        adjsim.decision.PositiveSumConstraint(0)

    with pytest.raises(ValueError):
        adjsim.decision.PositiveSumConstraint(None)

range_values = [(0, 1.6), (-1.4, 0.5), (0.0, 7.0), (-7, 0.4), (300.7, 400.9), (-300.5, 400.2), (-400.5, -300.6)]
shape_values = [(5,), (5, 6), [5, 6,], (4, 7, 3, 4)]
product = itertools.product(range_values, shape_values)
items = [(e[0][0], e[0][1], e[1]) for e in product]
@pytest.mark.parametrize("mutable_min,mutable_max,shape", items)
def test_float_array_range_constraint(mutable_min, mutable_max, shape):
    import adjsim

    constraint = adjsim.decision.RangeConstraint(mutable_min, mutable_max)
    d = adjsim.decision.DecisionMutableFloatArray(shape, constraint)

    # Test parameters.
    assert d.constraint.max_val == mutable_max
    assert d.constraint.min_val == mutable_min
    assert d.shape == tuple(shape)

    # Test valid inputs.
    valid_values = [(mutable_max - mutable_min)/2 + mutable_min, mutable_min, mutable_max]

    for value in valid_values:
        d._set_value(np.zeros(shape, dtype=np.float_) + value)
        assert (d.value == np.zeros(shape, dtype=np.float_) + value).all()  

    # Test invalid inputs.
    invalid_types = [
        None, 
        InvalidClass(),
        (np.zeros(shape) + (mutable_max - mutable_min)/2 + mutable_min).astype(np.int_),
    ]
    
    for value in invalid_types:
        with pytest.raises(TypeError):
            d._set_value(value)

    invalid_values = [
        np.zeros(shape, dtype=np.float_) + mutable_min - 1, 
        np.zeros(shape, dtype=np.float_) + mutable_max + 1,
        np.zeros(np.array(shape) + 1, dtype=np.float) + (mutable_max - mutable_min)/2 + mutable_min,
    ]

    for value in invalid_values:
        with pytest.raises(ValueError):
            d._set_value(value)

    # Test random generation.

    for _ in range(50):
        d._set_value_random()
        assert (d.value <= constraint.max_val).all() and (d.value >= constraint.min_val).all()

    for _ in range(50):
        d._perturb_around_locus(np.zeros(shape, dtype=np.float_) + valid_values[0])
        assert (d.value <= constraint.max_val).all() and (d.value >= constraint.min_val).all()

    for _ in range(50):
        d._perturb_locally()
        assert (d.value <= constraint.max_val).all() and (d.value >= constraint.min_val).all()
    

sum_values = [1, -1, 5, -5, 400, -400, 7.78, -5,789]
shape_values = [(5,), (5, 6), [5, 6,], (4, 7, 3, 4)]
items = itertools.product(sum_values, shape_values)
@pytest.mark.parametrize("sum_val,shape", items)
def test_float_array_sum_constraint(sum_val, shape):
    import adjsim

    constraint = adjsim.decision.PositiveSumConstraint(sum_val)
    d = adjsim.decision.DecisionMutableFloatArray(shape, constraint)

    # Test parameters.
    assert d.constraint.sum == sum_val
    assert d.shape == tuple(shape)

    # Test valid inputs.
    num_elements = np.prod(shape)

    onehot = np.array([float(i == 0) for i in range(num_elements)]).reshape(shape)*sum_val
    uniform = np.ones(shape)*sum_val/num_elements

    valid_values = [
        onehot,
        uniform,
        np.random.dirichlet(np.ones((num_elements,))).reshape(shape)*sum_val
    ]

    for value in valid_values:
        print(sum_val, np.sum(value))
        d._set_value(value)
        assert (d.value == value).all()  

    # Test invalid inputs.
    invalid_types = [
        None, 
        InvalidClass(), 
    ]
    
    for value in invalid_types:
        with pytest.raises(TypeError):
            d._set_value(value)

    invalid_values = [
        onehot + 1,
        onehot * 3,
        onehot - 1,
        onehot / 3,
        uniform + 2,
        uniform - 2,
        np.random.dirichlet(np.ones((num_elements,))).reshape(shape)*sum_val*2,
        np.random.dirichlet(np.ones((num_elements,))).reshape(shape)*sum_val/2,
    ]

    for value in invalid_values:
        with pytest.raises(ValueError):
            d._set_value(value)

    # Test random generation.
    for _ in range(50):
        d._set_value_random()
        assert math.isclose(np.sum(d.value), sum_val)
    
    for _ in range(50):
        d._perturb_around_locus(valid_values[1])
        assert math.isclose(np.sum(d.value), sum_val)
    

range_values = [(0, 1), (-1, 0), (0, 7), (-7, 0), (300, 400), (-300, 400), (-400, -300)]
shape_values = [(5,), (5, 6), [5, 6,], (4, 7, 3, 4)]
product = itertools.product(range_values, shape_values)
items = [(e[0][0], e[0][1], e[1]) for e in product]
@pytest.mark.parametrize("mutable_min,mutable_max,shape", items)
def test_int_array_range_constraint(mutable_min, mutable_max, shape):
    import adjsim

    constraint = adjsim.decision.RangeConstraint(mutable_min, mutable_max)
    d = adjsim.decision.DecisionMutableIntArray(shape, constraint)

    # Test parameters.
    assert d.constraint.max_val == mutable_max
    assert d.constraint.min_val == mutable_min
    assert d.shape == tuple(shape)

    # Test valid inputs.
    valid_values = [(mutable_max - mutable_min)/2 + mutable_min, mutable_min, mutable_max]

    for value in valid_values:
        d._set_value(np.zeros(shape, dtype=np.int_) + int(value))
        assert (d.value == np.zeros(shape, dtype=np.int_) + int(value)).all()  

    # Test invalid inputs.
    invalid_types = [
        None, 
        InvalidClass(),
        np.zeros(shape, dtype=np.int_) + (mutable_max - mutable_min)/2 + mutable_min,
    ]
    
    for value in invalid_types:
        with pytest.raises(TypeError):
            d._set_value(value)

    invalid_values = [
        (np.zeros(shape) + mutable_min - 1).astype(np.int_), 
        (np.zeros(shape) + mutable_max + 1).astype(np.int_),
        (np.zeros(np.array(shape) + 1) + (mutable_max - mutable_min)/2 + mutable_min).astype(np.int_),
    ]

    for value in invalid_values:
        with pytest.raises(ValueError):
            d._set_value(value)

    # Test random generation.

    for _ in range(50):
        d._set_value_random()
        assert (d.value <= constraint.max_val).all() and (d.value >= constraint.min_val).all()

    for _ in range(50):
        d._perturb_around_locus(np.zeros(shape, dtype=np.int_) + int(valid_values[0]))
        assert (d.value <= constraint.max_val).all() and (d.value >= constraint.min_val).all()

    for _ in range(50):
        d._perturb_locally()
        assert (d.value <= constraint.max_val).all() and (d.value >= constraint.min_val).all()


@pytest.mark.parametrize("shape", [(5,), (5, 6), [5, 6,], (4, 7, 3, 4)])
def test_bool_array_range_constraint(shape):
    import adjsim

    d = adjsim.decision.DecisionMutableBoolArray(shape)

    # Test parameters.
    assert d.shape == tuple(shape)

    # Test valid inputs.
    valid_values = [np.zeros(shape, dtype=np.bool_), np.ones(shape, dtype=np.bool_)]

    for value in valid_values:
        d._set_value(value)
        assert (d.value == value).all()  

    # Test invalid inputs.
    invalid_types = [None, InvalidClass(), np.zeros(shape, dtype=np.int_)]
    
    for value in invalid_types:
        with pytest.raises(TypeError):
            d._set_value(value)

    invalid_values = [np.zeros(np.array(shape) + 1, dtype=np.bool_)]

    for value in invalid_values:
        with pytest.raises(ValueError):
            d._set_value(value)

    # Test random generation.

    for _ in range(50):
        d._set_value_random()
        assert np.logical_or(d.value, np.logical_not(d.value)).all() # Trivial.

    for _ in range(50):
        d._perturb_around_locus(valid_values[0])
        assert np.logical_or(d.value, np.logical_not(d.value)).all() # Trivial.

    for _ in range(50):
        d._perturb_locally()
        assert np.logical_or(d.value, np.logical_not(d.value)).all() # Trivial.