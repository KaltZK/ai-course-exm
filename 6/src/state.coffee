import shuffle from 'shuffle-array'

export BOAT =
  L: 0
  R: 1

BOAT_SIZE = 2

export generate_init = (m, n) ->
  lb: # 左岸
    m: m# 传教士
    c: n# 野蛮人
  rb: # 右岸
    m: 0
    c: 0
  b: BOAT.L # 船的位置

export generate_dest = (m, n) ->
  lb: # 左岸
    m: 0# 传教士
    c: 0# 野蛮人
  rb: # 右岸
    m: m
    c: n
  b: BOAT.R # 船的位置

export hash = (s) ->
  tm = s.lb.m + s.rb.m
  tc = s.lb.c + s.rb.c
  (s.b * tm ** 2 * tc ** 2) + (s.lb.m * tm * tc ** 2) + (s.rb.m * tc ** 2) + (s.lb.c * tc) + (s.rb.c)

export equal_bank = (b1, b2) ->
  b1.m == b2.m and b1.c == b2.c

export equal = (s1, s2)->
  equal_bank(s1.lb, s2.lb) and equal_bank(s1.rb, s2.rb) and s1.b == s2.b

export valid_bank = (b) ->
  b.m >= 0 and b.c >= 0 and (b.m == 0 or b.m >= b.c)

export valid = (s)->
  valid_bank(s.rb) and valid_bank(s.lb)

export get_children = (s) ->
  if s.b == BOAT.L
    bank  = s.lb
    tfunc = to_right_bank 
  else 
    bank  = s.rb
    tfunc = to_left_bank
  children = []
  for dm in [0..bank.m]
    for dc in [0..bank.c]
      if (dm != 0 or dc != 0) and (dm + dc <= BOAT_SIZE)
        c = tfunc(s, dm, dc)
        if valid(c)
          children.push c
  children

export to_right_bank = (s, m, n) ->
  console.log("TO R: (#{s.lb.m}, #{s.lb.c}) -> (#{m}, #{n}) -> (#{s.rb.m}, #{s.rb.c})")
  throw "No one on the boat." if m == 0 and n == 0
  throw "Boat is full." if m+n>BOAT_SIZE
  throw "Invalid Bank" if s.b == BOAT.R
  return
    lb: # 左岸
      m: s.lb.m - m # 传教士
      c: s.lb.c - n # 野蛮人
    rb: # 右岸
      m: s.rb.m + m
      c: s.rb.c + n
    b: BOAT.R # 船的位置
    parent: s

export get_path = (s) ->
  path = []
  while s
    path.push(s)
    s = s.parent
  path.reverse()

export to_left_bank = (s, m, n) ->
  console.log("TO L:(#{s.lb.m}, #{s.lb.c}) <- (#{m}, #{n}) <- (#{s.rb.m}, #{s.rb.c})")
  throw "No one on the boat." if m == 0 and n == 0
  throw "Boat is full." if m+n>BOAT_SIZE
  throw "Invalid Bank" if s.b == BOAT.L
  return
    lb: # 左岸
      m: s.lb.m + m # 传教士
      c: s.lb.c + n # 野蛮人
    rb: # 右岸
      m: s.rb.m - m
      c: s.rb.c - n
    b: BOAT.L # 船的位置
    parent: s

export distance = (s1, s2) ->
  sum = 0
  for b in ['lb', 'rb']
    for k in ['m', 'c']
      sum += Math.abs(s1[b][k] - s2[b][k])
  sum