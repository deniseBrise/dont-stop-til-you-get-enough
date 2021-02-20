<template>
  <section class="section">
    <div class="columns is-multiline is-mobile">
      <div class="column is-narrow" v-for="i in nbGrids" :key="i">
        <mba-grid :gridNumber="i" :grid="grids[i-1]||{}" :maxSquares="maxSquares" :maxStars="maxStars" :draw="draw"></mba-grid>
      </div>
    </div>
  </section>
</template>

<script>
import MbaGrid from '@/components/Grid.vue'

export default {
  props: {
    grids: Array,
    nbGrids: Number,
    draw: Object,
    maxSquares: Number,
    maxStars: Number,
  },
  components: {
    MbaGrid,
  },
}
</script>
