#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "state_helpers.h"
#include "search.h"

void display(){
  int i=0;
  struct GameState *(*const funcs[])(struct GameState *, struct Range, int)
    ={search_by_black, search_by_white};
  const char *names[] = {"BLACK", "WHITE"};
  struct Range r = range(-C_INF, C_INF);
  struct GameState *ns, *next; 
  struct GameState *s = new_state();
  display_state(s);
  ns = s;
  while(!end_state(ns)){
    next = funcs[i%2](ns, r, SEARCH_DEPTH);
    free(ns);
    printf("Player: %s (Round %d)\n", names[i%2], i+1);
    display_state(next);
    ns = next;
    i++;
  }
  if(is_pos_inf(ns->weight)){
    puts("Black Wins!");
  }else{
    puts("White Wins!");
  }
}

struct GameState *search_by_user(
  struct GameState *state,
  enum PosState fill
){
  int ix, iy;
  printf("Your Turn (as %s). Input x y:", (fill == C_BLACK ? "Black" : "White"));
  scanf("%d%d", &ix, &iy);
  assert(ix>=0 && ix < B_WIDTH && iy>=0 && iy < B_HEIGHT);
  return update_state(state, ix, iy, fill);
}

struct GameState *user_as_black(
struct GameState *state, 
struct Range rang,
int depth){
  return search_by_user(state, C_BLACK);
}

struct GameState *user_as_white(
struct GameState *state, 
struct Range rang,
int depth){
  return search_by_user(state, C_WHITE);
}

void battle(){
  struct GameState *(*const funcs[][2])(struct GameState *, struct Range, int)
    ={ 
      {user_as_black, search_by_white},
      {search_by_black, user_as_white},
    };
  const char *names[] = {"BLACK", "WHITE"};
  
  int type, i;
  struct GameState *ns, *next;
  struct Range r = range(-C_INF, C_INF);
  
  printf("Black(1) or White(2)?");
  scanf("%d", &type);
  type --;
  assert(type >= 0 && type < 2);
  ns = new_state();
  i = 0;
  while(ns != NULL && !end_state(ns)){
    printf("Player: %s (Round %d)\n", names[i%2], i+1);
    next = funcs[type][i%2](ns, r, SEARCH_DEPTH);
    display_state(next);
    free(ns);
    ns = next;
    i++;
  }
  if(ns != NULL){
    if(is_pos_inf(ns->weight)){
      puts("Black Wins!");
    }else{
      puts("White Wins!");
    }
  }else{
    puts("State is Empty: Failed to search.");
  }
}

int main(int argc, char **args){
  if(argc == 2 && strcmp(args[1], "battle") == 0){
    battle();
  }else{
    display();
  }
  return 0;
}