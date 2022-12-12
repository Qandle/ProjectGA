# Genetic Algorithms code
import pprint as pp
import numpy as np
from knapsack import garage

# Elitism function : keep 5% of the population that have less distance


def elitism(pathDict):
    eliteDict = dict()
    listOfKeys = sorted(list(pathDict.keys()))

    i = 0
    for key in listOfKeys:
        if i == 30:
            break
        dummyLen = len(pathDict[key])
        i += dummyLen
        if i <= 30:
            eliteDict[key] = pathDict[key].copy()
            del pathDict[key]
        else:
            eliteDict[key] = []
            nth_item = dummyLen-(i-30)
            eliteDict[key] = pathDict[key][:nth_item].copy()
            del pathDict[key][:nth_item]
            i = 30
    return eliteDict, pathDict


def findTotalDistance(pathDict):
    total = 0
    allKey = pathDict.keys()
    for key in allKey:
        total += key[0] * len(pathDict[key])
    return total


def findTotalDistanceReverse(pathDict):
    total = findTotalDistance(pathDict)
    retotal = 0
    allKey = pathDict.keys()
    for key in allKey:
        retotal += total - (key[0] * len(pathDict[key]))
    return retotal/total

# Assign Fitness function
#  return area(fitness probability)


def hash_fitness(distance, total):
    fitProb = 1 - (distance/total)
    # print(distance, total,fitProb)
    return fitProb


def fitnessCalculator(maxDistance, curDistance):
    return 100 * (maxDistance-curDistance)/maxDistance


def findMaxDis(pathDict_470):
    maxDis = -1
    for key in pathDict_470.keys():
        if key[0] > maxDis:
            maxDis = key[0]
    return maxDis


def roulette_Selc(pathDict_470, percentCross, numPopulation):
    maxDis = findMaxDis(pathDict_470)
    numToCross = int(round(numPopulation*percentCross/100))

    # calculate fitnessValue for each gene
    all = 0
    fitList = []
    for key in pathDict_470.keys():
        length = len(list(pathDict_470[key]))
        for i in range(length):
            fitValue = fitnessCalculator(maxDis, key[0])
            all += fitValue
            fitList.append(fitValue)

    # calculate probability for each gene
    probList = []
    indexToCross = []
    num = len(fitList)
    for i in range(num):
        probList.append(fitList[i]/all)
        indexToCross.append(i)

    # random gene to crossover
    listOfIndexParent = np.random.choice(indexToCross, numToCross, p=probList)

    # get all gene
    allPath = []
    for paths in pathDict_470.values():
        for path in paths:
            allPath.append(path)

    # collect gene to crossover
    parentToCross = []
    for i in range(numToCross):
        parentToCross.append(allPath[listOfIndexParent[i]].copy())

    return parentToCross

# Crossover function
# input: parent1,
# output: 2 parent


def crossover_PMX(parent1, parent2):
    # print(parent1)
    # print(parent2)
    point1 = int(round(len(parent1)/3))
    point2 = int(round((len(parent1)/3))*2)
    # print("point",point1,point2)
    # 0 1 2 3 4 | 5 6 7 8 9 | 10 11 12 13
    temp1 = parent1.copy()
    temp2 = parent2.copy()
    # print(parent1 , parent2)
    parent1[point1:point2], parent2[point1:point2] = parent2[point1:point2], parent1[point1:point2]
    for i in range(point1, point2):
        # print (i, parent1[i],parent2[i])
        if parent1[i] in parent1[:point1] or parent1[i] in parent1[point2:]:
            index = temp1.index(parent1[i])
            # print("show",parent1[i],index)
            parent1[index] = temp1[i]
            j = index
            while (parent1[index] in parent1[point1:point2]):
                j = temp2.index(parent1[index])
                parent1[index] = temp1[j]
                # print(parent1)
                # print (temp1[i], j,temp1[j])
        if parent2[i] in parent2[:point1] or parent2[i] in parent2[point2:]:
            index = temp2.index(parent2[i])
            # print("show2",index)
            parent2[index] = temp2[i]
            j = i
            while (parent2[index] in parent2[point1:point2]):
                j = temp1.index(parent2[index])
                parent2[index] = temp2[j]
                # print (temp2[i], j,temp2[j])
    # print(parent1 , parent2)
    return parent1, parent2

# Crossover x roulette


def gen_crossover(pathDict_470, percentCross, numPopulation, distance_matrix, customer_matrix):
    parentL = roulette_Selc(pathDict_470, percentCross, numPopulation)
    newGen = dict()
    numCross = int(round(percentCross/100*numPopulation))
    for i in range(0, numCross, 2):
        parent1, parent2 = crossover_PMX(parentL[i], parentL[i+1])
        # append to keep new gen
        total, car_amount, parent1 = garage(
            parent1, distance_matrix, customer_matrix).population()
        key = (total, car_amount)
        newGen.setdefault(key, list())
        newGen[key].append(list(parent1))

        total, car_amount, parent2 = garage(
            parent2, distance_matrix, customer_matrix).population()
        key = (total, car_amount)
        newGen.setdefault(key, list())
        newGen[key].append(list(parent2))
    return newGen

# Condition function


def criteria(pathDict, gen):
    keys = []
    for key, path in dict(pathDict):
        for i in range(len(pathDict[(key, path)])):
            keys.append(key)
    # print(keys)
    sd = np.std(keys)
    # print(sd)

    # when different less than 1% (5 from 500)
    # or generation greater than 500
    #     then out of loop GA
    # else continue
    if sd <= 5 or gen > 500:
        return False
    else:
        return True


def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list

# Mutation : mutation rate 2.5%
#    swap 12 chromosone of sample after crossover


def mutation(pathDict, distance_matrix, customer_matrix, percentCross, percentMutation, numPopulation):
    numCross = percentCross/100*numPopulation
    numMutation = int(round(numCross*percentMutation/100))

    ## find gene to mutate & find key and index for deletion ##
    posGeneToMutate = np.random.choice(470, numMutation, replace=False)
    posGeneToMutate.sort()
    i = 0
    numGene = 0
    numCurSetGene = -1
    listKey = list(pathDict.keys())
    geneToMutate = []
    oldKey = (-1, -1)
    toDelete = dict()
    indexToDelete = []
    count = 0
    for item in pathDict.values():
        numCurSetGene = len(item)
        numGene += numCurSetGene
        if (count == numMutation):
            break
        while numGene >= posGeneToMutate[count] + 1:  # gene to mutate in set
            numGene -= numCurSetGene
            # target = current gene's index in this set
            target = posGeneToMutate[count] - numGene
            # collect gene and index for deletion
            geneToMutate.append(list(pathDict.values())[i][target])
            indexToDelete.append(target)
            # add to new dict for deletion
            oldKey = tuple(listKey[i])
            toDelete.setdefault(oldKey, int(0))
            toDelete[oldKey] = toDelete[oldKey] + 1
            count += 1  # next random index
            numGene += numCurSetGene  # reset to check is any gene in this set is left
            if (count == numMutation):
                break
        i += 1  # sequence of key

    ## remove in pathDict ##
    i = 0
    for key, value in toDelete.items():
        length = len(pathDict[key])
        while value != 0:
            pathDict[key].remove(geneToMutate[i])
            value -= 1
            length -= 1
            i += 1
            if (length == 0):
                del pathDict[key]

    ## mutation & add to pathDict##
    length = len(geneToMutate[0])
    for i in range(numMutation):
        toSwap = np.random.choice(length, 2, replace=False)
        geneToMutate[i] = swapPositions(geneToMutate[i], toSwap[0], toSwap[1])
        # find new key
        total, car_amount, _list = garage(
            geneToMutate[i], distance_matrix, customer_matrix).population()
        newKey = tuple([total, car_amount])
        # add newDict to pathDict
        pathDict.setdefault(newKey, list())
        pathDict[newKey].append(geneToMutate[i].copy())

# merge to firstDict


def merge(firstDict, secondDict):
    for key, value in secondDict.items():
        if key in firstDict.keys():
            for path in value:
                firstDict[key].append(path)
        else:
            firstDict.setdefault(key, list())
            for path in value:
                firstDict[key].append(path)
