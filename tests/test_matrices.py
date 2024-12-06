"""
This file contains the tests for the matrices.py file.
The tests are written using the pytest framework.
"""

# import packages
import numpy as np
import pytest
from LeOpardLink import matrices

# generate an example matrix with uncertainty
example_non_symmetric = np.array([
    [1, 1, 1, -1, -1, 0],
    [1, 1, 1, -1, -1, 0],
    [1, 1, 1, -1, -1, -1],
    [-1, -1, -1, -1, 1, -1],
    [-1, -1, -1, 1, 1, -1],
    [-1, 0, 0, -1, -1, 1]])

example_wrong_input1 = np.array([
    [1,1,0,0],
    [1,1,0,0],
    [0,0,1,2],
    [0,0,2,1]
])

example_wrong_input2 = np.array([
    [1,1,0,0],
    [1,1,0,0],
    [0,0,1,None],
    [0,0,None,1]
])

example_wrong_input3 = np.array([
    [1,1,"N","N"],
    [1,1,"N","N"],
    ["N","N",1,-1],
    ["N","N",-1,1]
])

example_transitive_closure = np.array([
    [1, 1, 1, -1, -1, 0],
    [1, 1, 1, -1, -1, 0],
    [1, 1, 1, -1, -1, 0],
    [-1, -1, -1, 1, 1, -1],
    [-1, -1, -1, 1, 1, -1],
    [0, 0, 0, -1, -1, 1]])

example_conflict = np.array([
    [1, 1, 0, -1, -1, 0],
    [1, 1, 1, -1, -1, 0],
    [0, 1, 1, -1, -1, 0],
    [-1, -1, -1, 1, 1, -1],
    [-1, -1, -1, 1, 1, -1],
    [0, 0, 0, -1, -1, 1]])

example_not_transitive_closure = np.array([
    [1, -1, 1, -1, -1, 0],
    [-1, 1, 1, -1, -1, 0],
    [1, 1, 1, -1, -1, 0],
    [-1, -1, -1, 1, 1, -1],
    [-1, -1, -1, 1, 1, -1],
    [0, 0, 0, -1, -1, 1]])

example_not_transitive_closure_list = [[[0,1],[1,-1],[2,1],[3,-1],[4,-1],[5,0]],
                                        [[0,-1],[1,1],[2,1],[3,-1],[4,-1],[5,0]],
                                        [[0,1],[1,1],[2,1],[3,-1],[4,-1],[5,0]],
                                        [[0,-1],[1,-1],[2,-1],[3,1],[4,1],[5,-1]],
                                        [[0,-1],[1,-1],[2,-1],[3,1],[4,1],[5,-1]],
                                        [[0,0],[1,0],[2,0],[3,-1],[4,-1],[5,1]]]

# 3 possibilities for the uncertain matrix, (012,34,5),(01234,5),(012,345)
exampleCombos = [[
    [[0,1],[1,1],[2,1],[3,1],[4,1],[5,0]],
    [[0,1],[1,1],[2,1],[3,1],[4,1],[5,0]],
    [[0,1],[1,1],[2,1],[3,1],[4,1],[5,0]],
    [[0,1],[1,1],[2,1],[3,1],[4,1],[5,0]],
    [[0,1],[1,1],[2,1],[3,1],[4,1],[5,0]],
    [[0,0],[1,0],[2,0],[3,0],[4,0],[5,1]]],

    [
    [[0,1],[1,1],[2,1],[3,0],[4,0],[5,0]],
    [[0,1],[1,1],[2,1],[3,0],[4,0],[5,0]],
    [[0,1],[1,1],[2,1],[3,0],[4,0],[5,0]],
    [[0,0],[1,0],[2,0],[3,1],[4,1],[5,0]],
    [[0,0],[1,0],[2,0],[3,1],[4,1],[5,0]],
    [[0,0],[1,0],[2,0],[3,0],[4,0],[5,1]]],

    [
    [[0,1],[1,1],[2,1],[3,0],[4,0],[5,0]],
    [[0,1],[1,1],[2,1],[3,0],[4,0],[5,0]],
    [[0,1],[1,1],[2,1],[3,0],[4,0],[5,0]],
    [[0,0],[1,0],[2,0],[3,1],[4,1],[5,1]],
    [[0,0],[1,0],[2,0],[3,1],[4,1],[5,1]],
    [[0,0],[1,0],[2,0],[3,1],[4,1],[5,1]]],
    ]

def test_check_input():
    """Test the check_input function"""
    with pytest.raises(ValueError):
        matrices.check_input(example_wrong_input1)
        matrices.check_input(example_wrong_input2)
        matrices.check_input(example_wrong_input3)


def test_create_adjlist():
    """Test the create_adjlist function"""
    adj_list = matrices.create_adjlist(example_not_transitive_closure)
    assert adj_list == example_not_transitive_closure_list

def test_check_symmetric_t():
    """Test the check_symmetric function"""
    assert matrices.check_symmetric(example_not_transitive_closure_list) is True

def test_check_symmetric_f():
    """Test the check_symmetric function"""
    with pytest.raises(ValueError):
        matrices.check_symmetric(matrices.create_adjlist(example_non_symmetric))

def test_check_transitivity_weighted():
    """Test the check_transitivity_weighted function"""
    assert matrices.check_transitivity_weighted(example_not_transitive_closure_list) is False

def test_detect_conflicts():
    """Test the detect_conflicts function"""
    assert matrices.detect_conflicts(matrices.create_adjlist(example_transitive_closure)) is True
    with pytest.raises(ValueError):
        matrices.detect_conflicts(matrices.create_adjlist(example_conflict))

def test_strict_transitive_closure():
    """Test the strict_transitive_closure function"""
    assert np.array_equal(matrices.strict_transitive_closure(
        example_not_transitive_closure), example_transitive_closure)

def test_generate_graphs_with_transitivity():
    """Test the generate_graphs_with_transitivity function"""
    assert len(matrices.generate_graphs_with_transitivity(
        matrices.create_adjlist(example_transitive_closure))) == 3
