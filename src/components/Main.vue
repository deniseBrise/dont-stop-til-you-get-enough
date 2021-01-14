<template>
  <div>

    <section class="hero">
      <div class="hero-body box">
        <div class="container columns">

          <div class="column">
            <h1 class="title">
              Total: {{ totalPrice }} €
            </h1>
          </div>

          <div class="column">
            <b-field label="Nombre de grilles">
              <b-numberinput v-model="nbGrids" min="0" max="10000" step="1" :exponential=".5" :editable="false" controls-position="compact" controls-rounded></b-numberinput>
            </b-field>
          </div>

          <div class="column">
            <b-field grouped label="Jeu et Options">
              <b-switch v-model="gridType" passive-type='is-primary'>{{ gridType ? 'Loto' : 'Euro' }}</b-switch>
              <b-checkbox v-model="isOption">{{ gridType ? '2nd tirage' : 'Etoile+' }}</b-checkbox>
            </b-field>
          </div>

        </div>
      </div>
    </section>

  </div>
</template>

<script>
export default {
  data() {
    return {
      nbGrids: 0,
      gridType: false,
      isOption: false,
    }
  },
  computed: {
    gridPrice: function() {
      return this.gridType ? 2.20 : 2.50;
    },
    optionPrice: function() {
      return this.gridType ? 0.80 : 1.00;
    },
    totalPrice: function() {
      return this.nbGrids * (this.gridPrice + (this.isOption ? this.optionPrice : 0));
    },
  },
}
</script>
