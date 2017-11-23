#!/usr/bin/env python
#encoding=UTF-8
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

  def exec_x(self, X):
    (n, ) = X.shape
    X = X.reshape(n, 1)
    for l in self.layers:
      X = l.priv(X)
    X = np.array(X).reshape( ( l.number, ) )
    return X

  def run(self, Xs):
    return np.array(map(self.exec_x, np.array(Xs)))

  def train(self, Xs, ys, times):
    Xs = np.copy(Xs)
    ys = np.array(ys)
    xnum, xdim = Xs.shape
    ynum, ydim = ys.shape
    assert(xnum == ynum)
    # _result = [None] * ynum
    # ys = ys.reshape((num, 1))
    for i in xrange(times):
      total_loss = 0
      pairs = zip(Xs, ys)
      np.random.shuffle(pairs)
      for j, (X, y) in enumerate(pairs):
        y = y.reshape(ydim, 1)
        f = self.exec_x(X)
        # print f, y
        loss = layer.Layer.loss(y, f)
        # print '#',i, 'loss=', loss
        total_loss += loss
        self.back_propagation(y)
        # if self.each_bp_func is not None:
        #   _result[j] = f
      if self.each_bp_func is not None:
        self.each_bp_func()
          # self.each_bp_func(_result)
          # _result = [None] * ynum
      print '#', i, 'loss=', total_loss/ynum

  def on_each_bp(self, func):
    self.each_bp_func = func

  def back_propagation(self, d):
    delta, W = d, None
    for l in reversed(self.layers):
      delta, W = l.back(delta, W)