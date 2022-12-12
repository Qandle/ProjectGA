# Knapsack Algorithms code
# import pandas as pd
import numpy as np
# import pprint as pp


class car(object):
    def __init__(self, _value, distance_matrix):
        self.places = _value
        self.distance_matrix = distance_matrix

    def findDistance(self):
        path = [0] + self.places + [0]
        distance = 0
        for i in range(1, len(path)):
            distance += self.distance_matrix[path[i-1]][path[i]]
        return distance

    def __repr__(self) -> str:
        return f'distance: {self.findDistance()} | path: {self.places}'

    def __str__(self) -> str:
        return f'distance: {self.findDistance()} \npath: {self.places}'


class garage(object):
    def __init__(self, _value, distance_matrix, customer_matrix):
        value = list()
        for a in _value:
            if customer_matrix[a-1] != 0:
                value.append(a)
        amount_car = 0
        toldis = 0
        cars = []
        mock = []
        for i in range(len(value)):
            weight_arr = list(map(lambda a: customer_matrix[a-1], mock))
            if sum(weight_arr + [customer_matrix[value[i] - 1]]) <= 2.3:
                mock.append(value[i])
            else:
                cars.append(mock.copy())
                mock.clear()
                mock.append(value[i])
            if i == len(value) - 1 and len(mock) > 0:
                cars.append(mock)
        amount_car = len(cars)
        car_distance = list(
            map(lambda a: car(a, distance_matrix).findDistance(), cars))
        toldis = sum(car_distance)
        self.amount = amount_car
        self.value = value
        self.total_dis = toldis

    def population(self):
        return (self.total_dis, self.amount, self.value)

    def __repr__(self) -> str:
        return f'distance: {self.total_dis} | car amount: {self.amount} | path: {self.value}'

    def __str__(self) -> str:
        return f'distance: {self.total_dis} \n car amount: {self.amount} \n path: {self.value}'


def init_population(distance_matrix, customer_matrix):
    # Loop 500 collect in set
    # Random number list
    # cut by 2.3 tons
    # calculate the distance

    pathDict = dict()
    # use (weight,car_amount) as key <class : 'tup'>
    #    and A SET of path() as value <class : 'set'>
    # when find new key just insert to dict,
    #    but if same (weight,amouth_car) check append it to its set

    # i = 1
    # while i <= 500:
    for _ in range(500):
        # while i <= 2:
        # create number list
        X = np.random.permutation(range(1, 15))
        # print(type(X))
        X = list(X)
        # print(X)
        # cut the list by 2.3 tons per truck

        total, car_amount, X = garage(
            X, distance_matrix, customer_matrix).population()
        pathDict.setdefault((total, car_amount), list())
        # print(pathDict[(total, car_amount)])
        # pathDict[(total, car_amount)].add(tuple(X))

        # when found that data has append to the dict plus 1
        # try :
        #dummylen = len(pathDict[(total, car_amount)])
        # except KeyError :
        # dummylen = 0

        pathDict[(total, car_amount)].append(list(X))

        # if dummylen == 0:
        #  i += 1
        # elif dummylen < len(pathDict[(total, car_amount)]):
        #  i += 1
        # else:
        #  pass
        # print(i)

    # pp.pprint(pathDict)
    # print(pathDict)
    # pd.DataFrame.from_dict(pathDict)

    # check amount of chromosome
    # k=0
    # for item in pathDict.values():
    #   k += len(item)
    # print(k)
    return pathDict
