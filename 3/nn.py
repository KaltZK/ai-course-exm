#!/usr/bin/env python
#encoding=UTF-8
import numpy as np
import layer
class Network(object):
  def __init__(self, number, layers):
    self.number = number
    self.layers = layers
  
  def init(number, dimension):
    for l in self.layers:
      if isinstance(l, layer.Input):
        l.set_shape(dimension, number)
      elif isinstance(l, layer.Output):
        l.set_shape(dimension, 1)
      else:
        

  def run(self, X):
    for l in self.layers:
      y = l.priv(X)
      X = np.repeat(y, self.number).reshape(self.number, self.number).T
      print X.shape
    return X

  def train(self, X, y, times):
    for i in xrange(times):
      f = self.run(X)
      loss = layer.Layer.loss(y, f)
      print '#',i, 'loss=', loss
      self.back_propagation(f)

  def back_propagation(self, f):
    delta, W = np.array(f), None
    for l in reversed(self.layers):
      delta, W = l.back(delta, W)