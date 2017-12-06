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
            p QUEUE: {{queue_tail - queue_head}}
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
        .row
          button.btn.col-xs-6(@click="generate_state") REROLL
          button.btn.col-xs-6(@click="i_am_feeling_lucky") I'm Feeling Lucky 
        .row
          button.btn.col-xs-12(@click="bfs") BFS
          // button.btn.col-xs-6(@click="dfs") DFS
      .col-xs-3
        h3 CURRENT STATE
        state-view(:state="current_state")
      .col-xs-3
        h3 TARGET STATE
        state-view(:state="target_state")
    .row.results(v-if="results")
      .col-xs-12
        h3 RESULT
        div
          template(v-for="(r, i) in results")
            state-view.state-view(:state="r")
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

import StateView from './StateView.vue'
import * as statetools from './state.coffee'

bfs_state =
  queue: []
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
      bfs_state.queue.length
  methods:
    generate_state: ->
      @stop()
      @stop_displaying()
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
    failed: ->
      @message = 'Failed to reach the target.'
      @stop()
    success: ->
      @message = 'Succeed.'
      @stop()
      @results = statetools.get_seq(@current_state)
      @display()
    display: ->
      @display_timer = setInterval(=>
        @display_index++
        (@display_index = 0) if @display_index == @results.length 
      , 1000)
    stop_displaying: ->
      if(@display_timer)
        clearInterval @display_timer
        @display_timer = null
      @results = null
      @display_index = 0

    init_search: ->
      @round = 0
      bfs_state.queue = []
      bfs_state.visited = {}
      @queue_head = @queue_tail = 0

    set_speed: ->
      @stop()
      @bfs_start()
    bfs_start: ->
      @timer = setInterval(=>
        @failed() if bfs_state.queue.length == 0
        @current_state = bfs_state.queue.shift()
        @queue_head++
        @success() if statetools.equal(@current_state, @target_state)

        bfs_state.visited[@current_state.hash] = 1
        children = statetools.children(@current_state)
        children = arraySort(children, 'h')
        # children = children.filter((s)=> !bfs_state.visited[s.])
        children = children.map((c) =>
          v: bfs_state.visited[c.hash],
          c: c
        )
        @children_state = children
        for {c, v} in children
          continue if v
          bfs_state.visited[c.hash] = 1
          bfs_state.queue.push c
          @queue_tail++
          if statetools.equal(c, @target_state)
            @current_state = c
            @success()
            break
        # @queue = arraySort(@queue, 'h')
        @round++

      , parseInt(@time_sep))
    bfs: ->
      @stop_displaying()
      @init_search()
      bfs_state.queue.push @init_state
      bfs_state.visited[@init_state.hash] = true
      @bfs_start()
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
.results{
  background-color: #A5DEE4;
  overflow-x: scroll;
  white-space: nowrap;
}
.state-view{
  display: inline-block;
  margin-left:  1rem;
  margin-right: 1rem;
}
</style>
