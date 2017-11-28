import numpy as np
from base import Layer
from forward import Forward

class Output(Layer, Forward): # generate delta
  def backward(self, y, _):
    delta = self.update_delta(self.last_f, y, None)
    W = self.updateW(delta)
    return delta, W
  
  def calc_delta(self, f, d, _):
    delta = (d-f) * f *(1-f)
    print 'calc_delta', d.shape, f.shape, delta.shape
    return delta