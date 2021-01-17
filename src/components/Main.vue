<template>
  <div>

    <nav class="hero">
      <div class="hero-body box">
        <div class="container columns">

          <div class="column">
            <b-field label="Total">
              <h1 class="title">
                {{ totalPrice | currency }}
              </h1>
            </b-field>
          </div>

          <div class="column">
            <b-field label="Nombre de grilles">
              <b-numberinput v-model="params.nbGrids" min="0" max="10000" step="1" :exponential=".5" :editable="false" controls-position="compact" controls-rounded></b-numberinput>
            </b-field>
          </div>

          <div class="column">
            <b-field grouped label="Jeu et Options">
              <b-switch v-model="params.gridType" passive-type='is-primary'>{{ params.gridType ? 'Loto' : 'Euro' }}</b-switch>
              <b-checkbox v-model="params.isOption">{{ params.gridType ? '2nd tirage' : 'Etoile+' }}</b-checkbox>
            </b-field>
          </div>

        </div>
      </div>
    </nav>

    <section class="section">
      <div class="columns is-multiline is-mobile">
        <div class="column is-narrow" v-for="i in params.nbGrids" :key="i">
          <mba-grid :gridNumber="i" :nbSquares="squareMaxValue" :nbStars="starMaxValue" :squareList="[1, 2, 3, 4]" :starList="[1, 2]"></mba-grid>
        </div>
      </div>
    </section>

  </div>
</template>

<script>
import MbaGrid from '@/components/Grid.vue'

const currencyFormatter = new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' });

export default {
  created: function() {
    const queryNbGrids = (this.$route.query.nbGrids||0);
    const querySeed = this.query2seed(this.$route.query.seed);
    this.params.nbGrids = (parseInt(queryNbGrids, 10)||0);
    this.params.gridType = (this.$route.query.gridType||false);
    this.params.isOption = (this.$route.query.isOption||false);
    this.params.seed = (querySeed||this.seedGenerator());
  },
  components: {
    MbaGrid,
  },
  data() {
    return {
      params: {
        nbGrids: 0,
        gridType: false,
        isOption: false,
        seed: [],
      },
    }
  },
  computed: {
    seedMaxValue: function() {
      return 50;
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
    seedGenerator: function() {
      var a = Array.from({length: this.seedMaxValue}, (_, i) => i + 1);
      for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
      }
      return a;
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
        this.$router.push({
          query: { 
            nbGrids: this.params.nbGrids,
            gridType: this.params.gridType,
            isOption: this.params.isOption,
            seed: this.seed2query(this.params.seed),
          }
        }).catch(() => {});
      }
    }
  }
}
</script>
