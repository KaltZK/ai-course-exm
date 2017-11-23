#!/usr/bin/env python
#encoding=UTF-8
import numpy as np
import layer
class Network(object):
  def __init__(self, layers):
    
    self.layers = layers

    for l in self.layers:
      if isinstance(l, layer.Input):
        dim = l.number
      else:
        l.set_input(dim)

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
    Xs = np.array(Xs)
    ys = np.array(ys)
    xnum, xdim = Xs.shape
    ynum, ydim = ys.shape
    # ys = ys.reshape((num, 1))
    for i in xrange(times):
      total_loss = 0
      for X, y in zip(Xs, ys):
        f = self.exec_x(X)
        loss = layer.Layer.loss(y, f)
        # print '#',i, 'loss=', loss
        total_loss += loss
        self.back_propagation(f)
      print '#', i, 'loss=', total_loss/num

  def back_propagation(self, f):
    delta, W = np.array(f), None
    for l in reversed(self.layers):
      delta, W = l.back(delta, W)