<template>
  <div id="app">
      <navbar />
      <b-card class="body">
          <router-view/>
      </b-card>
  </div>
</template>

<script>

import navbar from './components/NavBar.vue'

export default {
  name: 'app',
  components: {
      navbar,
  }
}

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  background: url('./assets/oriental-tiles.png');
  color: #2c3e50;
  min-height: 100vh;
}

#app .body {
    margin: 1vh auto 0 auto;
    width: 1024px;
}



</style>
