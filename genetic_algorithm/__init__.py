import numpy as np
import pandas as pd
import pprint as pp
import math
import time
from genetic import *
from knapsack import init_population as ip

start = time.time()


CUSTOMER_MATRIX = [
    [0.0, 0.8, 0.0, 0.9, 1.3, 1.5, 0.0, 0.0, 0.3, 0.2, 1.0, 0.0, 0.6, 0.4],
    [0.2, 0.8, 0.3, 0.7, 0.5, 1.0, 1.0, 1.0, 2.0, 0.1, 0.1, 0.2, 0.2, 0.3],
    [2.0, 0.2, 0.5, 0.1, 1.3, 0.1, 1.5, 1.8, 0.0, 0.0, 0.2, 0.3, 0.4, 0.4],
    [0.5, 1.0, 1.5, 0.0, 0.2, 0.0, 0.8, 0.2, 0.0, 1.0, 0.0, 0.1, 0.5, 1.2]
]

DISTANCE_MATRIX = pd.read_csv("./data/distanceMatrix.csv", header=None)

if __name__ == '__main__':
    # save best gene(may > 1) for each testCase
    ans = []
    i = 0
    for j in range(10):
        gen = 1
        init_pop_500 = ip(DISTANCE_MATRIX, CUSTOMER_MATRIX[i])
        genX = init_pop_500
        print(f"gen: {gen} round: {j+1}")

        gen = 2
        while (criteria(genX, gen)):
            print(f"gen: {gen} round: {j+1}")
            eliteDict, pathDict = elitism(genX)
            newGen = gen_crossover(pathDict, 94, 500, DISTANCE_MATRIX,
                                   CUSTOMER_MATRIX[i])
            mutation(newGen, DISTANCE_MATRIX, CUSTOMER_MATRIX[i], 94, 2.5, 500)
            merge(newGen, eliteDict)
            genX = newGen
            gen += 1

        # save best gene(may > 1) for each round
        dummy = dict()
        minDis = math.inf
        numCar = math.inf
        minPath = []
        for key, value in genX.items():
            if minDis > key[0]:
                minDis = key[0]
                numCar = key[1]
                minPath = genX[key]
        key = (minDis, numCar)
        dummy[key] = minPath
        ans.append(dummy.copy())

    # save best gene(may > 1) for each round
    for k in range(10):
        print("best for round:", k+1, "testCase:", i+1)
        pp.pprint(ans[k])

    end = time.time()
    print("time used:", format((end - start), '.4f'))
