<template lang="jade">
div(:class="{visited: visited}")
  template(v-if="state")
    // p {{hash(state)}}
    table.table.table-bordered.table-condensed
      tr
        th 
        th L
        th 
        th R
      tr
        td M
        td {{state.lb.m}}
        td(colspan="b") {{ state.b == 0 ? 'L' : 'R' }}
        td {{state.rb.m}}
      tr
        td C
        td {{state.lb.c}}
        td(colspan="b")
        td {{state.rb.c}}
  template(v-else)
    p N/A
</template>

<script lang="coffee">
import * as statetools from './state.coffee'
export default
  name: 'state-view'
  props: ['state', 'visited']
  methods:
    hash: (s) ->
      statetools.hash s
</script>

<style scoped>
td{
  font-size: 2rem;
  width: 1.5rem;
  height: 1.5rem;
  padding: 0.3rem;
  color: black;
}
td.non-empty{
  background-color: #A8D8B9;
}
td.empty{
  background-color: white;
}
.visited{
  background-color: #FEDFE1;
}
</style>
