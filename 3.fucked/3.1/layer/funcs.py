import numpy as np

def loss(d, f):
  return np.sum( ( d-f ) ** 2)

def loss_p(d, f):
  n, dim = d.shape
  return np.sum( ( d-f ) ** 2, axis = n).reshape(1, dim)

def sigmoid(x):
  f = 1 / ( 1 + np.exp(-x) )
  return f

def relu(x):
  return x * (x > 0)

def d_sigmoid(x):
  z = np.array(sigmoid(x))
  return z * (1 - z)

def X2Xhat(X):
  n, dim = X.shape
  x0 = [1]
  Xhat = np.insert(X, (0, ), x0, 1)
  return Xhat

def Xhat2X(X):
  return np.delete(X, (0, ), 1)