# import packages
import numpy as np
from LeOpardLink import matrices
import pytest
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

def test_checkInput():
    with pytest.raises(ValueError):
        matrices.checkInput(example_wrong_input1)
        matrices.checkInput(example_wrong_input2)
        matrices.checkInput(example_wrong_input3)


def test_createAdjList():
    adj_list = matrices.createAdjList(example_not_transitive_closure)
    assert adj_list == example_not_transitive_closure_list

def test_checkSymmetricT():
    assert matrices.checkSymmetric(example_not_transitive_closure_list) == True

def test_checkSymmetricF():
    with pytest.raises(ValueError):
        matrices.checkSymmetric(matrices.createAdjList(example_non_symmetric))

def test_checkTransitivityWeighted():
    assert matrices.checkTransitivityWeighted(example_not_transitive_closure_list) == False

def test_detect_conflicts():
    assert matrices.detect_conflicts(matrices.createAdjList(example_transitive_closure)) == True
    with pytest.raises(ValueError):
        matrices.detect_conflicts(matrices.createAdjList(example_conflict))

def test_strictTransitiveClosure():
    assert np.array_equal(matrices.strictTransitiveClosure(example_not_transitive_closure), example_transitive_closure)

def test_generateGraphsWithTransitivity():
    assert len(matrices.generateGraphsWithTransitivity(matrices.createAdjList(example_transitive_closure))) == 3