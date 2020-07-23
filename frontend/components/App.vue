<style>
body {
  margin: 0 0 25px;
  padding: 10px;
  font-family: sans-serif;
}

p {
  line-height: 150%;
}

li {
  line-height: 150%;
}
</style>

<template>
  <div id="app">
    <h1>BlueLeaks Explorer</h1>
    <ul class="sites">
      <li v-for="site in structure">{{ site.name }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      structure: null,
    };
  },
  created: function () {
    this.getStructure();
  },
  methods: {
    getStructure: function () {
      var that = this;
      fetch("/structure.json")
        .then(function (response) {
          if (response.status !== 200) {
            console.log(
              "Error fetching structure, status code: " + response.status
            );
            return;
          }
          response.json().then(function (data) {
            that.structure = data;
          });
        })
        .catch(function (err) {
          console.log("Error fetching structure", err);
        });
    },
  },
};
</script>