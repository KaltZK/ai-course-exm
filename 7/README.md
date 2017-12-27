# 使用Alpha-Beta剪枝下五子棋

## 编译

### 使用Makefile编译


```bash
make build
```

或交叉编译到Windows

```bash
make build_win32
```

### 直接编译

```bash
gcc -Wall -o main main.c state_helpers.c search.c
```

## 运行

直接运行即可

会打印出每一步的操作

黑白交替进行

## 说明

#### main.c

程序入口

#### state_helpers.h

声明状态的数据结构及处理状态的函数

包括以下类型的声明:

* GameState 状态
* PosState 棋子类型
* Player 玩家标记
* Range 由alpha与beta构成的区间

包括以下函数:

* calc_weight 计算状态的权重
* new_state 生成空状态
* update_state 从已有状态放置棋子生成新状态
* is_inf 是否是正/负无穷大
* is\_pos\_inf 是否是正无穷大
* is\_neg\_inf 是否是负无穷大
* display\_state 显示状态
* range 生成区间
* range\_empty 是否是空区间
* range\_union 对两个区间取交集
* end\_state 是否是目标状态(一方获胜)
* empty_state 是否是初始状态

#### search.h

用于搜索的函数:

* search\_by\_black 由黑棋搜索
* search\_by\_white 由白棋搜索
