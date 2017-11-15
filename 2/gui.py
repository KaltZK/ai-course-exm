#!/usr/bin/env python
#encoding=UTF-8
import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()

def init(N, edges):
  global G_pos
  G.add_nodes_from( xrange(N))
  G.add_weighted_edges_from( edges )
  G_pos = nx.spring_layout(G, k=0.15, iterations=20)

def draw(path, mg):
  edges = mg.get_edges_on_path(path)
  labels = [e[2] for e in edges]
  nx.draw(G, pos = G_pos)
  nx.draw_networkx_edges(G, 
    pos = G_pos, 
    edgelist=edges, 
    edge_color='r', 
    width=4.0,
    labels = labels)