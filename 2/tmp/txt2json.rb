#!/usr/bin/env ruby
#encoding=utf-8
require 'json'
n_s, f, t = ARGV
node = n_s.to_i
data = File.read(f).split.map(&:to_i)
edges = []
node.times do |i|
  node.times do |j|
    next if i >= j
    edges.push([i, j, data[i*node + j]])
  end
end
File.write t, {
  node: node,
  edges: edges
}.to_json