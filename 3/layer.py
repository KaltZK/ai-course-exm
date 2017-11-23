#!/usr/bin/env python
#encoding=UTF-8

import numpy as np

class Layer(object):
  def __init__(self, number):
    self.number  = number # last_m
    self.sample_number = 1
    
  def set_input(self, dimension, c):
    self.c = c
    print 'init layer', (self.number, dimension)
    self.dimension = dimension  # m
    self.W = 0.1 * np.random.randn( self.number, self.dimension + 1 )
  @staticmethod
  def loss(d, f):
    return np.sum( ( d-f ) ** 2 )

  @staticmethod
  def sigmoid(x):
    f = 1 / ( 1 + np.exp(-x) )
    return f

  @classmethod
  def d_sigmoid(cls, x):
    z = np.array(cls.sigmoid(x))
    return z * (1 - z)
  
  def updateW(self, delta):
    # W_old + delta * X -> W_new
    # (number, dimension+1) + (number, 1) * (dimension+1, 1)T -> (number, dimension+1)
    # delta_ = np.sum(delta, axis=1).reshape(1, self.number)
    delta_ = delta
    # print 'updateW', 'W', self.W.shape, 'delta', delta.shape, 'last_X.T', self.last_X.T.shape
    # print 'delta', delta_
    # print 'X', self.last_X.T
    new_W = self.W + self.c * np.dot( delta_ , self.last_X.T )
    self.W = new_W
    assert(self.W.shape == (self.number, self.dimension + 1))

class ForwardLayer(Layer):
  def forward(self, X):
    #   W * X -> y
    # (number, dimension+1) * (dimension+1, 1) -> (number, 1)
    assert( X.shape == (self.dimension, self.sample_number) )
    x0 = np.repeat(1, self.sample_number).reshape(1, self.sample_number)
    X = np.insert(X, (0, ), x0, axis = 0)
    
    self.last_X = X
    self.last_f = self.sigmoid( np.dot( self.W , X ) )
    return self.last_f

class BackwardLayer(Layer):
  def backward(self, next_delta, next_W):
    # d_sigmoid(f) .* FUNC?( next_W , next_delta ) -> delta
    # (number, 1) .*  FUNC?( (number_next, number+1) , (number_next, 1) ) -> (number, 1)
    (nnum, ndim) = next_W.shape
    f = self.last_f
    df = f * (1-f)

    assert(df.shape == (self.number, self.sample_number))

    # delta = df * np.dot( next_W.T , next_delta )
    # delta = np.delete(delta, (0, ), axis = 0) # 强行裁剪
    # 上面的做法是错的

    _right = np.array([
      np.sum( next_W + cT.T.reshape(nnum, 1) , axis = 0 ).T
      for cT in next_delta.T
    ]).T
    
    # print 'R',df
    delta = df * np.delete(_right, (0, ), axis = 0)
    # print 'Rd',delta

    assert( delta.shape == (self.number, self.sample_number) )

    self.updateW(delta)
    return delta, self.W


class Input(Layer): # just do nothing
  
  def __init__(self, dimension):
    self.number = dimension
    self.W = None

  def forward(self, X):
    dm, dmx = X.shape
    # print X.shape
    # print (self.number, self.sample_number)
    assert(dm == self.number and dmx == self.sample_number)
    return X

  def backward(self, next_delta, next_W):
    return next_delta, next_W

class Output(ForwardLayer): # generate delta
  def backward(self, y, _):
    # (y - f) * d_sigmoid(f) -> delta
    # (number, 1) .* (number, 1) -> (number, 1) ???
    delta = (y - self.last_f) * self.d_sigmoid(self.last_f)
    assert( delta.shape == (self.number, self.sample_number) )
    self.updateW(delta)
    return delta, self.W

class Dense(ForwardLayer, BackwardLayer): # hidden layer
  pass