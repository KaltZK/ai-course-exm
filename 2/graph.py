#!/usr/bin/env python
#encoding=UTF-8

class Graph(object):
  INFINITY = float('inf')
  def __init__(self, v_num, symmetrical = True):
    self.v_num = v_num
    self.edges = dict()
    self.symmetrical = symmetrical
  
  def __getitem__(self, pair):
    if self.symmetrical:
      f = min(pair)
      t = max(pair)
    else:
      f, t = pair
    
    if (f, t) in self.edges:
      return self.edges[f, t]
    else:
      return self.INFINITY
  
  def __setitem__(self, pair, val):
    if self.symmetrical:
      f = min(pair)
      t = max(pair)
    else:
      f, t = pair
    self.edges[f, t] = val
    return val

  def get_distance(self, path):
    dist = self[ path[-1], path[0] ]
    for i in xrange(1, len(path)):
      ed = self[ path[i-1], path[i] ]
      dist += ed
      if dist == self.INFINITY:
        return self.INFINITY
    return dist
  
  def get_edges_on_path(self, path):
    edges = []
    for i in xrange(1, len(path)):
      dist = self[ path[i-1], path[i] ]
      if dist < self.INFINITY:
        edges.append(( path[i-1], path[i], dist ))
    return edges