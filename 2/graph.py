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
    dist = 0
    if not self.valid_loop(path):
      return self.INFINITY
    for i in xrange(1, len(path)):
      ed = self[ path[i-1], path[i] ]
      if ed == self.INFINITY:
        return self.INFINITY
      else:
        dist += ed
    return dist

  def valid_loop(self, path):
    mark = [False] * self.v_num
    if path[0] != path[-1]:
      return False
    # print path
    for v in path:
      mark[v] = True
    return all(mark)
  
  def get_edges_on_path(self, path):
    edges = []
    for i in xrange(1, len(path)):
      dist = self[ path[i-1], path[i] ]
      if dist < self.INFINITY:
        edges.append(( path[i-1], path[i], dist ))
    return edges