#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>

#include "state_helpers.h"
#include "search.h"

#define DEBUG 0
#define DEBUG_DISPLAY_STATE 0
#define DISPLAY_PRUNING 0

#define RESTRICT_ANS 1

#define NEIGHBOR_DISTANCE 4
#define NEIGHBOR_THRESHOLD 3

struct GameState *search_by_player(
struct GameState *state, 
struct Range rang,
int depth,
int (*cmp)(int, int),
enum PosState fill,
struct Range (*range_update)(struct Range, int),
struct GameState *(*next_search)(struct GameState *, struct Range rang, int)){
  int i, j, p, q;
  int neighbor_ct = 0;
  struct NeighborInfo *neighbors;
  int m_score;
  int buf_size = 20;
  int max_neighbor = 0;
  static int neighbor_counter[B_WIDTH][B_HEIGHT];
  struct GameState *ns, *predict, *ans = NULL;
  assert(state != NULL);
  if(depth == 0){
    #if DEBUG_DISPLAY_STATE
    display_state(state);
    #endif 
    return state;
  }else{
    if(empty_state(state)){
      return update_state(state, B_WIDTH / 2, B_HEIGHT / 2, fill);
    }
    memset(neighbor_counter, 0, sizeof(neighbor_counter));
    for(i=0; i<B_WIDTH; i++){
      for(j=0; j<B_WIDTH; j++){
        if(get_state(state, i, j) != C_EMPTY){
          for(p=max(0, i-NEIGHBOR_DISTANCE); p<min(B_WIDTH, i+NEIGHBOR_DISTANCE); p++){
            for(q=max(0, i-NEIGHBOR_DISTANCE); q<min(B_HEIGHT, i+NEIGHBOR_DISTANCE); q++){
              neighbor_counter[p][q]+= NEIGHBOR_DISTANCE - min(abs(p - i), abs( q-j ));
              max_neighbor = max(max_neighbor, neighbor_counter[p][q]);
            }
          }
        }
      }
    }
    
    neighbors = malloc(sizeof(struct NeighborInfo) * buf_size);
    for(i=0; i<B_WIDTH; i++){
      for(j=0; j<B_HEIGHT; j++){
        if(get_state(state, i, j) != C_EMPTY)
          continue;
        if(neighbor_counter[i][j] < min(max_neighbor, NEIGHBOR_THRESHOLD))
          continue;
        neighbors[neighbor_ct++] = neighbor_info(i, j, neighbor_counter[i][j]);
        if(neighbor_ct > buf_size / 2){
          buf_size *= 2;
          neighbors = realloc(neighbors, sizeof(struct NeighborInfo) * buf_size);
        }
      }
    }
    qsort(neighbors, neighbor_ct, sizeof(struct NeighborInfo), neighbor_info_cmp);
    for(p=0; p<neighbor_ct; p++){
      i = neighbors[p].x;
      j = neighbors[p].y;
      ns = update_state(state, i, j, fill);
      #if RESTRICT_ANS
      assert(ns != NULL);
      #endif
      if(ns == NULL) continue;
      predict = next_search(ns, rang, depth - 1);
      if(ans == NULL){
        ans = ns;
        m_score = predict->weight;
        rang = range_update(rang, m_score);
      }else{
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
    ignore_rest_branches:
    #if RESTRICT_ANS
    assert(ans != NULL);
    #endif
    free(neighbors);
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

struct NeighborInfo neighbor_info(int x, int y, int n){
  struct NeighborInfo ni;
  ni.x = x;
  ni.y = y;
  ni.neighbors = n;
  return ni;
}

int neighbor_info_cmp(const void *_a, const void *_b){
  struct NeighborInfo *a = _a, *b = _b;
  return b->neighbors - a->neighbors;
}