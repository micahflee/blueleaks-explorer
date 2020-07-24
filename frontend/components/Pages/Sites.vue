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
    <ul>
      <li v-for="site in sites">
        <div class="site-link">
          <i class="fas fa-sitemap"></i>
          <router-link v-bind:to="linkToSite(site.folder)">{{ site.name }}</router-link>
        </div>
        <div class="meta">BlueLeaks folder: {{ site.folder }}</div>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      sites: null,
    };
  },
  created: function () {
    this.getSites();
  },
  methods: {
    getSites: function () {
      var that = this;
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
          });
        })
        .catch(function (err) {
          console.log("Error fetching sites", err);
        });
    },
    linkToSite: function (folder) {
      return "/" + folder;
    },
  },
};
</script>