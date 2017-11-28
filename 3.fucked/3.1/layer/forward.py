import numpy as np
from funcs import *

class Forward(object):
  def forward(self, X, W):
    X_hat = X2Xhat(X)
    return sigmoid(np.dot(X_hat, W))