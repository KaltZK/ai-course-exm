#include <cstring>
#include <set>
#include <vector>
using namespace std;
#include "state.h"

GameState::GameState(GameItem mc, GameItem ml, GameItem bal, GameItem bol){
  monkey_carrying = mc;
  monkey_loc = ml;
  banana_loc = bal;
  box_loc = bol;
}

GameState::GameState(GameState *const gs){
  monkey_carrying = gs->monkey_carrying;
  monkey_loc      = gs->monkey_loc;
  banana_loc      = gs->banana_loc;
  box_loc         = gs->box_loc;
}

// 谓词
bool GameState::AT(GameItem x, GameItem w){
  if(!(x & X && w & W)) return false;
  return monkey_loc == w;
}
bool GameState::HOLD(GameItem x, GameItem t){
  if(!(x & X && t & T)) return false;
  return monkey_carrying == t;
}

bool GameState::EMPTY(GameItem x){
  if(!(x & X)) return false;
  return monkey_carrying == NOTHING;
}

bool GameState::ON(GameItem t, GameItem y){
  if(!(t & T && y & Y)) return false;
  if(t == BANANA)
    return banana_loc == y;
  else 
    return box_loc == y;
}

bool GameState::CLEAR(GameItem y){
  if(!(y & Y)) return false;
  return monkey_loc != y && banana_loc != y && box_loc != y;
}

bool GameState::IS_BOX(GameItem u){
  if(!(u & U)) return false;
  return u == BOX;
}

bool GameState::IS_BANANA(GameItem v){
  if(!(v & V)) return false;
  return v == BANANA;
}

// 行动
GameState *GameState::WALK(GameItem m, GameItem n){
  if(m != monkey_loc) return NULL;
  if(!(m & W && n & W) ) return NULL;
  GameState *ns = new GameState(this);
  ns -> monkey_move(n);
  return ns;
}

GameState *GameState::CARRY(GameItem s, GameItem r){
  if(!(s & S && r & R) ) return NULL;
  if(location_of(s) != r) return NULL;
  if(r != monkey_loc && !(monkey_loc == BOX && r == CEILING && box_loc == B) ) return NULL;
  GameState *ns = new GameState(this);
  ns -> monkey_carrying = s;
  return ns;
}

GameState *GameState::CLIMB(GameItem b, GameItem u){
  if(b != BOX || u == CEILING) return NULL;
  GameState *ns = new GameState(this);
  ns -> monkey_carrying = NOTHING;
  ns -> monkey_loc = b;
  return ns;
}

void GameState::monkey_move(GameItem loc){
  monkey_loc = loc;
  update_carring_item_pos();
}

void GameState::update_carring_item_pos(){
  if(monkey_carrying == BANANA){
    banana_loc = monkey_loc;
  }else if(monkey_carrying == BOX){
    box_loc = monkey_loc;
  }
}

GameItem GameState::location_of(GameItem i){
  if(i == MONKEY){
    return monkey_loc;
  }else if(i == BANANA){
    return banana_loc;
  }else if(i == BOX){
    return box_loc;
  }else{
    return NOTHING;
  }
}

bool GameState::equal(GameState* gs){
  return
    gs != NULL &&
    monkey_carrying == gs->monkey_carrying &&
    monkey_loc == gs->monkey_loc &&
    banana_loc == gs->banana_loc &&
    box_loc == gs->box_loc;    
}

#include "display.cpp"