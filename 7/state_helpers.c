#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <stdio.h>
#include "state_helpers.h"

#define DEBUG 5

int valid_pos(int x, int y){
  return x>=0 && x<B_WIDTH && y>=0 && y<B_HEIGHT;
}

enum PosState get_state(struct GameState *s, int x, int y){
  assert(s != NULL && valid_pos(x, y));
  return s->board[x][y];
}

void set_state(struct GameState *s, int x, int y, enum PosState val){
  assert(s->board[x][y] == C_EMPTY);
  s->board[x][y] = val;
}

int max(int a, int b){
  return a > b ? a : b;
}

int min(int a, int b){
  return a < b ? a : b;
}


static int get_weight_in_seq(int counter, int empty_side){
  if(counter == 3){
    if(empty_side == 2){
      return 64;
    }else if(empty_side == 1){
      return 8;
    }else{
      return 0;
    }
  }else if(counter == 4){
    if(empty_side == 2){
      return 256;
    }else if(empty_side == 1){
      return 128;
    }else{
      return 0;
    }
  }else if(counter >= 5){
    return C_INF;
  }else{
    if(empty_side == 2){
      return counter;
    }else if(empty_side == 1){
      return counter/2;
    }else{
      return 0;
    }
  }
}

void _next_pos(enum PosState val, int op, int *black_p, int *white_p){
  // const int len_weight[] = {0, 1, 2, 4, 128, C_INF};
  // const int len_weight[] = {0, 1, 2, 3, 4, 5};
  static enum PosState last = C_EMPTY;
  static int counter = 0;
  static int empty_side = 0;
  // printf("val = %d (op=%d) C_EMPTY=%d C_BLACK=%d C_WHITE=%d\n", val, op, C_EMPTY, C_BLACK, C_WHITE);
  switch(op){
    case 0:
      last = C_EMPTY;
      counter = 0;
      empty_side = 0;
      break;
    case 1:
      #if DEBUG > 8
      // printf("`%c` -> `%c` [%d]\n", disp_pos(last), disp_pos(val), counter);
      #endif 
      if(val == last){
        if(val != C_EMPTY){
          counter ++;
        }
      }else if(last == C_EMPTY){ /* val is not empty */
        last = val;
        counter = 1;
        empty_side = 1;
      }else if(last == C_BLACK){
        if(val == C_EMPTY){
          empty_side++;
          *black_p += get_weight_in_seq(counter, empty_side);
          counter = 0;
          empty_side = 1;
        }else{
          *black_p += get_weight_in_seq(counter, empty_side);
          counter = 1;
          empty_side = 0;
        }
        last = val;
      }else if(last == C_WHITE){
        if(val == C_EMPTY){
          empty_side ++;
          *white_p += get_weight_in_seq(counter, empty_side);
          counter = 0;
          empty_side = 1;
        }else{
          counter = 1;
          empty_side = 0;
        }
        last = val;
      }else{
        printf("Invalid value of `last' = %d\n", last);
        assert(0);
      }
      break;
    case 2:
      if(last == C_BLACK){
        *black_p += get_weight_in_seq(counter, empty_side);
      }else if(last == C_WHITE){
        *white_p += get_weight_in_seq(counter, empty_side);
      }
      break;
    default:
      assert(0);
      break;
  }
}

void _calc_seq_weight( struct GameState *state, 
                      int fx, int tx, int dx, 
                      int fy, int ty, int dy,
                      int *black_p, int *white_p){
  _next_pos(get_state(state, fx, fy), 0, black_p, white_p);
  int x, y;
  for(x = fx, y = fy; x < tx && x >= 0 && y < ty && y >= 0; x+=dx, y+=dy){
    // #if DEBUG > 9
    // printf("(%d, %d): ", x, y, disp_pos(get_state(state, x, y)));
    // #endif
    _next_pos(get_state(state, x, y), 1, black_p, white_p);
  }
  _next_pos(C_EMPTY, 2, black_p, white_p);
  
  #if DEBUG > 9
  putchar('`');
  for(x = fx, y = fy; x < tx && x >= 0 && y < ty && y >= 0; x+=dx, y+=dy){
    putchar(disp_pos(get_state(state, x, y)));
  }
  putchar('`');
  putchar('\n');
  printf("\tB: %d\tW: %d\n", *black_p, *white_p);
  #endif
}

void calc_weight(struct GameState *state){
  int black = 0, white = 0;
  int i;
  for(i=0; i<B_HEIGHT; i++){
    _calc_seq_weight(state, 0, B_WIDTH, 1, i, i+1, 0, &black, &white);
  }

  for(i=0; i<B_WIDTH; i++){
    _calc_seq_weight(state, i, i+1, 0, 0, B_HEIGHT, 1, &black, &white);
  }
  
  for(i=0; i<B_HEIGHT; i++){
    _calc_seq_weight(state, 0, B_WIDTH, 1, i, B_HEIGHT, 1, &black, &white);
  }
  
  for(i=0; i<B_WIDTH; i++){
    _calc_seq_weight(state, i, B_WIDTH, 1, 0, B_HEIGHT, 1, &black, &white);
  }
  
  for(i=0; i<B_HEIGHT; i++){
    _calc_seq_weight(state, 0, B_WIDTH, 1, i, B_HEIGHT, -1, &black, &white);
  }
  
  for(i=0; i<B_WIDTH; i++){
    _calc_seq_weight(state, i, B_WIDTH, -1, 0, B_HEIGHT, 1, &black, &white);
  }
  
  state -> weight = black - white;
}

struct GameState *new_state(){
  struct GameState *s = malloc(sizeof(struct GameState));
  assert(s != NULL);
  memset(s->board, C_EMPTY, sizeof(s->board));
  s->step = 0;
  calc_weight(s);
  return s;
}

struct GameState *update_state(struct GameState *old, int x, int y, enum PosState val){
  struct GameState *s = malloc(sizeof(struct GameState));
  memcpy(s->board, old->board, sizeof(old->board));
  set_state(s, x, y, val);
  calc_weight(s);
  s->step = old -> step + 1;
  return s;
}

struct GameOperation operate(int x, int y, enum Player p){
  struct GameOperation go;
  go.x = x;
  go.y = y;
  go.player = p;
  return go;
}

struct GameState *reduce_operation(
struct GameState *s, 
struct GameOperation opt){
  return update_state(
    s, 
    opt.x, opt.y, 
    opt.player == P_BLACK ? C_BLACK : C_WHITE);
}

int is_inf(int v){
  return abs(v) >= (C_INF - C_INF_RANGE);
}

int is_pos_inf(int v){
  return v > 0 && is_inf(v);
}

int is_neg_inf(int v){
  return v < 0 && is_inf(v);
}

char disp_pos(enum PosState p){
  if(p == C_BLACK){
    return 'B';
  }else if(p == C_WHITE){
    return 'W';
  }else{
    return ' ';
  }
}

void display_state(struct GameState *state){
  int i, j;
  if(state == NULL){
    puts("|| NULL STATE ||");
    return;
  }
  printf("WEIGHT = ");
  if(is_pos_inf(state -> weight)){
    printf("+INF");  
  }else if(is_neg_inf(state -> weight)){
    printf("-INF");  
  }else{
    printf("%d", state -> weight);
  }
  printf(" (STEP = %d)\n", state->step);
  
  for(i=0; i<B_HEIGHT+2; i++){
    putchar('=');
  }
  putchar('\n');
  for(i=0; i<B_WIDTH; i++){
    putchar('|');
    for(j=0; j<B_HEIGHT; j++){
      putchar(disp_pos(state->board[i][j]));
    }
    putchar('|');
    putchar('\n');
  }
  for(i=0; i<B_HEIGHT+2; i++){
    putchar('=');
  }
  putchar('\n');
}

int end_state(struct GameState *s){
  return is_inf(s->weight);
}

struct Range range(int gte, int lte){
  struct Range r;
  r.gte = gte;
  r.lte = lte;
  return r;
}

int range_empty(struct Range r){
  return r.gte > r.lte;
}

struct Range range_union(struct Range a, struct Range b){
  return range(
    max(a.gte, b.gte),
    min(a.lte, b.lte)
  );
}

int empty_state(struct GameState *s){
  int i, j;
  if(s->weight != 0) return 0;
  for(i=0; i<B_WIDTH; i++){
    for(j=0; j<B_HEIGHT; j++){
      if(get_state(s, i, j) != C_EMPTY){
        return 0;
      }
    }
  }
  return 1;
}
