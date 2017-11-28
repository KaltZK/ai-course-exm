#!/usr/bin/env python
#encoding=UTF-8
import numpy as np

import sklearn.datasets

import layer
import nn

digits = sklearn.datasets.load_digits()

Xs = np.array([i.reshape((64, )) / 255 for i in digits.images])
y = digits.target

Ys = np.zeros((len(y), 10))

for label, v in zip(y, Ys):
  v[int(label) - 1] = 1.0


network = nn.Network([
  layer.Input(64),
  layer.Dense(1024),
  # layer.Dense(1024),
  # layer.Dense(1024),
  # layer.Dense(1024),
  # layer.Dense(1024),
  # layer.Dense(1024),
  # layer.Dense(1024),
  # layer.Dense(1024),
  layer.Output(10)
], c = 1.0)

network.train(Xs, Ys, 20)
f = network.run(Xs)
pre_y = [
  max(enumerate(y),key=lambda (i, z): z)[0]
  for y in f
]

print(pre_y)