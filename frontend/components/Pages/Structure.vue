<style scoped>
ul {
  list-style: none;
  padding: 0;
}

li .site-link {
  font-weight: bold;
  font-size: 1.2em;
}

li .meta {
  color: #333333;
  font-style: italic;
}
</style>

<template>
  <div>
    <template v-if="loading">
      <div class="loading">
        <img src="/static/loading.gif" alt="Loading" />
      </div>
    </template>
    <template v-else>
      <h2>
        <i class="fas fa-tools"></i>
        Define Structure
      </h2>
    </template>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      loading: false,
      structure: null,
    };
  },
  created: function () {
    this.getStructure();
  },
  methods: {
    getStructure: function () {
      var that = this;
      this.loading = true;
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
            that.loading = false;
          });
        })
        .catch(function (err) {
          that.loading = false;
          console.log("Error fetching structure", err);
        });
    },
  },
};
</script>