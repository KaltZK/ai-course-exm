#include <stdlib.h>
#include <assert.h>
#include <stdio.h>

#include "state_helpers.h"
#include "search.h"

#define DEBUG 0
#define DEBUG_DISPLAY_STATE 0
#define DISPLAY_WEIGHT 0
#define DISPLAY_CUT 0

struct GameState *search_by_player(
struct GameState *state, 
struct Range rang,
int depth,
int (*cmp)(int, int),
enum PosState fill,
struct Range (*range_update)(struct Range, int),
struct GameState *(*next_search)(struct GameState *, struct Range rang, int)){
  int i, j;
  int m_score;
  struct GameState *ns, *predict, *ans = NULL;
  assert(state != NULL);
  if(depth == 0){
    #if DEBUG_DISPLAY_STATE
    display_state(state);
    #endif 
    return state;
  }else{
    #if DISPLAY_WEIGHT
    printf("weights: [");
    #endif
    for(i=0; i<B_WIDTH; i++){
      for(j=0; j<B_HEIGHT; j++){
        if(get_state(state, i, j) != C_EMPTY){
          continue;
        }
        ns = update_state(state, i, j, fill);
        assert(ns != NULL);
        predict = next_search(ns, rang, depth - 1);
        assert(ns != NULL);
        if(ans == NULL){
          ans = ns;
          m_score = predict->weight;
          rang = range_update(rang, m_score);
        }else{      
          #if DISPLAY_WEIGHT
          if(is_pos_inf(ns->weight)){
            printf(" +INF,");
          }else if(is_neg_inf(ns->weight)){
            printf(" -INF,");
          }else{
            printf(" %d,", ns->weight);
          }
          #endif
          if(cmp(m_score, ns->weight) == m_score){
            free(ns);
          }else{
            free(ans);
            ans = ns;
            m_score = predict->weight;
            rang = range_update(rang, m_score);
            // printf("[%d, %d] << %d\n", rang.gte, rang.lte, ns->weight);
          }
        }
        assert(ans != NULL);
        if(range_empty(rang)){
          #if DISPLAY_CUT
          printf("CUT!: [%d, %d]\n", rang.gte, rang.lte);
          #endif
          goto ignore_rest_branches;
        }
      }
    }
    ignore_rest_branches:
    #if DISPLAY_WEIGHT
    printf("]\n");
    #endif
    assert(ans != NULL);
    return ans;
  }
}

struct Range range_update_gte(struct Range r, int a){
  r.gte = a;
  return r;
}

struct Range range_update_lte(struct Range r, int a){
  r.lte = a;
  return r;
}

struct GameState *search_by_black(
struct GameState *state, 
struct Range rang,
int depth){
  #if DEBUG_DISPLAY_STATE
  int _x = SEARCH_DEPTH-depth;
  while(_x--) printf("  ");
  puts("Player: BLACK");
  #endif
  return search_by_player(
    state,
    rang,
    depth,
    max,
    C_BLACK,
    range_update_gte,
    search_by_white
  );
}

struct GameState *search_by_white(
struct GameState *state, 
struct Range rang,
int depth){
  #if DEBUG_DISPLAY_STATE
  int _x = SEARCH_DEPTH-depth;
  while(_x--) printf("  ");
  puts("Player: WHITE");
  #endif
  return search_by_player(
    state,
    rang,
    depth,
    min,
    C_WHITE,
    range_update_lte,
    search_by_black
  );
}