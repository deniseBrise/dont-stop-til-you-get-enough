<template>
  <div class="box">
    <div class="tile is-ancestor">
      <div class="tile">
      </div>
      <div class="tile">
        <b-field label="Tirage à vérifier" :type="inputType" :message="inputMessage">
          <b-input v-model="drawStr" :placeholder="inputPlaceholder"></b-input>
          <p class="control">
            <b-button class="button is-primary" :disabled="!isValidDraw" @click="setFilter">Go</b-button>
          </p>
        </b-field>
      </div>
      <div class="tile">
      </div>
    </div>
  </div>
</template>

<script>
export default {
  mounted: function() {
    this.drawStr = this.draw2str(this.initialFilter);
  },
  props: {
    initialFilter: Object,
    maxSquares: Number,
    maxStars: Number,
    nbSquares: Number,
    nbStars: Number,
  },
  data() {
    return {
      drawStr: '',
    }
  },
  computed: {
    draw: function() {
      return this.str2draw(this.drawStr);
    },
    isValidDraw: function() {
      return this.isValid(this.draw);
    },
    inputPlaceholder: function() {
      let draw = { squares: [], stars: [] };
      for (let i = 0 ; i < this.nbSquares ; i++) {
        draw.squares.push('X');
      }
      for (let i = 0 ; i < this.nbStars ; i++) {
        draw.stars.push('X');
      }
      return this.draw2str(draw);
    },
    inputType: function() {
      if (this.drawStr) {
        return (this.isValidDraw ? "is-success" : "is-danger");
      }
      return "";
    },
    inputMessage: function() {
      let draw = this.draw;
      if ((((draw||{}).squares||[]).length != this.nbSquares) || (((draw||{}).stars||[]).length != this.nbStars)) {
        return 'Doit contenir ' + this.nbSquares + ' numéro' + (this.nbSquares > 1 ? 's' : '') + ' et ' + this.nbStars + ' étoile' + (this.nbStars ? 's' : '');
      }
      for (let square of draw.squares) {
        if (isNaN(square) || square < 1 || square > this.maxSquares) {
          return 'Les numéros doivent être compris entre 1 et ' + this.maxSquares;
        }
        if (draw.squares.filter(x => x == square).length > 1) {
          return 'Le numéro ' + square + ' ne doit être présent qu\'une seule fois';
        }
      }
      for (let star of draw.stars) {
        if (isNaN(star) || star < 1 || star > this.maxStars) {
          return 'Les numéros étoiles doivent être compris entre 1 et ' + this.maxStars;
        }
        if (draw.stars.filter(x => x == star).length != 1) {
          return 'Le numéro étoile ' + star + ' ne doit être présent qu\'une seule fois';
        }
      }
      return '';
    },
  },
  methods: {
    draw2str: function(draw) {
      let drawSquares = ((draw||{}).squares||[]);
      let drawStars = ((draw||{}).stars||[]);
      let squares = '';
      let stars = '';
      for (let square of drawSquares) {
        squares += (squares.length == 0 ? '' : '-') + square;
      }
      for (let star of drawStars) {
        stars += (stars.length == 0 ? '*' : '-') + star;
      }
      return squares + stars;
    },
    str2draw: function(str) {
      return { squares: ((str.split('*')[0]||'').split('-')||'').map(x => parseInt(x)), stars: ((str.split('*')[1]||'').split('-')||'').map(x => parseInt(x)) };
    },
    isValid: function(draw) {
      if ((((draw||{}).squares||[]).length == this.nbSquares) && (((draw||{}).stars||[]).length == this.nbStars)) {
        for (let square of draw.squares) {
          if (isNaN(square) || square < 1 || square > this.maxSquares || draw.squares.filter(x => x == square).length != 1) {
            return false;
          }
        }
        for (let star of draw.stars) {
          if (isNaN(star) || star < 1 || star > this.maxStars || draw.stars.filter(x => x == star).length != 1) {
            return false;
          }
        }
        return true;
      }
      return false;
    },
    setFilter: function() {
      if (this.isValidDraw) {
        this.$emit('setFilter', this.draw);
      }
    },
  },
}
</script>
