import pandas as pd
import pprint as pp
import math
import time
from genetic import *
from knapsack import init_population as ip

start = time.time()


CUSTOMER_MATRIX = pd.read_csv("./data/customer_matrix.csv", header=None).T
DISTANCE_MATRIX = pd.read_csv("./data/distance_matrix.csv", header=None)
FILENAME = "testCase"
TESTCASE = 2

if __name__ == '__main__':
    # collect best chromosome(may > 1) for each testCase
    ans = []
    i = 0
    for j in range(10):
        gen = 1
        init_pop_500 = ip(DISTANCE_MATRIX, CUSTOMER_MATRIX[i])
        genX = init_pop_500
        with open(f'./test/example/{FILENAME}{TESTCASE}.txt', "a") as out:
            out.write(f'gen: {gen} round: {j+1}\n')
            pp.pprint(genX, stream=out)
        with open(f'./test/example/{FILENAME}{TESTCASE}.log', "a") as out:
            out.write(f'gen: {gen} round: {j+1}\n')
            pp.pprint(genX, stream=out)


        gen = 2
        while (criteria(genX, gen)):
            eliteDict, pathDict = elitism(genX)
            newGen = gen_crossover(pathDict, 94, 500, DISTANCE_MATRIX,
                                   CUSTOMER_MATRIX[i])
            mutation(newGen, DISTANCE_MATRIX, CUSTOMER_MATRIX[i], 94, 2.5, 500)
            merge(newGen, eliteDict)
            genX = newGen
            if gen == 250 or gen == 500:
                with open(f'./test/example/{FILENAME}{TESTCASE}.txt', "a") as out:
                    out.write(f'gen: {gen} round: {j+1}\n')
                    pp.pprint(genX, stream=out)
                with open(f'./test/example/{FILENAME}{TESTCASE}.log', "a") as out:
                    out.write(f'gen: {gen} round: {j+1}\n')
                    pp.pprint(genX, stream=out)
            gen += 1

        # save best chromosome(may > 1) for each round
        dummy = dict()
        minDis = math.inf
        numCar = math.inf
        minPath = []
        for key, value in genX.items():
            if minDis > key[0] or (minDis == key[0] and numCar > key[1]) :
                minDis = key[0]
                numCar = key[1]
                minPath = genX[key]
        key = (minDis, numCar)
        dummy[key] = minPath
        ans.append(dummy.copy())

    # save best chromosome(may > 1) for each round
    for k in range(10):
        print("best for round:", k+1, "testCase:", i+1)
        pp.pprint(ans[k])

    end = time.time()
    print("time used:", format((end - start), '.4f'))
