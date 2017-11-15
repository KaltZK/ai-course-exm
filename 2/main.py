#!/usr/bin/env python
#encoding=UTF-8
from graph import Graph
from evolution import Evolution

# 随便写的参数
pop_size      = 15
node          = 6
alpha         = 0.5
crossover_rate = 0.02
mutate_rate   = 0.1
generation_num= 5

use_gui = False
gui_plot_col  = 5

edges = [
  (0, 1, 3),
  (1, 2, 3),
  (2, 3, 3),
  (3, 4, 3),
  (4, 5, 3),
  (5, 0, 3),
  (2, 4, 1),
  (0, 3, 15),
  (1, 4, 8),
  (2, 0, 54),
  (4, 0, 2),
  (5, 2, 4),
  (5, 3, 2),
  (2, 5, 44),
  (0, 2, 28),
  (5, 1, 46),
  (4, 2, 72),
  (5, 3, 41),
  (3, 5, 64),
  (1, 3, 93),
  (3, 0, 1),
  (1, 5, 82),
]


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
  gui.plt.figure(figsize=(gui_plot_row*5, gui_plot_col*5))
  gui.init(node, edges)

evol.display()
for g in xrange(generation_num):
  evol.next()
  evol.display()
  if use_gui:
    for i, p in enumerate(evol.individuals):
      gui.plt.subplot(gui_plot_row, gui_plot_col, i+1)
      gui.draw(p, graph)
    # gui.plt.show()
    gui.plt.savefig('imgs/g%04d.svg'%(g))
    gui.plt.clf()