#!/usr/bin/env python
#encoding=UTF-8
import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()

def init(N, edges):
  global G_pos
  G.add_nodes_from( xrange(N))
  G.add_weighted_edges_from( edges )
  G_pos = nx.spring_layout(G, k=0.15, iterations=10)

def draw(path, mg):
  edges = mg.get_edges_on_path(path)
  
  nx.draw_networkx_nodes(G, pos = G_pos, edge_color='black', node_size=10, alpha=0.5)
  # nx.draw_networkx_nodes(G, pos = G_pos, node_color='red', alpha = 0.5)
  nx.draw_networkx_edges(G, 
    pos = G_pos, 
    edgelist=edges, 
    edge_color='r', 
    width=2.0,
    alpha = 0.5)
  # nx.draw_networkx_labels(G,G_pos,{x: str(x) for x in xrange(len(path))},font_size=5)