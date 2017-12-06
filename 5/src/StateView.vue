<template lang="jade">
div(:class="get_class()")
  template(v-if="state")
    p D(x): {{state.distance}}
    p H(x): {{state.h}}
    p F(x): {{state.p}}
    p(v-if="update_from_open") UPDATED ON OPEN
    p(v-if="update_from_close") REOPENED
    p(v-if="switched") SWITCHED WITH PARENT
    table
      tr(v-for="row in 3")
        template(v-for="col in 3")
          td.non-empty(v-if="state.arr[(row-1) * 3 + (col-1)] != 0")
            {{state.arr[(row-1) * 3 + (col-1)]}}
          td.empty(v-else)
  template(v-else)
    p N/A
</template>

<script lang="coffee">
export default
  name: 'state-view'
  props: ['state', 'ignored', 'switched', 'update_from_open', 'update_from_close']
  methods: 
    get_class: ->
      if @switched or @update_from_close or @update_from_open
        'updated'
      else if @ignored
        'ignored'
      else
        ''
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

.updated{
  background-color: rgb(250, 214, 137);
}

.ignored{
  background-color: #FEDFE1;
}
</style>
