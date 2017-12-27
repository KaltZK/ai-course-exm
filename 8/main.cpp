#include <iostream>
#include <cstdlib>
#include "state.h"
using namespace std;

static GameState *state;

void _update_state(const char *opname, GameItem op1, GameItem op2, GameState *next){
  delete state;
  state = next;
  cout
    << opname << "("<<name_of(op1) << ", " << name_of(op2) << "):" << endl
    << state << endl << endl;
  if(state == NULL){
    cout << "Error: Invalid State." << endl;
    exit(-1);
  }
}

void WALK(GameItem m, GameItem n){
  _update_state( "WALK", m, n, state->WALK(m, n));
}
void CARRY(GameItem s, GameItem r){
  _update_state( "CARRY", s, r, state->CARRY(s, r));
}
void CLIMB(GameItem s, GameItem r){
  _update_state( "CLIMB", s, r, state->CLIMB(s, r));
}

int main(){
  state = new GameState(NOTHING, A, CEILING, C);
  
  WALK(A, C);
  CARRY(BOX, C);
  WALK(C, B);
  CLIMB(BOX, B);
  CARRY(BANANA, CEILING);
  
  cout << "Done." << endl;

  return 0;
}