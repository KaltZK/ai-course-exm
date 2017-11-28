import numpy as np
from base import Layer

class Backward(object):
  def backward(self, next_delta, next_W):
    delta = self.update_delta(self.last_f, next_delta, next_W)
    W = self.updateW(delta)
    return delta, W

  def calc_delta(self, f, next_delta, nW_hat):
    # next_delta[i, j] 第 i 个样本 第 j 维 的偏差    (sample_num, next_out_dim)
    # f[i, j] 第 i 个样本 第 j 维 的结果(估计)        (sample_num, out_dim)
    # nW[i, j] 第 j 个神经元在第 i 维的权值           (in_dim, out_dim)
    # delta[i, j] 第 i 个样本 第 j 维 的偏差         (sample_num, out_dim)
    nW = np.delete(nW_hat, (0, ), 0)
    nW_sum = np.sum(nW, axis=0) 
    nD_sum = np.sum(next_delta, axis=0)
    print nW.shape, next_delta.shape, f.shape
    right = np.sum(nW + d, axis=0).T
    delta = f * (1-f) * right
    return delta