import shuffle from 'shuffle-array'

export TARGET=
  distance: 0
  empty: [1, 1]
  arr: [
    1, 2, 3,
    8, 0, 4,
    7, 6, 5
  ],
  h: 0

TARGET_POS_TABLE = [
  4, 0, 1, 2, 5, 8, 7, 6, 3
]


export DIRE=
  UP:     0
  RIGHT:  1
  DOWN:   2
  LEFT:   3

export dX = [-1,  0, +1,  0]
export dY = [ 0, +1,  0, -1]
export dI = [-3, +1, +3, -1]

export valid_pos=([x, y]) -> 
  x>=0 && x < 3 && y >= 0 && y < 3

export pos2index= ([x, y]) ->
  x * 3 + y

export index2pos= (idx) ->
  [Math.floor(idx/3), idx%3]

export valid_index=(idx)->
  valid_pos(index2pos(idx))

export replace=(src, dst) ->
  throw "NOT EQUAL" unless equal(src, dst)
  dst.h = src.h
  dst.distance = src.distance
  dst.p = src.p

export distance_to_target = (state) ->
  dist = 0
  for idx in [0...9]
    [ x,  y] = index2pos(idx)
    [tx, ty] = index2pos(TARGET_POS_TABLE[state.arr[idx]])
    dist += Math.abs(x - tx) + Math.abs(y - ty)
  dist

hash = (state) ->
  h = 0
  for s in state.arr
    h *= 10
    h += s
  h


export swap_by_index = (state, idxf, idxt) ->
  throw("invalid idxf: empty pos not match ( #{idxf} for #{state.arr} )") unless state.arr[idxf] == 0
  next = Object.assign {}, state
  next.arr = Array.from state.arr
  next.arr[idxf] = state.arr[idxt]
  next.arr[idxt] = state.arr[idxf]
  next.empty = index2pos(idxt)
  next.distance = state.distance + 1
  next.parent = state
  next.h = distance_to_target(next)
  next.hash = hash(next)
  next.p = next.h + next.distance
  next

export children= (state) ->
  th_idx = pos2index(state.empty)
  [x, y] = state.empty
  cd_idx =( pos2index([x + dX[k], y + dY[k]]) for k in [0...4] when valid_pos([x + dX[k], y + dY[k]]) )
  # console.log cd_idx
  cd_idx.map (cdx) =>
    swap_by_index state, th_idx, cdx

export equal= (s1, s2) ->
  for i in [0...9]
    return false if s1.arr[i] != s2.arr[i]
  true

zero_pos = (arr) ->
  for i in [0...9]
    if arr[i] == 0
      return index2pos i

export from_array = (arr) ->
  s = {
    parent: null,
    distance: 0,
    empty: zero_pos(arr),
    arr
  }
  s.h = distance_to_target(s)
  s.hash = hash(s)
  s.p = s.h + s.distance
  s

export random_state= ->
  arr = [0...9]
  arr = shuffle arr
  from_array arr

export get_seq = (cur_state) ->
  seq = []
  head = cur_state
  while head != null
    seq.push head
    head = head.parent
  seq.reverse()