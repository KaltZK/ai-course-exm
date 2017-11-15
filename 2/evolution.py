#!/usr/bin/env python
#encoding=UTF-8
import random
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
    for i, vec1 in enumerate(self.individuals):
      for j, vec2 in enumerate(self.individuals):
        if random.random() >= self.crossover_rate:
          continue
        print vec1, vec2
        vec1.reverse()
        vec2.reverse()
        nv1 = []
        nvs1=set()
        nv2 = []
        nvs2=set()
        while vec1 or vec2:
          if vec1 and vec1[-1] not in nvs1:
            val = vec1.pop()
            nv1.append( val )
            nvs1.add(val)
          if vec2 and vec2[-1] not in nvs2:
            val = vec2.pop()
            nv2.append( val )
            nvs2.add(val)
          vec1, vec2 = vec2, vec1
        vec1.extend(nv1)
        vec2.extend(nv2)
        print vec1, vec2, '$'
        self.record_crossover(i, j)
        self.record_crossover(j, i)
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
  
  def display(self):
    print "Generation", self.generation_index
    for i, vec in enumerate(self.individuals):
      print i, ":",
      for j, v in enumerate(vec):
        print v, '->',
      print vec[0],
      print '# Distance =', self.graph.get_distance(vec),
      if i in self.mutate_record:
        print '!!Mutated!!',
      if i in self.crossover_record:
        print '@ Crossover with: [', ', '.join(map(str, self.crossover_record[i])),']',
      print
    print