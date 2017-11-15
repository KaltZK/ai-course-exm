#!/usr/bin/env python
#encoding=UTF-8
import random
import itertools
class Evolution(object):
  def __init__(self, 
    pop_size, 
    scale,
    alpha, 
    crossover_rate,
    mutate_rate,
    graph):

    self.pop_size = pop_size
    self.scale    = scale
    self.graph    = graph
    self.alpha    = alpha
    self.generation_index = 0
    self.crossover_rate = crossover_rate
    self.mutate_rate = mutate_rate
    self.crossover_record = dict()
    self.mutate_record = set()
    
    # 如果我没理解错的话这里的eval_v只取决于排名而不是具体距离
    self.eval_v = [ self.alpha*(1-self.alpha) ** i for i in xrange(self.pop_size)]
    evs = sum(self.eval_v)
    # 所以需要归一化？
    self.eval_v = [v / evs for v in self.eval_v]

    self.individuals = [
      # [ random.randint(0, scale-1) for _j in xrange(scale) ]
      range(scale)
      for _i in xrange(pop_size)
    ]
    for vec in self.individuals:
      random.shuffle(vec)
    self.individuals.sort(key = graph.get_distance)
  
  def choice(self):
    r = random.random()
    for i in xrange(self.pop_size):
      r -= self.eval_v[i]
      if r <= 0:
        return i

  def select(self):
    # self.individuals.sort(key = self.graph.get_distance)
    next_generation = [
      list(self.individuals[ self.choice() ])
      for _ in xrange(self.pop_size)
    ]
    self.individuals = next_generation

  def crossover(self):
    for vi1, vec1 in enumerate(self.individuals):
      for vi2, vec2 in enumerate(self.individuals):
        if vi1 == vi2 or random.random() >= self.crossover_rate:
          continue
        bp = random.randint(0, self.scale-1)
        ep = self.scale
        sv1 = vec1[bp: ep]
        sv2 = vec2[bp: ep]
        map1= dict(zip(sv2, sv1))
        map2= dict(zip(sv1, sv2))
        vec1[bp: ep], vec2[bp: ep] = sv2, sv1
        for i in itertools.chain(xrange(0, bp), xrange(ep, self.scale)):
          for v, m in [(vec1, map1), (vec2, map2)]:
            p = v[i]
            while p in m:
              p = m[p]
            v[i] = p
        self.record_crossover(vi1, vi2)
        self.record_crossover(vi2, vi1)

  def record_crossover(self, f, t):
    if f in self.crossover_record:
      self.crossover_record[f].add(t)
    else:
      self.crossover_record[f] = set([t])

  def mutate(self):
    for k, vec in enumerate(self.individuals):
      if random.random() >= self.mutate_rate:
        continue
      p1 = random.randint(0, self.scale-1)
      p2 = random.randint(0, self.scale-1)
      vec[p1], vec[p2] = vec[p2], vec[p1]
      self.record_mutate(k)
  
  def record_mutate(self, i):
    self.mutate_record.add(i)

  def next(self):
    self.crossover_record = dict()
    self.mutate_record = set()

    self.select()
    self.crossover()
    self.mutate()
    
    self.individuals.sort(key = self.graph.get_distance)
    self.generation_index += 1
    return self.individuals
  
  def display(self, path = True, mutate = True, crossover = True):
    print "Generation", self.generation_index
    for i, vec in enumerate(self.individuals):
      print i, ":",
      if path:
        for j, v in enumerate(vec):
          print v, '->',
        print vec[0],
      print '# Distance =', self.graph.get_distance(vec),
      if mutate and i in self.mutate_record:
        print '!!Mutated!!',
      if crossover and i in self.crossover_record:
        print '@ Crossover with: [', ', '.join(map(str, self.crossover_record[i])),']',
      print
    print