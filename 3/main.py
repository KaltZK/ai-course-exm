#!/usr/bin/env python
#encoding=UTF-8
import numpy as np

import layer
import nn

network = nn.Network(400, [
  layer.Input(),
  layer.Dense(),
  # layer.Dense(),
  layer.Output()
])

X = np.genfromtxt('fea.csv', delimiter=',')
y = np.genfromtxt('gnd.csv', delimiter=',')

# network.train(X, y, 10)

print(network.run(X))