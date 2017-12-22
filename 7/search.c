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

#define NEIGHBOR_DISTANCE  2
#define NEIGHBOR_THRESHOLD 3

void _calc_search_weight(
  struct GameState *state,
  int pos_weight[B_WIDTH][B_HEIGHT],
  int pos_ref_x[B_WIDTH][B_HEIGHT], 
  int pos_ref_y[B_WIDTH][B_HEIGHT]
){
  int i, j, k, p, q, rp, rq, ri, rj, max_w;
  const int weight_neighbors_dx[] = {-1,  0, -1,-1};
  const int weight_neighbors_dy[] = { 0, -1, -1,+1};
  for(i=0; i<B_WIDTH; i++){
    for(j=0; j<B_WIDTH; j++){
      if(get_state(state, i, j) != C_EMPTY){
        max_w = 1;
        ri = i;
        rj = j;
        for(k=0; k<4; k++){
          p = i + weight_neighbors_dx[k];
          q = i + weight_neighbors_dy[k];
          if(!valid_pos(p, q) || get_state(state, p, q) != get_state(state, i, j)) continue;
          rp = pos_ref_x[p][q];
          rq = pos_ref_y[p][q];
          if(pos_weight[rp][rq] + 1 > max_w){
            max_w = pos_weight[rp][rq] + 1;
            ri = rp;
            rj = rq;
          }
        }
        pos_ref_x[i][j] = ri;
        pos_ref_y[i][j] = rj;
        pos_weight[i][j] = -1;
        pos_weight[ri][rj] = max_w;
      }else{
        pos_ref_x[i][j] = i;
        pos_ref_y[i][j] = j;
        pos_weight[i][j] = 0;
      }
    }
  }
}

void _calc_neighbors(
  struct GameState *state,
  int *max_neighbor,
  int neighbor_counter[B_WIDTH][B_HEIGHT],
  int pos_weight[B_WIDTH][B_HEIGHT],
  int pos_ref_x[B_WIDTH][B_HEIGHT], 
  int pos_ref_y[B_WIDTH][B_HEIGHT]
){
  int i, j, p, q, ri, rj;
  for(i=0; i<B_WIDTH; i++){
    for(j=0; j<B_WIDTH; j++){
      if(get_state(state, i, j) != C_EMPTY){
        ri = pos_ref_x[i][j];
        rj = pos_ref_y[i][j];
        for(p=max(0, i-NEIGHBOR_DISTANCE); p<=min(B_WIDTH-1, i+NEIGHBOR_DISTANCE); p++){
          for(q=max(0, i-NEIGHBOR_DISTANCE); q<=min(B_HEIGHT-1, i+NEIGHBOR_DISTANCE); q++){
            neighbor_counter[p][q] += pos_weight[ri][rj];
            // neighbor_counter[p][q]+= NEIGHBOR_DISTANCE - min(abs(p-i), abs(q-j));
            *max_neighbor = max(*max_neighbor, neighbor_counter[p][q]);
          }
        }
      }
    }
  }
}

struct GameState *search_by_player(
struct GameState *state, 
struct Range rang,
int depth,
int (*cmp)(int, int),
enum PosState fill,
struct Range (*range_update)(struct Range, int),
struct GameState *(*next_search)(struct GameState *, struct Range rang, int)){
  int i, j, p;
  int neighbor_ct = 0;
  struct NeighborInfo *neighbors;
  int m_score;
  int buf_size = 20;
  int max_neighbor = 0;
  static int pos_ref_x[B_WIDTH][B_HEIGHT], pos_ref_y[B_WIDTH][B_HEIGHT];
  static int pos_weight[B_WIDTH][B_HEIGHT];
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
    _calc_search_weight(state, pos_weight, pos_ref_x, pos_ref_y);
    _calc_neighbors(state, &max_neighbor, neighbor_counter, pos_weight, pos_ref_x, pos_ref_y);
    neighbors = malloc(sizeof(struct NeighborInfo) * buf_size);
    for(i=0; i<B_WIDTH; i++){
      for(j=0; j<B_HEIGHT; j++){
        if(get_state(state, i, j) != C_EMPTY)
          continue;
        if(neighbor_counter[i][j] < min(max_neighbor, NEIGHBOR_THRESHOLD))
          continue;
        neighbors[neighbor_ct++] = neighbor_info(i, j, neighbor_counter[i][j]);
        if(neighbor_ct > buf_size * 2 / 3){
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
  struct NeighborInfo *a = (struct NeighborInfo *)_a, *b = (struct NeighborInfo *)_b;
  return b->neighbors - a->neighbors;
}