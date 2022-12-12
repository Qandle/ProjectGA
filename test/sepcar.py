import pandas as pd
import numpy as np
import pprint as pp

customer_matrix = [[0.0, 0.8, 0.0, 0.9, 1.3, 1.5, 0.0, 0.0, 0.3, 0.2, 1.0, 0.0, 0.6 ,0.4],
                 [0.2, 0.8, 0.3, 0.7, 0.5, 1.0, 1.0, 1.0, 2.0, 0.1, 0.1, 0.2, 0.2, 0.3],
                 [2.0, 0.2, 0.5, 0.1, 1.3, 0.1, 1.5, 1.8, 0.0, 0.0, 0.2, 0.3, 0.4, 0.4],
                 [0.5, 1.0, 1.5, 0.0, 0.2, 0.0, 0.8, 0.2, 0.0, 1.0, 0.0, 0.1, 0.5, 1.2]]

distance_matrix = pd.read_csv("data/distanceMatrix.csv", header = None)


class car(object):
  def __init__(self, _value, distance_matrix):
    self.places = _value
    self.distance_matrix = distance_matrix
  def findDistance(self):
    path = [0] + self.places + [0]
    print(path,end=" ")
    distance = 0
    for i in range(1, len(path)):
      distance += self.distance_matrix[path[i-1]][path[i]]
      print("+" ,self.distance_matrix[path[i-1]][path[i]],"=", distance)
    return distance
  def __str__(self) -> str:
        return f'distance: {self.findDistance()} \n path: {self.places}'

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
      weight_arr = list(map(lambda a : customer_matrix[a-1], mock))
      if sum(weight_arr + [ customer_matrix[ value [i] - 1] ]) <= 2.3:
        mock.append(value[i])
      else:
        cars.append(mock.copy())
        mock.clear()
        mock.append(value[i])
      if i == len(value) - 1 and len(mock) > 0:
        cars.append(mock)
    amount_car = len(cars)
    car_distance = list(map(lambda a : car(a, distance_matrix).findDistance(), cars))
    toldis = sum(car_distance)
    self.amount = amount_car
    self.value = value
    self.total_dis = toldis

  def population(self):
    return (self.total_dis, self.amount, self.value)
    
b = [2, 4]
print( car(b, distance_matrix) )
# a = [9, 2, 4, 11, 14, 5, 6, 13, 10]
# a = [2, 4, 5, 9, 11, 14, 6, 13, 10]
# a = [10, 12, 3, 14, 8, 1, 7, 2, 5, 13]
testCase = 4
# print( garage(a, distance_matrix, customer_matrix[testCase-1]).population() )
