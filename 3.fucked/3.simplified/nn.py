#!/usr/bin/env python
#encoding=UTF-8
import layer
import funcs
import numpy as np
class Network(object):
  def __init__(self, layers, c):
    self.layers = layers
    self.c = c
  
  def init_layers(self):
    for l in self.layers:
      if isinstance(l, layer.Input):
        priv_n = l.dim_out
      l.before_calc(priv_n, self.c)
      priv_n = l.dim_out
  
  def predict(self, X):
    self.init_layers()
    for k, l in enumerate(self.layers):
      # print "Fwd:", k
      X = l.forward(X)
    return X

  def fit(self, X, y, N):
    num, dim = X.shape
    pairs = zip(X, y)
    for k in xrange(N):
      f = self.predict(X)
      loss = funcs.loss(y, f)
      print '#',k,'loss=',loss / num
      self.back_propagation(X, y)
      # tloss = 0.
      # for x, z in pairs:
      #   x = np.array([x])
      #   z = np.array([z])
      #   f = self.predict(x)
      #   # print f
      #   loss = funcs.loss(z, f)
      #   # print "#", k, "loss=", loss
      #   tloss += loss
      #   self.back_propagation(x, z)
      # print "#", k, "loss=", tloss / num
  
  def back_propagation(self, X, y):
    for k, l in enumerate(reversed(self.layers)):
      # print "BP:", len(self.layers)-1-k
      if isinstance(l, layer.Output):
        next_right = l.output_backward(y)
      else:
        next_right = l.backward(next_right)