#!/usr/bin/env python
#encoding=UTF-8
import numpy as np

def normalize(X):
  mi = np.min(X)
  mx = np.max(X)
  return (X - mi) / (mx - mi)

def sigmoid(X):
  return 1. / ( 1 + np.exp(-X) )

def loss(d, f):
  return np.sum( (d-f) ** 2 )