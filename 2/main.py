#!/usr/bin/env python
#encoding=UTF-8
import json
import sys
from graph import Graph
from evolution import Evolution

# 随便写的参数
pop_size        = 10
alpha           = 0.5
crossover_rate  = 0.1
mutate_rate     = 0.1
generation_num  = 50

use_gui = False
gui_plot_col  = 5

print_path = False
print_mutate= True
print_crossover = True

data = json.load(open(sys.argv[1]))
node = data['node']
edges= data['edges']


graph = Graph(node)
for f, t, d in edges:
  graph[f, t] = d

evol = Evolution(
  pop_size,
  node,
  alpha,
  crossover_rate,
  mutate_rate,
  graph
)

gui_plot_row = pop_size / gui_plot_col + int(pop_size % gui_plot_col)

if use_gui:
  import gui
  gui.plt.figure(figsize=(gui_plot_col*5, gui_plot_row*5))
  gui.init(node, edges)

evol.display(print_path, print_mutate, print_crossover)
for g in xrange(generation_num):
  evol.next()
  evol.display(print_path, print_mutate, print_crossover)
  if use_gui:
    for i, p in enumerate(evol.individuals):
      gui.plt.subplot(gui_plot_row, gui_plot_col, i+1)
      gui.draw(p, graph)
    # gui.plt.show()
    gui.plt.savefig('imgs/g%04d.svg'%(g))
    gui.plt.clf()

print "Detected Shortest Loop:"
loop = min(evol.individuals, key = graph.get_distance)
for i, p in enumerate(loop):
  print p, '->',
print loop[0]

print "Length:",graph.get_distance(loop)