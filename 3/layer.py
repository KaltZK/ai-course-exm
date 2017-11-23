#!/usr/bin/env python
#encoding=UTF-8

import numpy as np

class Layer(object):
  def __init__(self, number):
    self.number  = number # last_m
    
  def set_input(self, dimension, out_dim):
    self.dimension = dimension  # m
    self.out_dim = out_dim
    self.W = np.zeros( (self.number, self.dimension + 1) )
  
  @staticmethod
  def loss(d, f):
    return np.sum( ( d-f ) ** 2 )

  @staticmethod
  def sigmoid(x):
    return 1 / ( 1 + np.exp(-x) )

  @classmethod
  def d_sigmoid(cls, x):
    z = np.array(cls.sigmoid(x))
    return z * (1 - z)
  
  def updateW(self, delta):
    # W_old + delta * X -> W_new
    # (number, dimension+1) + (number, 1) * (dimension+1, 1)T -> (number, dimension+1)
    # print 'updateW', 'W', self.W.shape, 'delta', delta.shape, 'last_X.T', self.last_X.T.shape
    self.W = self.W + 0.01 * np.dot( delta , self.last_X.T )
    assert(self.W.shape == (self.number, self.dimension + 1))

class PrivLayer(Layer):
  def priv(self, X):
    #   W * X -> y
    # (number, dimension+1) * (dimension+1, 1) -> (number, 1)
    assert( X.shape == (self.dimension, 1) )
    # x0 = np.repeat(1, self.number).reshape((self.number, 1)) # add beta/x0
    x0 = [[0]]
    X = np.insert(X, (0, ), x0, axis = 0)
    
    self.last_X = X
    self.last_f = self.sigmoid( np.dot( self.W , X ) )
    return self.last_f

class BackLayer(Layer):
  def back(self, next_delta, next_W):
    # d_sigmoid(f) .* FUNC?( next_W , next_delta ) -> delta
    # (number, 1) .*  FUNC?( (number_next, number+1) , (number_next, 1) ) -> (number, 1)
    (nnum, ndim) = next_W.shape
    f = self.last_f
    df = self.sigmoid(f)

    assert(df.shape == (self.number, 1))

    # delta = df * np.dot( next_W.T , next_delta )
    # delta = np.delete(delta, (0, ), axis = 0) # 强行裁剪
    # 上面的做法是错的

    # print 'back', 'df', df.shape, 'next_W', next_W.shape, 'next_delta', next_delta.shape
    _right = np.sum( next_W + next_delta , axis = 0 ).reshape(self.number + 1, 1)
    delta = df * np.delete(_right, (0, ), axis = 0)

    assert( delta.shape == (self.number, 1) )

    self.updateW(delta)
    return delta, self.W


class Input(Layer): # just do nothing
  
  def __init__(self, dimension):
    self.number = dimension

  def priv(self, X):
    dm, dmx = X.shape
    assert(dm == self.number and dmx == 1)
    return X

  def back(self, next_delta, next_W):
    return next_delta, next_W

class Output(PrivLayer): # generate delta
  def back(self, y, _):
    # (y - f) * d_sigmoid(f) -> delta
    # (number, 1) .* (number, 1) -> (number, 1) ???
    delta = np.array(y - self.last_f) * np.array(self.d_sigmoid(self.last_f))
    print 'output:back', 'W', self.W.shape, 'delta', delta.shape
    assert( delta.shape == (self.number, 1) )
    self.updateW(delta)
    return delta, self.W

class Dense(PrivLayer, BackLayer): # hidden layer
  pass