<template>
  <div class="box">
    <p class="title is-3">#{{ gridNumber }}</p>
    <table class="table subtitle is-6 is-bordered is-striped is-narrow">
      <tbody>
        <tr v-for="i in iSquareMax" :key="i">
          <td v-for="j in (i == iSquareMax ? jSquareMax : nbColumns)" :key="j">
            <div class="has-text-centered">
              {{ index(i, j) }}
            </div>
          </td>
        </tr>
      </tbody>
      <p>*</p>
      <tbody>
        <tr v-for="i in iStarMax" :key="i">
          <td v-for="j in (i == iStarMax ? jStarMax : nbColumns)" :key="j">
            <div class="has-text-centered">
              {{ index(i, j) }}
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    gridNumber: Number,
    nbSquares: Number,
    nbStars: Number,
    squareList: Array,
    starList: Array,
  },
  data() {
    return {
      nbColumns: 5,
    }
  },
  computed: {
    iSquareMax: function() {
      return Math.ceil(this.nbSquares / this.nbColumns);
    },
    jSquareMax: function() {
      return (this.nbSquares % this.nbColumns) || this.nbColumns;
    },
    iStarMax: function() {
      return Math.ceil(this.nbStars / this.nbColumns);
    },
    jStarMax: function() {
      return (this.nbStars % this.nbColumns) || this.nbColumns;
    },
  },
  methods: {
    index: function(i, j) {
      return j + (i-1) * this.nbColumns;
    }
  }
}
</script>
