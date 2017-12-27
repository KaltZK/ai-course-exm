#include "state.h"

const char *name_of(GameItem i){
  switch(i){
    case NOTHING:   return "nothing";
    case MONKEY:    return "monkey";
    case A:         return "a";
    case B:         return "b";
    case C:         return "c";
    case BOX:       return "box";
    case CEILING:   return "ceiling";
    case BANANA:    return "banana";
    default: throw "Invalid Item";
  }
}

std::ostream& operator<< (std::ostream &os, GameState* gs){
  if(gs == NULL){
    os << "<invalid state>";
  }else{
    gs->display(os);
  }
  return os;
}

void GameState::display(std::ostream &os){
  const GameItem items[]={BANANA, BOX};
  const GameItem locs[]={A, B, C, CEILING}; 
  os
    << "AT(" 
    << "monkey, "
    << name_of(monkey_loc) 
    << ")^";
  
  if( EMPTY(MONKEY) ){
    os 
      << "EMPTY(" 
      << name_of(MONKEY) 
      << ")^";
  }else{
    os 
      << "HOLD(" 
      << name_of(MONKEY) 
      << ", "
      << name_of(monkey_carrying)
      << ")^";
  }

  for(int i=0; i<2; i++){
    GameItem loc = location_of(items[i]);
    if(loc != NOTHING){
      os  << "ON("
          << name_of(items[i])
          << ", "
          << name_of(loc)
          << ")^";
    }
  }

  for(int i=0; i<4; i++){
    if(CLEAR(locs[i])){
      os  << "CLEAR("
          << name_of(locs[i])
          << ")^";
    }
  }

  os << "BOX("<< name_of(BOX) << ")^";
  os << "BANANA("<< name_of(BANANA) << ")";
}