<template>
  <div>

    <section class="hero">
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
    </section>

  </div>
</template>

<script>
const currencyFormatter = new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' });

export default {
  created: function() {
    const nbGridsStr = (this.$route.query.nbGrids||0);
    this.params.nbGrids = (parseInt(nbGridsStr, 10)||0);
    this.params.gridType = (this.$route.query.gridType||false);
    this.params.isOption = (this.$route.query.isOption||false);
  },
  data() {
    return {
      params: {
        nbGrids: 0,
        gridType: false,
        isOption: false,
      },
    }
  },
  computed: {
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
          }
        }).catch(() => {});
      }
    }
  }
}
</script>
