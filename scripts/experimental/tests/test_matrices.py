# import packages
import numpy as np
from experimental import matrices
# generate an example matrix with uncertainty
exampleUncertain = np.array([
    [1, -1, 1, -1, -1, 0],
    [-1, 1, 1, -1, -1, 0],
    [1, 1, 1, -1, -1, 0],
    [-1, -1, -1, 1, 1, -1],
    [-1, -1, -1, 1, 1, -1],
    [0, 0, 0, -1, -1, 1]])

exampleUncertain_list = [[[0,1],[1,-1],[2,1],[3,-1],[4,-1],[5,0]],
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

def test_createAdjList():
    adj_list = matrices.createAdjList(exampleUncertain)
    assert adj_list == exampleUncertain_list

def test_checkSymmetric():
    assert matrices.checkSymmetric(exampleUncertain_list) == True

def test_checkTransitivityWeighted():
    assert matrices.checkTransitivityWeighted(exampleUncertain_list) == False


def test_genCombos():
    assert matrices.genCombos(exampleUncertain_list) == exampleCombos
