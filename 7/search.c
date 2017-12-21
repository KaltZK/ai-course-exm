#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>

#include "state_helpers.h"
#include "search.h"

#define DEBUG 0
#define DEBUG_DISPLAY_STATE 0
#define DISPLAY_WEIGHT 0
#define DISPLAY_PRUNING 0

#define RESTRICT_ANS 1

#define NEIGHBOR_PRUNING 1
#define NEIGHBOR_DISTANCE 4
#define NEIGHBOR_THRESHOLD 2

struct GameState *search_by_player(
struct GameState *state, 
struct Range rang,
int depth,
int (*cmp)(int, int),
enum PosState fill,
struct Range (*range_update)(struct Range, int),
struct GameState *(*next_search)(struct GameState *, struct Range rang, int)){
  int i, j, p, q;
  int m_score;
  int max_neighbor = 0;
  static int neighbor_counter[B_WIDTH][B_HEIGHT];
  struct GameState *ns, *predict, *ans = NULL;
  assert(state != NULL);
  #if NEIGHBOR_PRUNING
  if(empty_state(state)){
    return update_state(state, B_WIDTH / 2, B_HEIGHT / 2, fill);
  }
  memset(neighbor_counter, 0, sizeof(neighbor_counter));
  for(i=0; i<B_WIDTH; i++){
    for(j=0; j<B_WIDTH; j++){
      if(get_state(state, i, j) != C_EMPTY){
        for(p=max(0, i-NEIGHBOR_DISTANCE); p<min(B_WIDTH, i+NEIGHBOR_DISTANCE); p++){
          for(q=max(0, i-NEIGHBOR_DISTANCE); q<min(B_HEIGHT, i+NEIGHBOR_DISTANCE); q++){
            neighbor_counter[p][q]++;
            max_neighbor = max(max_neighbor, neighbor_counter[p][q]);
          }
        }
      }
    }
  }
  #endif
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
        #if NEIGHBOR_PRUNING
        // printf("%d %d\n", state -> step, neighbor_counter[i][j]);
        if(neighbor_counter[i][j] < min(max_neighbor, NEIGHBOR_THRESHOLD)){
          continue;
        }
        // printf("X %d\n", neighbor_counter[i][j]);
        #endif
        ns = update_state(state, i, j, fill);
        if(ns == NULL) continue;
        #if RESTRICT_ANS
        assert(ns != NULL);
        #endif
        predict = next_search(ns, rang, depth - 1);
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
            //printf("[%d, %d] << %d\n", rang.gte, rang.lte, ns->weight);
          }
        }
        assert(ans != NULL);
        if(range_empty(rang)){
          #if DISPLAY_PRUNING
          printf("Prune!: pos: (%d, %d), depth: %d, range: [%d, %d]\n", 
            i, j,
            depth,
            rang.gte, rang.lte);
          #endif
          goto ignore_rest_branches;
        }
      }
    }
    ignore_rest_branches:
    #if DISPLAY_WEIGHT
    printf("]\n");
    #endif
    #if RESTRICT_ANS
    assert(ans != NULL);
    #endif
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