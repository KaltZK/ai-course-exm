#!/usr/bin/env python
#encoding=UTF-8

import numpy as np

class Layer(object):
  def set_shape(dimension, number):
    self.number  = number # last_m
    self.dimension = dimension  # m
    self.W = np.zeros( (number, dimension + 1) )
  
  def updateW(self, delta):
    self.W = self.W +  self.last_X.T * delta
  
  @staticmethod
  def loss(d, f):
    return np.sum( ( d-f ) ** 2 )

  @staticmethod
  def sigmoid(x):
    return 1 / ( 1 + np.exp(-x) )

  @classmethod
  def d_sigmoid(cls, x):
    return cls.sigmoid(x) * (1 - sigmoid(x))

class PrivLayer(Layer):
  def priv(self, X):
    (num, dm) = X.shape
    assert(num == self.number)
    assert(dm == self.dimension)
    x0 = np.repeat(1, self.number).reshape((self.number, 1)) # add beta/x0
    X = np.insert(X, (0, ), x0, axis = 1)
    self.last_X = X
    y = np.sum( self.sigmoid(X * self.W), axis = 1)
    self.last_f = y
    return y

class BackLayer(Layer):
  def back(self, next_delta, next_W): # next_delta: array(n, 1), next_W: (n, m)
    (nnum, ndim) = next_W.shape
    print next_delta.shape, next_W.shape
    delta = self.last_f * (1 - self.last_f) *  (next_delta * next_W)
    self.updateW(delta)
    return delta, self.W


class Input(BackLayer): # just do nothing
  def __init__(self, dimension):
    self.dimension = dimension

  def priv(self, X):
    (num, dm) = X.shape
    assert(num == self.number)
    assert(dm == self.dimension)
    x0 = np.repeat(1, self.number).reshape((self.number, 1)) # add beta/x0
    X = np.insert(X, (0, ), x0, axis = 1)
    self.last_X = X
    y = np.sum( self.sigmoid(X * self.W), axis = 1)
    self.last_f = y
    return y

class Output(PrivLayer): # generate delta
  def back(self, y, _): # y: array
    delta = (y - self.last_f) * self.last_f * (1 - self.last_f) 
    self.updateW(delta)
    return delta, self.W

class Dense(PrivLayer, BackLayer): # hidden layer
  pass