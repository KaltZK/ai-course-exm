#!/usr/bin/env python
#encoding=UTF-8
import numpy as np
import funcs

class Layer(object):
  def __init__(self, n_components):
    self.dim_out = n_components

  def before_calc(self, priv_n_components, c):
    self.dim_in = priv_n_components
    self.c = c
    self.W = 0.1* np.random.randn(self.dim_in+1, self.dim_out)
  
class ForwardMixin(object):
  def forward(self, X):
    num, _dim_in = X.shape
    self.X = X
    X = np.insert(X, (0,), np.repeat(1., num).reshape(num, 1), axis=1)
    s = np.dot(X, self.W)
    f = funcs.sigmoid( s )
    self.f = f
    return f

class BackwardMixin(object):
  def backward(self, next_right):
    num, _dim_in = self.X.shape
    delta = self.f * (1. - self.f) * next_right
    pX = np.sum( self.X ) / num
    dW = self.c * delta.T * pX
    print self.W.shape, dW.shape
    W = self.W + dW.reshape((self.dim_in+1, 1))
    self.W = W
    right = np.sum(delta * W, axis = 1)
    return right

class Output(Layer, ForwardMixin):
  def __init__(self, func = np.array):
    super(Output, self).__init__(1)
    self.func = func

  def output_backward(self, d):
    # d (num, dim_out)
    # delta (num,)
    # W (dim_in, dim_out) == (dim_in ,1)
    # X (num, dim_in)     == (num, dim_in)
    #  For each delta and each X, W should be updated independently
    #  So pdW[k][i] = delta[k] * X[k][i]
    #  pdW looks like (num, dim_in)
    #  then W[j][i] += int( pdW[k][i] ) / num k=0..num
    # pX -- a number
    # right -- ()
    num, dim = d.shape
    delta = np.sum( (d - self.f) * self.f * (1. - self.f) , axis = 0)
    # pX = np.sum( self.X ) / num
    pdW = delta * self.X
    dW  = np.sum(pdW, axis=0) / num # -> (dim_in, )
    W = self.W + self.c * dW.T
    self.W = W
    print delta.shape, W.shape, 'wtf'
    right = np.sum(delta * W, axis = 1)
    return right

class Dense(Layer, ForwardMixin, BackwardMixin):
  pass

class Input(Dense):
  pass