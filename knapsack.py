# Knapsack Algorithms code

import pandas as pd
import numpy as np

customer_matrix = [[0.0, 0.8, 0.0, 0.9, 1.3, 1.5, 0.0, 0.0, 0.3, 0.2, 1.0, 0.0, 0.6 ,0.4],
                 [0.2, 0.8, 0.3, 0.7, 0.5, 1.0, 1.0, 1.0, 2.0, 0.1, 0.1, 0.2, 0.2, 0.3],
                 [2.0, 0.2, 0.5, 0.1, 1.3, 0.1, 1.5, 1.8, 0.0, 0.0, 0.2, 0.3, 0.4, 0.4],
                 [0.5, 1.0, 1.5, 0.0, 0.2, 0.0, 0.8, 0.2, 0.0, 1.0, 0.0, 0.1, 0.5, 1.2]]

distance_matrix = pd.read_csv("distanceMatrix.csv", header = None)

class garage(object):
  def __init__(self, value):
    # cut the list by 2.3 tons per truck
    i = 0
    amount_car = 0
    toldis = 0
    while i < 14:
      toldis += distance_matrix[0][value[i]]
      weight = customer_matrix[0][value[i]-1]
      i += 1
      while weight <= 2.3 and i<14:
        weight += customer_matrix[0][value[i]-1]
        toldis += distance_matrix[value[i-1]][value[i]]
        i += 1
        # print("ในลูป", i)
      # toldis -= distance_matrix[value[i-1]][value[i]]
      # go back home
      # print("นอกลูป",i)
      # print(i)
      toldis += distance_matrix[value[i-1]][0]
      amount_car += 1
    self.amount = amount_car
    self.value = value
    self.total_dis = toldis

  def population(self):
    return (self.total_dis, self.amount)

def knapsack(weight):
  # Loop 500 collect in set
  # Random number list
  # cut by 2.3 tons
  # calculate the distance

  pathDict = dict() 
  #use (weight,car_amount) as key <class : 'tup'>
  #    and A SET of path() as value <class : 'set'>
  #when find new key just insert to dict,
  #    but if same (weight,amouth_car) check append it to its set  
  
  i = 1
  while i <= 500:
  # while i <= 2:
    # create number list
    X = np.random.permutation(range(1,15))
    # print(type(X))
    X = list(X)
    # cut the list by 2.3 tons per truck
  
    total, car_amount = garage(X).population()
    pathDict.setdefault((total, car_amount), set())
    # print(pathDict[(total, car_amount)])
    # pathDict[(total, car_amount)].add(tuple(X))
  
    # when found that data has append to the dict plus 1
    # try :
    dummylen = len(pathDict[(total, car_amount)])
    # except KeyError :
     # dummylen = 0
    pathDict[(total, car_amount)].add(tuple(X))
    
    if dummylen == 0:
     i += 1
    elif dummylen < len(pathDict[(total, car_amount)]):
     i += 1
    else:
     pass
    print(i)
  
  print(pathDict)
  
  # check amount of chromosome
  k=0
  for item in pathDict.values():
    k += len(item)
  print(k)
  return pathDict