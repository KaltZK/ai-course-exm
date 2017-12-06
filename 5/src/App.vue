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
              state-view.col-xs-3(
                :state="s.c", 
                :switched="s.swd",
                :ignored ="s.ign",
                :updated_from_open="s.oud",
                :updated_from_close="s.cud"
              )
</template>
<script lang="coffee">
import arraySort from 'array-sort'

import Heap from 'heap'
import StateView from './StateView.vue'
import * as statetools from './state.coffee'

search_state =
  heap: null
  open: {}
  close: {}

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
      open_counter: 0
      close_counter: 0
  computed:
    queue_length: ->
      @queue_tail - @queue_head
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
      search_state.heap = new Heap((a, b) => 
        a.p - b.p
      )
      search_state.open = {}
      search_state.close = {}
      @queue_head = @queue_tail = 0
      @open_counter = @close_counter = 0

      search_state.heap.push(@init_state)
      @open_add(@init_state)
      @queue_tail++
    
    open_add: (s) ->
      search_state.open[s.hash] = s
      @open_counter++

    open_del: (s) ->
      delete search_state.open[s.hash]
      @open_counter--
    
    close_add: (s) ->
      search_state.close[s.hash] = s
      @close_counter++

    close_del: (s) ->
      delete search_state.close[s.hash]
      @close_counter--

    set_speed: ->
      @stop()
      @search_start()
    
    search_start: ->
      @timer = setInterval(=>
        @failed() if @queue_tail <= @queue_head
        @current_state = search_state.heap.pop()
        
        @queue_head++
        @success() if statetools.equal(@current_state, @target_state)

        @open_del(@current_state)
        @close_add(@current_state)

        children = statetools.children(@current_state)
        children = children.map((c) =>
          opened_self = search_state.open[c.hash]
          closed_self = search_state.close[c.hash]
          swd = ign = oud = cud = false

          if opened_self or closed_self
            ign = true
            if opened_self and c.p < opened_self.p
              statetools.replace(c, opened_self)
              search_state.heap.heapify()
              oud = true
            else if closed_self and c.p < closed_self.p
              @close_del(c)
              @open_add(c)
              search_state.heap.push(c)
              cud = true


          {c, swd, ign, oud, cud}
        )
        @children_state = children
        for {c, cud, oud, ign} in children
          unless ign
            @open_add(c)
            search_state.heap.push(c)
            @queue_tail++
            if statetools.equal(c, @target_state)
              @current_state = c
              @success()
              break
        @round++

      , parseInt(@time_sep))
    a_star: ->
      @stop_displaying()
      @init_search()
      @search_start()
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
