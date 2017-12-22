#ifndef _SEARCH_H
#define _SEARCH_H

#include "state_helpers.h"

#define SEARCH_DEPTH 4

struct NeighborInfo{
  int x, y, neighbors;
};

struct NeighborInfo neighbor_info(int x, int y, int n);

int neighbor_info_cmp(const void *_a, const void *_b);

struct GameState *search_by_player(
  struct GameState *state, 
  struct Range rang,
  int depth,
  int (*cmp)(int, int),
  enum PosState fill,
  struct Range (*range_update)(struct Range, int),
  struct GameState *(*next_search)(struct GameState *, struct Range rang, int));

struct Range range_update_gte(struct Range r, int a);

struct Range range_update_lte(struct Range r, int a);

struct GameState *search_by_black(
  struct GameState *state, 
  struct Range rang,
  int depth);

struct GameState *search_by_white(
  struct GameState *state, 
  struct Range rang,
  int depth);


#endif