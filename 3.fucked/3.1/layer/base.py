#encoding=UTF-8
import numpy as np
from funcs import *

class Layer(object):
  def __init__(self, out_dim):
    self.out_dim = out_dim

  def set_input(self, in_dim, c):
    self.in_dim = in_dim
    self.c = c
  
  def before_calc(self, X):
    X_n, X_dim = X.shape
    assert(X_dim == self.in_dim)
    self.sample_num = X_n
    self.X_shape = (self.sample_num, self.in_dim)
    self.y_shape = (self.sample_num, self.out_dim)
    # self.delta_shape = (1, self.out_dim)
    self.delta_shape = self.y_shape
    self.W_shape = (self.in_dim + 1, self.out_dim)
    # self.next_delta_shape = (1, None)
    self.next_delta_shape = (self.sample_num, None)

    self.next_W_shape = (self.out_dim + 1, None)
    self.init_W()
  
  def init_W(self):
    self.W = 0.1 * np.random.randn(*self.W_shape)

  def check_shape(self, mat, shape):
    if not all( s2 is None or s1 == s2 for s1, s2 in zip(mat.shape, shape)):
      raise RuntimeError("Shape not match: got %s, expected %s"%(mat.shape, shape) )

  def updateW(self, delta):
    self.check_shape(self.W,  self.W_shape)
    self.check_shape(delta,   self.delta_shape)
    new_W = self.calc_W(self.W, delta)
    self.check_shape(new_W,   self.W_shape)
    self.W = new_W
    return new_W
  

  def calc_forward(self, X):
    self.check_shape(X, self.X_shape)
    f = self.forward(X, self.W)
    self.check_shape(f, self.y_shape)
    self.last_X = X
    self.last_f = f
    return f
  
  def calc_backward(self, next_delta, next_W):
    self.check_shape( next_delta, self.next_delta_shape )
    if next_W is not None:
      self.check_shape( next_W, self.next_W_shape )
    delta, W = self.backward(next_delta, next_W)
    self.check_shape(delta, self.delta_shape)
    self.check_shape(W, self.W_shape)
    self.delta = delta
    self.W = W
    return delta, W

  def update_delta(self, f, d, next_W):
    self.check_shape(f, self.y_shape)
    self.check_shape(d, self.next_delta_shape)
    if next_W is not None:
      self.check_shape( next_W, self.next_W_shape )
    delta = self.calc_delta(f, d, next_W)
    self.check_shape(delta, self.delta_shape)
    self.delta = delta
    return delta

  # def calc_delta(self, f, d):
  #   assert(False)

  # def forward(self, X, W):
  #   assert(False)
  
  # def backword(self, next_delta, next_W):
  #   assert(False)

  def calc_W(self, W, delta):

    # 这里是玄学
    Xhat = X2Xhat(self.last_X)
    tXs  = np.sum(Xhat.T, axis = 0).reshape(self.sample_num, 1)

    # print tXs.shape, delta.shape,'->',W.shape
    # print tXs.shape
    
    dW = np.sum(tXs * delta, axis = 0).reshape(1, self.out_dim)
    # print dW.shape,'->',W.shape

    #
    # sX = np.sum( X2Xhat(self.last_X), axis = 0 ).reshape(self.in_dim+1, 1)
    # dW = sX.T + delta
    # 
    new_W = W + self.c * dW
    return new_W