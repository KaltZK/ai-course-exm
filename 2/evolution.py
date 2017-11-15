#!/usr/bin/env python
#encoding=UTF-8
import random
class Evolution(object):
  def __init__(self, 
    pop_size, 
    scale,
    value_range,
    alpha, 
    exchange_rate,
    mutate_rate,
    mutate_range,
    graph):

    self.pop_size = pop_size
    self.scale    = scale
    self.graph    = graph
    self.alpha    = alpha
    self.generation_index = 0
    self.exchange_rate = exchange_rate
    self.mutate_rate = mutate_rate
    self.mutate_range = mutate_range
    self.exchange_record = dict()
    self.mutate_record = set()
    self.value_range = value_range
    
    # 如果我没理解错的话这里的eval_v只取决于排名而不是具体距离
    self.eval_v = [ self.alpha*(1-self.alpha) ** i for i in xrange(self.pop_size)]
    evs = sum(self.eval_v)
    # 所以需要归一化？
    self.eval_v = [v / evs for v in self.eval_v]

    self.individuals = [
      [ random.randint(*value_range) for _j in xrange(scale) ]
      for _i in xrange(pop_size)
    ]
  
  def choice(self):
    r = random.random()
    for i in xrange(self.pop_size):
      r -= self.eval_v[i]
      if r <= 0:
        return i

  def select(self):
    self.individuals.sort(key = self.graph.get_distance)
    next_generation = [
      list(self.individuals[ self.choice() ])
      for _ in xrange(self.pop_size)
    ]
    self.individuals = next_generation

  def exchange(self):
    for i, vec1 in enumerate(self.individuals):
      for j, vec2 in enumerate(self.individuals):
        if random.random() >= self.exchange_rate:
          continue
        pos = random.randint(0, self.scale-1)
        vec1[pos:], vec2[pos:] = vec2[pos:], vec1[pos:]
        self.record_exchange(i, j)
        self.record_exchange(j, i)
  
  def record_exchange(self, f, t):
    if f in self.exchange_record:
      self.exchange_record[f].add(t)
    else:
      self.exchange_record[f] = set([t])

  def mutate(self):
    ukmin, ukmax = self.mutate_range
    for k, vec in enumerate(self.individuals):
      if random.random() >= self.mutate_rate:
        continue
      for i in xrange(self.scale):
        dk = int(ukmin + random.random() * (ukmax - ukmin))
        new_val = vec[i] + dk
        new_val = max(new_val, self.value_range[0])
        new_val = min(new_val, self.value_range[1])
        vec[i]  = new_val
      self.record_mutate(k)
  
  def record_mutate(self, i):
    self.mutate_record.add(i)

  def next(self):
    self.exchange_record = dict()
    self.mutate_record = set()

    self.select()
    self.exchange()
    self.mutate()
    
    self.generation_index += 1
    return self.individuals
  
  def display(self):
    print "Generation", self.generation_index
    for i, vec in enumerate(self.individuals):
      print i, ":",
      for j, v in enumerate(vec):
        if j > 0:
          print '->',
        print v,
      print '# Distance =', self.graph.get_distance(vec),
      if i in self.mutate_record:
        print '!!Mutated!!',
      if i in self.exchange_record:
        print '@ Exchanged with: [', ', '.join(map(str, self.exchange_record[i])),']',
      print
    print