# Knapsack Algorithms code
import numpy as np

# object of path for 1 car driving
class car(object):
    def __init__(self, _value, distance_matrix):
        self.places = _value
        self.distance_matrix = distance_matrix

    # find the distance of 1 car driving
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

# object of all path must sending parcel
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

        # seperate the car when weight >= 2.3
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

        # find total distance after all cars sended
        car_distance = list(
            map(lambda a: car(a, distance_matrix).findDistance(), cars))
        toldis = sum(car_distance)

        self.amount = amount_car
        self.value = value
        self.total_dis = toldis
        self.cars = cars

    def population(self):
        return (self.total_dis, self.amount, self.value)

    def __repr__(self) -> str:
        return f'distance: {self.total_dis} | car amount: {self.amount} | path: {self.value}'

    def __str__(self) -> str:
        return f'distance: {self.total_dis} \ncar amount: {self.amount} \npath: {self.cars}'


#  generate initial generation : 500 chromosome
def init_population(distance_matrix, customer_matrix):
    pathDict = dict()

    # use (weight,car_amount) as key <class : 'tup'>
    #    and A List of path() as value <class : 'list'>
    for _ in range(500):

        # create number list
        X = np.random.permutation(range(1, 15))
        X = list(X)

        # cut the list by 2.3 tons per truck
        total, car_amount, X = garage(
            X, distance_matrix, customer_matrix).population()
        pathDict.setdefault((total, car_amount), list())
        pathDict[(total, car_amount)].append(list(X))

    return pathDict
