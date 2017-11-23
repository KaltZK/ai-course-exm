#!/usr/bin/env python
#encoding=UTF-8
import decimal
import numpy as np
import layer
class Network(object):
  def __init__(self, layers, c = 1.0):
    self.c = c    
    self.layers = layers

    for l in self.layers:
      if not isinstance(l, layer.Input):
        assert(isinstance(dim, int))
        l.set_input(dim, c)
      dim = l.number
    
    self.each_bp_func = None


  def exec_X(self, X):
    X = X.T
    for l in self.layers:
      X = l.forward(X)
    return X

  def run(self, Xs):
    return self.exec_X(Xs)
    # return np.array(map(self.exec_x, np.array(Xs)))

  def train(self, Xs, ys, times):
    Xs = np.array(np.copy(Xs))
    ys = np.array(ys)
    xnum, xdim = Xs.shape
    ynum, ydim = ys.shape
    assert(xnum == ynum)
    for l in self.layers:
      l.sample_number = xnum

    y = ys.T
    
    if self.each_bp_func is not None:
        self.each_bp_func()
    for i in xrange(times):
      f = self.exec_X(Xs)
      # print f, y
      loss = layer.Layer.loss(y, f)
      print '#',i, 'loss=', loss
      self.back_propagation(y)
      if self.each_bp_func is not None:
        self.each_bp_func()

  def on_each_bp(self, func):
    self.each_bp_func = func

  def back_propagation(self, d):
    delta, W = d, None
    for l in reversed(self.layers):
      delta, W = l.backward(delta, W)