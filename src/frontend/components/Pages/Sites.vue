<style scoped>
ul {
  list-style: none;
  padding: 0;
}

li {
  margin-bottom: 1em;
}

li .site-link {
  font-weight: bold;
  font-size: 1.2em;
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
      <h2>Choose a site to explore</h2>
      <ul>
        <li v-for="site in sites">
          <i class="fas fa-sitemap"></i>
          <router-link class="site-link" v-bind:to="linkToSite(site.site)">{{ site.name }}</router-link>
          <span class="meta">({{ site.site }})</span>
        </li>
      </ul>
    </template>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      loading: false,
      sites: null,
    };
  },
  created: function () {
    this.getSites();
  },
  methods: {
    getSites: function () {
      var that = this;
      this.loading = true;
      fetch("/api/sites")
        .then(function (response) {
          if (response.status !== 200) {
            console.log(
              "Error fetching sites, status code: " + response.status
            );
            return;
          }
          response.json().then(function (data) {
            that.sites = data;
            that.loading = false;
          });
        })
        .catch(function (err) {
          that.loading = false;
          console.log("Error fetching sites", err);
        });
    },
    linkToSite: function (folder) {
      return "/" + folder;
    },
  },
};
</script>