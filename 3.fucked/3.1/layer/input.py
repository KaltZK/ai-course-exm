import numpy as np
from base import Layer
class Input(Layer): # just do nothing

  def calc_forward(self, X):
    return X

  def backward(self, next_delta, next_W):
    pass