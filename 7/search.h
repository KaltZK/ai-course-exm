#ifndef _SEARCH_H
#define _SEARCH_H

#include "state_helpers.h"

#define SEARCH_DEPTH 2

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