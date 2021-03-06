<template>
  <div>

    <!-- Hidden navbar to fix dynamic offset -->
    <b-navbar>
      <template #start>
        <b-navbar-item>
          <b-field label="Total">
            <p class="title">€</p>
          </b-field>
        </b-navbar-item>
      </template>
    </b-navbar>

    <!-- Real navbar -->
    <b-navbar class="box" centered transparent fixed-top>
      <template #start>

        <b-navbar-item class="mx-1">
          <b-field label="Total">
            <p class="title">{{ totalPrice | currency }}</p>
          </b-field>
        </b-navbar-item>
        <b-navbar-item class="mx-3">
          <b-field label="Gain">
            <p class="title is-4">{{ estimatedGain | currency }}</p>
          </b-field>
        </b-navbar-item>

        <b-navbar-item class="mx-3">
          <b-field label="Nombre de grilles">
            <b-numberinput v-model="params.nbGrids" min="0" max="10000" step="1" :exponential=".5" :editable="false" controls-position="compact" controls-rounded></b-numberinput>
          </b-field>
        </b-navbar-item>

        <b-navbar-item class="mx-3">
          <b-field grouped label="Jeu et Options">
            <b-switch v-model="params.gridType" @input="params.draw = {}" passive-type='is-primary'>{{ params.gridType ? 'Loto' : 'Euro' }}</b-switch>
            <b-checkbox v-model="params.isOption">{{ params.gridType ? '2nd tirage' : 'Etoile+' }}</b-checkbox>
          </b-field>
        </b-navbar-item>

        <b-navbar-item class="mx-2">
          <b-field label="Actions">
            <b-button @click="newSeed">Suffle</b-button>
            <b-button :type="{ 'is-primary': params.isVerify }" @click="params.isVerify = !params.isVerify">Verify</b-button>
          </b-field>
        </b-navbar-item>

      </template>
    </b-navbar>

    <div v-if="params.isVerify">
      <mba-draw @setFilter="setDraw" :initialFilter="params.draw" :maxSquares="squareMaxValue" :maxStars="starMaxValue" :nbSquares="squareMaxNumber" :nbStars="starMaxNumber"></mba-draw>

      <div class="section columns is-multiline is-mobile" v-for="draw in bestDraws" v-show="draw.grids.length" :key="draw.rank">
        <p class="title is-1">{{ rankTitle(draw.rank, squareMaxNumber + starMaxNumber) }}</p>
        <mba-grids :grids="draw.grids" :nbGrids="draw.grids.length" :draw="params.draw" :maxSquares="squareMaxValue" :maxStars="starMaxValue"></mba-grids>
      </div>  
    </div>

    <div v-else>
      <mba-grids :grids="grids" :nbGrids="params.nbGrids" :draw="{}" :maxSquares="squareMaxValue" :maxStars="starMaxValue"></mba-grids>
    </div>

  </div>
</template>

<script>
import MbaGrids from '@/components/Grids.vue'
import MbaDraw from '@/components/Draw.vue'
import {Mutex} from 'async-mutex';

const processingMutex = new Mutex();
const currencyFormatter = new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' });

export default {
  created: function() {
    const querySeed = this.query2seed(this.$route.query.seed);
    const queryNbGrids = (this.$route.query.nbGrids||0);
    this.params.nbGrids = (parseInt(queryNbGrids, 10)||0);
    this.params.gridType = ((this.$route.query.gridType == 'true')||false);
    this.params.isOption = ((this.$route.query.isOption == 'true')||false);
    this.params.seed = (querySeed||this.shuffleSeed());
    this.params.isVerify = ((this.$route.query.isVerify == 'true')||false);
    this.params.draw = (this.query2draw(this.$route.query.draw)||{});
  },
  components: {
    MbaGrids,
    MbaDraw,
  },
  data() {
    return {
      grids: [],
      params: {
        nbGrids: 0,
        gridType: false,
        isOption: false,
        seed: [],
        isVerify: false,
        draw: {},
      },
      squaresData: {
        index: 0,
        commonNumber: 0,
        loopOffset: 0,
      },
      starsData: {
        index: 0,
        commonNumber: 0,
        loopOffset: 0,
      },
    }
  },
  computed: {
    seedMaxValue: function() {
      return 50;
    },
    squareSeed: function() {
      return this.filterSeed(this.squareMaxValue);
    },
    starSeed: function() {
      return this.filterSeed(this.starMaxValue);
    },
    squareDraws: function() {
      return this.grids.map(x => x.squares);
    },
    starDraws: function() {
      return this.grids.map(x => x.stars);
    },
    squareMaxNumber: function() {
      return this.params.gridType ? 5 : 5;
    },
    squareMaxValue: function() {
      return this.params.gridType ? 49 : 50;
    },
    starMaxNumber: function() {
      return this.params.gridType ? 1 : 2;
    },
    starMaxValue: function() {
      return this.params.gridType ? 10 : 12;
    },
    totalNumber: function() {
      return this.squareMaxNumber + this.starMaxNumber;
    },
    gridPrice: function() {
      return this.params.gridType ? 2.20 : 2.50;
    },
    optionPrice: function() {
      return this.params.gridType ? 0.80 : 1.00;
    },
    totalPrice: function() {
      return this.params.nbGrids * (this.gridPrice + (this.params.isOption ? this.optionPrice : 0));
    },
    estimatedGain: function() {
      let gain = 0;
      for (let i = 0 ; i < this.params.nbGrids ; i++) {
        gain += this.estimateGridGain(this.grids[i]);
      }
      return gain;
    },
    bestDraws: function() {
      let bestDraws = [];
      for (let i = this.squareMaxNumber + this.starMaxNumber ; i > 0 ; i--) {
        let grids = this.getBestGrids(i);
        bestDraws.push({ rank: i, grids: grids });
      }
      return bestDraws;
    },
  },
  methods: {
    shuffleSeed: function() {
      var a = Array.from({length: this.seedMaxValue}, (_, i) => i + 1);
      for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
      }
      return a;
    },
    newSeed: function() {
      this.grids = [];
      this.params.seed = this.shuffleSeed();
    },
    seed2query: function(seed) {
      if (Array.isArray(seed)) {
        return seed.join();
      }
      return null;
    },
    query2seed: function(query) {
      if (typeof query == 'string') {
        query = query.split(',').map(function(value) {
          return parseInt(value);
        });
        if (query.length == this.seedMaxValue) {
          for (var i = 1 ; i <= this.seedMaxValue ; i++) {
            if (!query.includes(i)) {
              return null;
            }
          }
          return query;
        }
      }
      return null;
    },
    draw2query: function(draw) {
      let array = [].concat(((draw||{}).squares||[])).concat(((draw||{}).stars||[]));
      if (array.length > 0) {
        return array.join();
      }
      return null;
    },
    query2draw: function(query) {
      if (typeof query == 'string') {
        query = query.split(',').map(function(value) {
          return parseInt(value);
        });
        if (query.length == (this.squareMaxNumber + this.starMaxNumber)) {
          const squares = query.slice(0, this.squareMaxNumber);
          const stars = query.slice(this.squareMaxNumber);
          for (const square of squares) {
            if (square <= 0 || square > this.squareMaxValue || this.getCommonNumber(squares, [ square ]) != 1) {
              return null;
            }
          }
          for (const star of stars) {
            if (star <= 0 || star > this.starMaxValue || this.getCommonNumber(stars, [ star ]) != 1) {
              return null;
            }
          }
          return { squares, stars };
        }
      }
      return null;
    },
    setDraw: function(draw) {
      this.params.draw = draw;
    },
    rankTitle: function(rank, max) {
      if (rank == max) {
        return 'Tous les bons numéros !!! BANG BANG';
      }
      return rank + ' bon' + (rank > 1 ? 's' : '') + ' numéro' + (rank > 1 ? 's' : '');
    },
    estimateGridGain: function(grid) {
      let nbSquare = this.getCommonNumber(((grid||{}).squares||[]), this.params.draw.squares);
      let nbStar = this.getCommonNumber(((grid||{}).stars||[]), this.params.draw.stars);
      if (this.params.gridType) {
        return this.estimateLotoGain(nbSquare, nbStar, this.params.isOption);
      }
      return this.estimateEuroGain(nbSquare, nbStar, this.params.isOption);
    },
    estimateLotoGain(nbSquare, nbStar) {
      if (nbSquare == 5) {
        return nbStar == 1 ? 2000000 : 100000;
      }
      if (nbSquare == 4) {
        return nbStar == 1 ? 1000 : 400;
      }
      if (nbSquare == 3) {
        return nbStar == 1 ? 50 : 20;
      }
      if (nbSquare == 2) {
        return nbStar == 1 ? 10 : 4.40;
      }
      if (nbStar == 1) {
        return 2.20;
      }
      return 0;
    },
    estimateSuperLotoGain(nbSquare, nbStar) {
      if (nbSquare == 5) {
        return nbStar == 1 ? 13000000 : 150000;
      }
      if (nbSquare == 4) {
        return nbStar == 1 ? 2000 : 1000;
      }
      if (nbSquare == 3) {
        return nbStar == 1 ? 100 : 50;
      }
      if (nbSquare == 2) {
        return nbStar == 1 ? 20 : 8;
      }
      if (nbStar == 1) {
        return 3;
      }
      return 0;
    },
    estimateGrandLotoGain(nbSquare, nbStar) {
      if (nbSquare == 5) {
        return nbStar == 1 ? 15000000 : 200000;
      }
      if (nbSquare == 4) {
        return nbStar == 1 ? 5000 : 2000;
      }
      if (nbSquare == 3) {
        return nbStar == 1 ? 200 : 100;
      }
      if (nbSquare == 2) {
        return nbStar == 1 ? 30 : 12;
      }
      if (nbStar == 1) {
        return 5;
      }
      return 0;
    },
    estimateEuroGain(nbSquare, nbStar, option) {
      if (nbSquare == 5) {
        if (nbStar == 2)
          return 210000000;
        if (nbStar == 1)
          return option ? 204933 : 200738;
        return 20851;
      }
      if (nbSquare == 4) {
        if (nbStar == 2)
          return option ? 1597 : 1299;
        if (nbStar == 1)
          return option ? 138 : 120;
        return 39;
      }
      if (nbSquare == 3) {
        if (nbStar == 2)
          return option ? 66 : 57;
        if (nbStar == 1)
          return option ? 14.10 : 11.26;
        return 9.32;
      }
      if (nbSquare == 2) {
        if (nbStar == 2)
          return option ? 16 : 14;
        if (nbStar == 1)
          return option ? 8.02 : 5.58;
        return 4;
      }
      if (nbSquare == 1) {
        if (nbStar == 2)
          return option ? 10.30 : 6.75;
        return 0;
      }
      if (nbStar == 2)
        return option ? 10.03 : 0;
      if (nbStar == 1)
        return option ? 2.50 : 0;
      return 0;
    },
    filterSeed: function(max) {
      return this.params.seed.filter(function (value) {
        return value <= max;
      });
    },
    getCommonNumber: function(valueList, refArray) {
      let commonNumber = 0;
      if (valueList && refArray) {
        for (const value of valueList) {
          if (refArray.includes(value)) {
            commonNumber++;
          }
        }
      }
      return commonNumber;
    },
    isValidNextValue: function(previousDraws, currentDraw, nextValue, startFrom, commonMax) {
      if (currentDraw.includes(nextValue)) {
        return false;
      }
      let array = currentDraw.slice(0);
      array.push(nextValue);
      for (const i in this.grids) {
        if (i >= startFrom 
          && this.getCommonNumber(previousDraws[i], array) > commonMax) {
          return false;
        }
      }
      return true;
    },
    nextDraw: function(seed, draws, data, maxNumber, maxValue) {
      let draw = [];

      while (draw.length < maxNumber) {
        // save initial index
        let initIndex = data.index;
        // loop until pushing a value to array
        while (initIndex > -42) {
          // increment start index
          data.index = (data.index + 1) % maxValue;
          // get seed value at index
          let nextValue = seed[data.index];
          // test if this value is acceptable considering existing grids
          if (this.isValidNextValue(draws, draw, nextValue, data.loopOffset, data.commonNumber)) {
            draw.push(nextValue);
            break;
          }
          // after a full loop over seeds without success...
          if (initIndex == data.index) {
            // ...increment the number of possible common numbers
            data.commonNumber = (data.commonNumber + 1) % maxNumber;
            // if common number was reset
            if (data.commonNumber == 0) {
              // set new offset to start index
              data.loopOffset = draws.length;
            }
          }
        }
      }

      return draw;
    },
    async processNewGrids() {
      // use a different starting index for squares and stars
      if (this.grids.length == 0) {
        this.squaresData.index = (this.params.seed[0] % this.squareMaxValue);
        this.starsData.index = (this.params.seed[1] % this.starMaxValue);
      }
      // fill grids with generated values
      processingMutex.runExclusive(
        () => {
          while (this.grids.length < this.params.nbGrids) {
            this.grids.push(
            {
              squares: this.nextDraw(this.squareSeed, this.squareDraws, this.squaresData, this.squareMaxNumber, this.squareMaxValue),
              stars: this.nextDraw(this.starSeed, this.starDraws, this.starsData, this.starMaxNumber, this.starMaxValue),
            });
          }
        }
      );
    },
    getBestGrids: function(rank) {
      let getCommonNumber = this.getCommonNumber;
      let draw = this.params.draw;
      let grids = this.grids;
      let nbGrids = this.params.nbGrids;
      return grids.filter(function (grid) {
          return grids.indexOf(grid) < nbGrids && getCommonNumber(grid.squares, draw.squares) + getCommonNumber(grid.stars, draw.stars) == rank;
        });
    },
  },
  filters: {
    currency: function(value) {
      return currencyFormatter.format(value);
    },
  },
  watch: {
    params: {
      deep: true,
      handler() {
        // update url query
        this.$router.push({
          query: { 
            nbGrids: this.params.nbGrids,
            gridType: this.params.gridType,
            isOption: this.params.isOption,
            seed: this.seed2query(this.params.seed),
            isVerify: this.params.isVerify,
            draw: this.draw2query(this.params.draw),
          }
        }).catch(() => {});
      }
    },
    'params.nbGrids': function() {
      if (this.grids.length < this.params.nbGrids) {
        this.processNewGrids();
      }
    },
    'params.gridType': function() {
      this.grids = [];
      this.processNewGrids();
    },
    'params.seed': function() {
      this.grids = [];
      this.processNewGrids();
    },
  }
}
</script>
