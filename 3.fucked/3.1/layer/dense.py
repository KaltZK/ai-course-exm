import numpy as np
from base import Layer
from forward import Forward
from backward import Backward

class Dense(Layer, Forward, Backward):
  pass