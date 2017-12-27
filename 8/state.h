#ifndef _STATE_H
#define _STATE_H

#include <set>
#include <iostream>

enum GameItem{
  NOTHING = 0,
  MONKEY = 1<<0,
  A = 1<<1,
  B = 1<<2,
  C = 1<<3,
  BOX = 1<<4,
  CEILING = 1<<5,
  BANANA =  1<<6
};

enum ItemDomain{
  X = MONKEY,
  W = A | B | C | BOX,
  T = BOX | BANANA,
  Y = B | C | CEILING,
  U = BOX,
  V = BANANA,
  R = C | CEILING,
  S = BOX | BANANA
};

struct GameState{
  GameItem monkey_carrying;
  GameItem monkey_loc, banana_loc, box_loc;

  GameState(GameItem mc, GameItem ml, GameItem bal, GameItem bol);
  GameState(GameState *gs);

  // 谓词
  bool AT(GameItem x, GameItem w);
  bool HOLD(GameItem x, GameItem t);
  bool EMPTY(GameItem x);
  bool ON(GameItem t, GameItem y);
  bool CLEAR(GameItem y);
  bool IS_BOX(GameItem u);
  bool IS_BANANA(GameItem v);

  // 行动
  GameState *WALK(GameItem m, GameItem n);
  GameState *CARRY(GameItem s, GameItem r);
  GameState *CLIMB(GameItem s, GameItem r);

  void monkey_move(GameItem loc);
  void update_carring_item_pos();
  GameItem location_of(GameItem i);
  void display(std::ostream &os);
  bool equal(GameState* gs);
};

std::ostream& operator<< (std::ostream &os, GameState*);

const char *name_of(GameItem);

#endif