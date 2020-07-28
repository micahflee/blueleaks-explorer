<style scoped>
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
        <i class="fas fa-sitemap"></i>
        {{ structure["name"] }}
      </h2>
    </template>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      loading: false,
      site: this.$route.path.split("/")[2],
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
      fetch("/api/structure/" + this.site)
        .then(function (response) {
          that.loading = false;

          if (response.status !== 200) {
            console.log(
              "Error fetching structure, status code: " + response.status
            );
            return;
          }
          response.json().then(function (data) {
            if (data["error"]) {
              alert(data["error_message"]);
              that.$router.push({ path: "/structure" });
            } else {
              that.structure = data["structure"];
            }
          });
        })
        .catch(function (err) {
          that.loading = false;
          console.log("Error fetching structure", err);
        });
    },
    linkToTable: function (table) {
      return "/" + this.siteFolder + "/" + table;
    },
    numberWithCommas: function (x) {
      if (!x) return "...";
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },
  },
};
</script>