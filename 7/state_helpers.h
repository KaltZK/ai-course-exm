#ifndef _STATE_HELPERS_H
#define _STATE_HELPERS_H

#define B_WIDTH   15
#define B_HEIGHT  15
#define C_INF     2048
#define C_INF_RANGE     1024

enum PosState{
  C_EMPTY,
  C_BLACK,
  C_WHITE,
  C_BLOCKED
};

enum Player{
  P_BLACK,
  P_WHITE
};

struct Range{
  int gte;
  int lte;
};

struct GameState {
  enum PosState board[B_WIDTH][B_HEIGHT];
  int weight;
};

struct GameOperation{
  int x, y;
  enum Player player;
};

enum PosState get_state(struct GameState *s, int x, int y);
void set_state(struct GameState *s, int x, int y, enum PosState val);

void calc_weight(struct GameState *state);
struct GameState *new_state();
struct GameState *update_state(struct GameState *state, int x, int y, enum PosState val);

int is_inf(int v);

int is_pos_inf(int v);
int is_neg_inf(int v);

void display_state(struct GameState *state);
char disp_pos(enum PosState p);

struct GameOperation operate(int x, int y, enum Player p);
struct GameState *reduce_operation(struct GameState *s, struct GameOperation opt);

struct Range range(int gte, int lte);
int range_empty(struct Range r);
struct Range range_union(struct Range a, struct Range b);

int max(int a, int b);

int min(int a, int b);

int end_state(struct GameState *s);

#endif