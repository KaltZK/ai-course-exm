import numpy as np
from layer import Input
import layer
class Network(object):
  def __init__(self, layers, c = 1.0):
    self.layers = layers

    for l in layers:
      if isinstance(l, Input):
        last_dim = l.out_dim
      l.set_input(last_dim, c)
      last_dim = l.out_dim


  def run(self, X):
    for l in self.layers:
      l.before_calc(X)
    for k, l in enumerate(self.layers):
      print 'forward:', k
      X = l.calc_forward(X)
    return X
  
  def train(self, X, y, times):
    for l in self.layers:
      l.before_calc(X)
    for i in xrange(times):
      f = self.run(X)
      loss = layer.loss(f, y)
      print '#', i, "loss =", loss
      self.back_propagation(y)

  
  def back_propagation(self, d):
    n, dim = d.shape
    delta = d
    # delta = np.sum(d, axis = 0).reshape(1, dim) / n
    W = None
    for k, l in enumerate(reversed(self.layers)):
      print 'backward:', len(self.layers) - 1 - k
      delta, W = l.calc_backward(delta, W)