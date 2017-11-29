<template lang="jade">
#app
  .container
    .row
      .col-xs-3
        h3 INITIAL STATE
        state-view(:state="init_state")
      .col-xs-3.container
        .row
          .col-xs-12
            h3 DASHBOARD
        .row
          .col-xs-12
            p ROUND: {{round}}
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
        template(v-for="offset in 4")
          state-view.col-xs-3(:state="results[(display_index + offset) % results.length]")
    .row
      .col-xs-12
        h3 CHILDREN STATE
        .container
          .row
            template(v-for="s in children_state")
              state-view.col-xs-3(:state="s")
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
  computed:
    queue_length: ->
      bfs_state.queue.length
  methods:
    generate_state: ->
      @stop()
      @stop_displaying()
      @init_state = statetools.random_state()
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

    set_speed: ->
      @stop()
      @bfs_start()
    bfs_start: ->
      @timer = setInterval(=>
        @failed() if bfs_state.queue.length == 0
        @current_state = bfs_state.queue.shift()
        @success() if statetools.equal(@current_state, @target_state)

        bfs_state.visited[@current_state.hash] = 1
        children = statetools.children(@current_state).filter((c) => 
          ! bfs_state.visited[c.hash]
        )
        children = arraySort(children, 'h')
        @children_state = children
        # console.log @children_state
        for c in @children_state
          bfs_state.visited[c.hash] = 1
          bfs_state.queue.push c
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
}
</style>
