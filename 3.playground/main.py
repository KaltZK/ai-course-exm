#!/usr/bin/env python
#encoding=UTF-8

#!/usr/bin/env python
#encoding=UTF-8

import numpy as np
import nn

X = np.genfromtxt('data/train/fea.csv', delimiter=',')
y = np.genfromtxt('data/train/gnd.csv', delimiter=',')

# X = nn.normalize(X)

(num, ) = y.shape
y = y.reshape((num, 1))

syn = nn.init_w([1024, 1024, 1024, 1024, 512, 256, 128, 64, 32, 16, 1])
nn.fit(X, y, syn, 200, 0.1)

print "Test"

txX = np.genfromtxt('data/test/fea.csv', delimiter=',')
txy = np.genfromtxt('data/test/gnd.csv', delimiter=',')

print "Predict"
print nn.predict(txX, syn)

print "y"
print txy