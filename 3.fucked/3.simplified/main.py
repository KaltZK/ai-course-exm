#!/usr/bin/env python
#encoding=UTF-8

import numpy as np

import layer
import nn
import funcs

network = nn.Network([
  layer.Input(1024),
  layer.Dense(2048),
  layer.Dense(2048),
  layer.Dense(2048),
  layer.Output(funcs.normalize)
], c = 1.0)

X = np.genfromtxt('fea.csv', delimiter=',')
y = np.genfromtxt('gnd.csv', delimiter=',')

X = funcs.normalize(X)
X = np.array(X, dtype = np.float64)

(num, ) = y.shape
y = y.reshape((num, 1))
y = np.array(y, dtype = np.float64)

network.fit(X, y, 10)

f = network.predict(X)

print f 