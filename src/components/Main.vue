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
          <b-field label="Seed">
            <b-button type="is-primary" @click="newSeed">Suffle</b-button>
          </b-field>
        </b-navbar-item>

        <b-navbar-item class="mx-6">
          <b-field grouped label="Jeu et Options">
            <b-switch v-model="params.gridType" passive-type='is-primary'>{{ params.gridType ? 'Loto' : 'Euro' }}</b-switch>
            <b-checkbox v-model="params.isOption">{{ params.gridType ? '2nd tirage' : 'Etoile+' }}</b-checkbox>
          </b-field>
        </b-navbar-item>

      </template>
    </b-navbar>

    <section class="section">
      <div class="columns is-multiline is-mobile">
        <div class="column is-narrow" v-for="i in params.nbGrids" :key="i">
          <mba-grid :gridNumber="i" :grid="grids[i-1]||{}" :nbSquares="squareMaxValue" :nbStars="starMaxValue"></mba-grid>
        </div>
      </div>
    </section>

  </div>
</template>

<script>
import MbaGrid from '@/components/Grid.vue'
import {Mutex} from 'async-mutex';

const processingMutex = new Mutex();
const currencyFormatter = new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' });

export default {
  created: function() {
    const querySeed = this.query2seed(this.$route.query.seed);
    const queryNbGrids = (this.$route.query.nbGrids||0);
    this.params.nbGrids = (parseInt(queryNbGrids, 10)||0);
    this.params.gridType = (this.$route.query.gridType||false);
    this.params.isOption = (this.$route.query.isOption||false);
    this.params.seed = (querySeed||this.shuffleSeed());
  },
  components: {
    MbaGrid,
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
      index: {
        square: 0,
        star: 0,
        squareCommon: 0,
        starCommon: 0,
        squareLoop: 0,
        starLoop: 0,
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
      this.index = 0;
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
    isValidNextValue(previousDraws, currentDraw, nextValue, startFrom, commonMax) {
      if (currentDraw.includes(nextValue)) {
        return false;
      }
      let array = currentDraw.slice(0);
      array.push(nextValue);
      for (const i in this.grids) {
        if (i >= startFrom 
          && this.hasCommonNumber(previousDraws[i], array) > commonMax) {
          return false;
        }
      }
      return true;
    },
    hasCommonNumber(array1, array2) {
      let commonNumber = 0;
      for (const value of array1) {
        if (array2.includes(value)) {
          commonNumber++;
        }
      }
      return commonNumber;
    },
    async processNewGrids() {
      await processingMutex.runExclusive(
        async () => {
          while (this.grids.length < this.params.nbGrids) {
            let grid = await this.nextGrid();
            this.grids.push(grid);
          }
        }
      );
    },
    async nextGrid() {
      let squares = [];
      let stars = [];

      while (stars.length < this.starMaxNumber) {
        // save initial index
        let initIndex = this.index.star;
        // loop until pushing a value to array
        while (initIndex > -42) {
          // increment start index
          this.index.star = (this.index.star + 1) % this.starMaxValue;
          // get seed value at index
          let nextValue = this.starSeed[this.index.star];
          // test if this value is acceptable considering existing grids
          if (this.isValidNextValue(this.starDraws, stars, nextValue, this.index.starLoop, this.index.starCommon)) {
            stars.push(nextValue);
            break;
          }
          // after a full loop over seeds without success...
          if (initIndex == this.index.star) {
            // ...increment the number of possible common numbers
            this.index.starCommon = (this.index.starCommon + 1) % this.starMaxNumber;
            // if common number was reset
            if (this.index.starCommon == 0) {
              // set new offset to start index
              this.index.starLoop = this.grids.length;
            }
            console.log('COMMON', this.index.starCommon, 'FROM', this.index.starLoop, 'AT', this.grids.length)
          }
        }
      }

      return {
        squares,
        stars,
      };
    },
    // async sleep(ms) {
    //   return new Promise(resolve => setTimeout(resolve, ms));
    // },
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

        // calc more grids if needed)
        this.processNewGrids();
      }
    }
  }
}
</script>
