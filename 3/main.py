#!/usr/bin/env python
#encoding=UTF-8
import numpy as np

import layer
import nn

network = nn.Network([
  layer.Input(1024),
  layer.Dense(1024),
  layer.Dense(1024),
  layer.Output(40)
])

X = np.genfromtxt('fea.csv', delimiter=',')
y = np.genfromtxt('gnd.csv', delimiter=',')

Ys = np.zeros((len(y), 40))
for label, v in zip(y, Ys):
  v[int(label) - 1] = 1.0

network.train(X, Ys, 20)

print(network.run(X))