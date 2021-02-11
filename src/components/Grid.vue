<template>
  <div class="box">

    <p class="title is-3">#{{ gridNumber }}</p>

    <table class="table subtitle is-6 is-bordered is-narrow container">
      <b-loading :is-full-page="false" v-model="isLoading"></b-loading>
      <tbody>
        <tr v-for="i in iSquareMax" :key="i">
          <td v-for="j in (i == iSquareMax ? jSquareMax : nbColumns)" :key="j">
            <div class="has-text-centered" :class="selectedSquareClass(i, j)">
              {{ index(i, j) }}
            </div>
          </td>
        </tr>
      </tbody>
      
      <p>*</p>

      <tbody>
        <tr v-for="i in iStarMax" :key="i">
          <td v-for="j in (i == iStarMax ? jStarMax : nbColumns)" :key="j">
            <div class="has-text-centered" :class="selectedStarClass(i, j)">
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
    grid: Object,
    maxSquares: Number,
    maxStars: Number,
  },
  data() {
    return {
      nbColumns: 5,
    }
  },
  computed: {
    isLoading: function() {
      return Object.keys(this.grid).length === 0 && this.grid.constructor === Object
    },
    iSquareMax: function() {
      return Math.ceil(this.maxSquares / this.nbColumns);
    },
    jSquareMax: function() {
      return (this.maxSquares % this.nbColumns) || this.nbColumns;
    },
    iStarMax: function() {
      return Math.ceil(this.maxStars / this.nbColumns);
    },
    jStarMax: function() {
      return (this.maxStars % this.nbColumns) || this.nbColumns;
    },
  },
  methods: {
    index: function(i, j) {
      return j + (i-1) * this.nbColumns;
    },
    isSelectedSquare: function(i, j) {
      if (this.grid.squares) {
        return this.grid.squares.includes(this.index(i, j));
      }
      return false;
    },
    isSelectedStar: function(i, j) {
      if (this.grid.stars) {
        return this.grid.stars.includes(this.index(i, j));
      }
      return false;
    },
    selectedSquareClass: function(i, j) {
      if (this.isSelectedSquare(i, j)) {
        return ['has-text-info', 'has-text-weight-bold' ];
      }
      return [ 'has-text-grey-light' ];
    },
    selectedStarClass: function(i, j) {
      if (this.isSelectedStar(i, j)) {
        return ['has-text-danger', 'has-text-weight-bold' ];
      }
      return [ 'has-text-grey-light' ];
    },
  }
}
</script>
