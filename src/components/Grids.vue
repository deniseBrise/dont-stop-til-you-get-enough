<template>
  <section class="section">
    <div class="columns is-multiline is-mobile">
      <div class="column is-narrow" v-for="i in nbGrids" :key="i">
        <mba-grid :gridNumber="i" :grid="grids[i-1]||{}" :nbSquares="nbSquares" :nbStars="nbStars"></mba-grid>
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
    nbSquares: Number,
    nbStars: Number,
  },
  components: {
    MbaGrid,
  },
}
</script>
