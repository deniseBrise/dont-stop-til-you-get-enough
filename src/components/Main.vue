<template>
  <div>

    <!-- Hidden navbar to fix dinamic offset -->
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

        <b-navbar-item class="mx-6">
          <b-field label="Total">
            <p class="title">{{ totalPrice | currency }}</p>
          </b-field>
        </b-navbar-item>

        <b-navbar-item class="mx-3">
          <b-field label="Nombre de grilles">
            <b-numberinput v-model="params.nbGrids" min="0" max="10000" step="1" :exponential=".5" :editable="false" controls-position="compact" controls-rounded></b-numberinput>
          </b-field>
        </b-navbar-item>

        <b-navbar-item class="mx-3">
          <b-field grouped label="Jeu et Options">
            <b-switch v-model="params.gridType" passive-type='is-primary'>{{ params.gridType ? 'Loto' : 'Euro' }}</b-switch>
            <b-checkbox v-model="params.isOption">{{ params.gridType ? '2nd tirage' : 'Etoile+' }}</b-checkbox>
          </b-field>
        </b-navbar-item>

        <b-navbar-item class="mx-2">
          <b-field label="Actions">
            <b-button @click="newSeed">Suffle</b-button>
          </b-field>
        </b-navbar-item>

      </template>
    </b-navbar>

    <mba-grids :grids="grids" :nbGrids="params.nbGrids" :nbSquares="squareMaxValue" :nbStars="starMaxValue"></mba-grids>

  </div>
</template>

<script>
import MbaGrids from '@/components/Grids.vue'
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
  },
  components: {
    MbaGrids,
  },
  data() {
    return {
      grids: [],
      params: {
        nbGrids: 0,
        gridType: false,
        isOption: false,
        seed: [],
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
    gridPrice: function() {
      return this.params.gridType ? 2.20 : 2.50;
    },
    optionPrice: function() {
      return this.params.gridType ? 0.80 : 1.00;
    },
    totalPrice: function() {
      return this.params.nbGrids * (this.gridPrice + (this.params.isOption ? this.optionPrice : 0));
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
    filterSeed: function(max) {
      return this.params.seed.filter(function (value) {
        return value <= max;
      });
    },
    getCommonNumber(array1, array2) {
      let commonNumber = 0;
      for (const value of array1) {
        if (array2.includes(value)) {
          commonNumber++;
        }
      }
      return commonNumber;
    },
    isValidNextValue(previousDraws, currentDraw, nextValue, startFrom, commonMax) {
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
