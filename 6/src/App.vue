<template lang="jade">
#app
  .container
    .row
      .col-xs-3.container(v-if="edit_mode")
        .row
          h3.col-xs-12 EDIT
        .row
          .form-group.col-xs-6
            label(for="inputM") M(Missionary)
            input#inputM.form-control(v-model="m", type="text", placeholder="Missionary")
          .form-group.col-xs-6
            label(for="inputN") N(Cannibal)
            input#inputN.form-control(v-model="n", type="text", placeholder="Cannibal")
        .row
          button.btn.col-xs-6(@click="set_state") OK
          button.btn.col-xs-6(@click="edit_mode = false") CANCEL
      .col-xs-3(v-else)
        h3 
          | INITIAL STATE
          | (
          a(@click="edit_mode = true") EDIT
          | )
        state-view(:state="init_state")
      .col-xs-3.container
        .row
          h3.col-xs-12 DASHBOARD
        .row(v-if="stopped && current_state")
          h4.col-xs-12.text-success(v-if="success_flag") Succeed.
          h4.col-xs-12.text-danger(v-else) Failed to find a solution.
        .row
          .col-xs-12
            .form-group
              label(for="selectSpeed") SPEED
              select.form-control#selectSpeed(@change="set_speed", v-model="sep_time")
                option(value=10)     FAST++
                option(value=100)    FAST
                option(value=500)   SLOW
                option(value=1000)  SLOW--
        .row(v-if="stopped")
          button.btn.col-xs-12(@click="init_search") SEARCH
        .row(v-else)
          button.col-xs-12.btn(v-if="timer", @click="stop_search") PAUSE
          template(v-else)
            button.btn.col-xs-6(@click="start_search")  RESUME
            button.btn.col-xs-6(@click="next_step")     STEP
      .col-xs-3
        h3 CURRENT STATE
        state-view(:state="current_state")
      .col-xs-3
        h3 TARGET STATE
        state-view(:state="dest_state")
    .row(v-if="result")
      .col-xs-12.results.display
          h3 RESULT
          template(v-for="c in result")
            state-view.state-view(:state="c")
    .row
      .col-xs-12.container(v-if="children_state")
        .row
          h3.col-xs-12 CHILDREN
        .row
          .col-xs-12.display
            template(v-for="c in children_state")
              state-view.state-view(:state="c.s", :visited = "c.v")
</template>
<script lang="coffee">
import arraySort from 'array-sort'

import Heap from 'heap'
import StateView from './StateView.vue'
import * as statetools from './state.coffee'

search_state = 
  queue: null
  visited: null

init_search = ->
  search_state.queue = []
  search_state.visited = {}

export default
  name: 'app',
  components: { StateView }
  data: () ->
    return
      init_state: null
      current_state: null
      dest_state: null
      m: 3
      n: 3
      result: null
      children_state: null
      timer: null
      sep_time: 100
      edit_mode: false
      message: null
      stopped: true
      success_flag: null
  methods:
    generate_state: (m, n)->
      @init_state = statetools.generate_init(m, n)
      @dest_state = statetools.generate_dest(m, n)
    
    init_search: ->
      @result = null
      @stopped = false
      init_search()
      search_state.queue.push(@init_state)
      @start_search()

    success: ->
      @message = "Success."
      @result = statetools.get_path(@current_state)
      @stop_search()
      @success_flag = true
      @stopped = true
    failed: ->
      @message = "Failed to find a solution."
      @stop_search() 
      @success_flag = false
      @stopped = true 
    stop_search: ->
      clearInterval(@timer) if @timer
      @timer = null
    start_search: ->
      @timer = setInterval(=>
        @next_step()
      , @sep_time)
    next_step: ->
      if search_state.queue.length == 0
        @failed()
        return
      @current_state = search_state.queue.pop()
      if statetools.equal(@current_state, @dest_state)
        @success()
        return
      children = statetools.get_children(@current_state)
      @children_state = children.map((s)->
        h = statetools.hash(s)
        {
          s, h, 
          v: search_state.visited[h]
        }
      )
      for {s, v, h} in @children_state
        continue if v
        search_state.visited[h] = true
        search_state.queue.push(s)
        if statetools.equal(s, @dest_state)
          @current_state = s
          @success()
    set_state: () ->
      @generate_state(parseInt(@m), parseInt(@n))
      @edit_mode = false
    set_speed: ->
      @stop_search()
      @sep_time = parseInt(@sep_time)
      @start_search()
  created: ->
    @generate_state(@m, @n)

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
