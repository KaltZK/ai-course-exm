#!/usr/bin/env python
#encoding=UTF-8
import numpy as np
import itertools

def init_w(nodes):
  shapes = zip(nodes[:-1], nodes[1:])
  return [2*np.random.random(s) - 1 for s in shapes]

def sigmoid(s):
  return 1/(1+np.exp(-s))

def loss(f, d):
  return np.sum((f-d)**2)

def normalize(x):
  return (x - np.min(x)) / (np.max(x) - np.min(x))

syn = init_w([3, 4, 8, 1])

def predict_(X, syn):
  xs = []
  fs = []
  for w in syn:
    xs.append(X)
    X = sigmoid(np.dot(X, w))
    fs.append(X)
  return xs, fs

def predict(X, syn):
  xs, fs = predict_(X, syn)
  return fs[-1]

def fit(X, y, syn, times, c = 1.0):
  for j in xrange(times):
    inputs, outputs = predict_(X, syn)
    delta = (y-outputs[-1]) * ( (outputs[-1]*(1-outputs[-1])) )
    syn[-1] += inputs[-1].T.dot(delta)
    bp_group = enumerate(reversed(zip( 
      syn[1:],
      syn[:-1],
      inputs[:-1], 
      outputs[:-1]
    )))
    for k, (next_w, w, v_in, v_out) in bp_group:
      ix = len(syn) - k - 2
      delta = delta.dot(next_w.T) * (v_out * (1-v_out))
      dW = v_in.T.dot(delta)
      syn[ix] = w + c*dW
    f = outputs[-1]
    print '#', j, 'loss=', loss(f, y)
    print f