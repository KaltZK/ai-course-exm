#!/usr/bin/env python
#encoding=UTF-8

import numpy as np

import layer
import nn

network = nn.Network([
  layer.Input(1024),
  layer.Dense(1024),
  layer.Output(40)
], c = 1.0)

X = np.genfromtxt('fea.csv', delimiter=',')
y = np.genfromtxt('gnd.csv', delimiter=',')


Xs = (X - np.min(X))  / (np.max(X) - np.min(X))
Ys = np.zeros((len(y), 40))

for label, v in zip(y, Ys):
  v[int(label) - 1] = 1.0

network.train(Xs, Ys, 20)

f = network.run(Xs)
pre_y = [
  max(enumerate(y),key=lambda (i, z): z)[0]
  for y in f
]

print(pre_y)