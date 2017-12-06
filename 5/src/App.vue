<template lang="jade">
#app
  .container
    .row
      .col-xs-3(v-if="!edit_init_state", @click="start_edit")
        h3 INITIAL STATE
        state-view(:state="init_state")
      .col-xs-3.container(v-else)
        .row
          h3 SET INITIAL STATE
          textarea.col-xs-12(
            v-model="edit_content",
            placeholder="Initial State", 
            type="text", 
            rows="3")
        .row
          .col-xs-12.container
            .row
              button.btn.col-xs-12(@click="stop_edit")
                | SET
            .row
              button.btn.col-xs-12(@click="edit_init_state = false")
                | CANCEL
      .col-xs-3.container
        .row
          .col-xs-12
            h3 DASHBOARD
        .row
          .col-xs-12
            p ROUND: {{round}}
            p HEAP: {{queue_tail - queue_head}}
        .row
          .col-xs-12
            h3 {{message}}
        .row
          .col-xs-12
            .form-group
              label(for="selectSpeed") SPEED
              select.form-control#selectSpeed(@change="set_speed", v-model="time_sep")
                option(value=0)     FAST++
                option(value=50)    FAST
                option(value=200)   SLOW
                option(value=1000)   SLOW--
        .row(v-if="current_state")
          button.col-xs-6.btn(v-if="timer", @click="stop()") PAUSE
          template(v-else)
            button.btn.col-xs-3(@click="search_start()") RESUME
            button.btn.col-xs-3(@click="search_step()")  STEP
          button.col-xs-6.btn(@click="snapshot") SHOT OPEN/CLOSE
        .row
          button.btn.col-xs-6(@click="generate_state") REROLL
          button.btn.col-xs-6(@click="i_am_feeling_lucky") I'm Feeling Lucky 
        .row
          button.btn.col-xs-12(@click="a_star") A*
          // button.btn.col-xs-6(@click="dfs") DFS
      .col-xs-3
        h3 CURRENT STATE
        state-view(:state="current_state")
      .col-xs-3
        h3 TARGET STATE
        state-view(:state="target_state")
    .row.results.display(v-if="results")
      .col-xs-12
        h3 RESULT
        div
          template(v-for="(r, i) in results")
            state-view.state-view(:state="r")
    .row.display(v-if="open_snapshot")
      .col-xs-12
        h3 
          | OPEN TABLE SNAPSHOT
          a.small(@click="open_snapshot = null") [x]
        div
          template(v-for="(c, i) in open_snapshot")
            state-view.state-view(:state="c")
    .row.display(v-if="close_snapshot")
      .col-xs-12
        h3 
          | CLOSE TABLE SNAPSHOT
          a.small(@click="close_snapshot = null") [x]
        div
          template(v-for="(c, i) in close_snapshot")
            state-view.state-view(:state="c")
    .row
      .col-xs-12
        h3 CHILDREN STATE
        .container
          .row
            template(v-for="s in children_state")
              state-view.col-xs-3(:state="s.c", :visited="s.v")
</template>
<script lang="coffee">
import arraySort from 'array-sort'

import Heap from 'heap'
import StateView from './StateView.vue'
import * as statetools from './state.coffee'

search_state =
  heap: null
  visited: {}

export default
  name: 'app',
  components: { StateView }
  data: () ->
    return
      init_state: null
      target_state: statetools.TARGET
      timer: null
      time_sep: 0
      current_state: null
      children_state: []
      message: ''
      round: 0
      display_timer: null
      results: null
      display_index: 0
      queue_tail: 0
      queue_head: 0
      edit_init_state: false
      edit_content: ''
      open_snapshot: null
      close_snapshot: null
  computed:
    queue_length: ->
      @queue_tail - @queue_head
  methods:
    generate_state: ->
      @stop()
      @init_state = statetools.random_state()

    start_edit: ->
      @edit_content = @init_state
                        .arr.map((i)=> i.toString()).join('')
                        .split(/(\d{3})/)
                        .filter((s)=> s.length)
                        .join("\n")
      @edit_init_state = true

    stop_edit: ->
      arr = @edit_content
          .split('')
          .filter((s)=> s >= '0' && s <= '9')
          .map((i) => parseInt(i))
      @init_state = statetools.from_array(arr)
      @init_search()
      @edit_init_state = false
    
    i_am_feeling_lucky: ->
      it = setInterval(=>
        s = @generate_state()
        if s.h < 10
          clearInterval it
      , 50)
    stop: ->
      clearInterval(@timer) if @timer
      @timer = null
    failed: ->
      @message = 'Failed to reach the target.'
      @stop()
    success: ->
      @message = 'Succeed.'
      @stop()
      @results = statetools.get_seq(@current_state)

    init_search: ->
      @round = 0
      search_state.heap = new Heap((a, b) => 
        a.p - b.p
      )
      search_state.visited = {}
      @queue_head = @queue_tail = 0
      @queue_tail++

    set_speed: ->
      @stop()
      @search_start()
    search_step: ->
        # console.log @queue_head, @queue_tail
        @failed() if @queue_tail <= @queue_head
        @current_state = search_state.heap.pop()
        @queue_head++
        @success() if statetools.equal(@current_state, @target_state)

        search_state.visited[@current_state.hash] = @current_state
        children = statetools.children(@current_state)
        children = arraySort(children, 'h')
        children = children.map((c) =>
          v: search_state.visited[c.hash],
          c: c
        )
        @children_state = children
        for {c, v} in children
          if v
            if c.p < v # 如果需要再次加入OPEN表
              search_state.visited[c.hash] = c  # 从CLOSE取出(其实就是更新visited)
              search_state.heap.push(c)           # 重新加入OPEN表
            # else 无事发生
          else
            search_state.visited[c.hash] = c
            search_state.heap.push c
            @queue_tail++
            if statetools.equal(c, @target_state)
              @current_state = c
              @success()
              break
        # @queue = arraySort(@queue, 'h')
        @round++

    search_start: ->
      @timer = setInterval(=>
        @search_step()
      , parseInt(@time_sep))
    a_star: ->
      @init_search()
      search_state.heap.push @init_state
      search_state.visited[@init_state.hash] = @init_state
      @search_start()
    snapshot: ->
      heap = search_state.heap.toArray()
      visited = Object.assign({}, search_state.visited)
      open = []
      close = []
      for c in heap
        delete visited[c.hash]
        open.push(c)
      for c in Object.values(visited)
        close.push(c)
      @open_snapshot = open
      @close_snapshot = close

  
  created: ->
    @generate_state()

</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}
.row{
  margin-top: 0.1rem;
}
.display{
  overflow-x: scroll;
  white-space: nowrap;
}
.results{
  background-color: #A5DEE4;
}
.state-view{
  display: inline-block;
  margin-left:  1rem;
  margin-right: 1rem;
}
</style>
