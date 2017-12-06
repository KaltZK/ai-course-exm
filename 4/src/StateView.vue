<template lang="jade">
div(:class="{visited: visited}")
  template(v-if="state")
    p D(x): {{state.distance}}
    p H(x): {{state.h}}
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
  props: ['state', 'visited']
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
