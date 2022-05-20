<script>
export default {
  data: function () {
    return {
      loading: false,
      implementedSites: [],
      unimplementedSites: [],
    };
  },
  created: function () {
    this.getStructures();
  },
  methods: {
    getStructures: function () {
      var that = this;
      this.loading = true;
      fetch("/api/structures")
        .then(function (response) {
          if (response.status !== 200) {
            console.log(
              "Error fetching structures, status code: " + response.status
            );
            return;
          }
          response.json().then(function (data) {
            that.implementedSites = data["implemented_sites"];
            that.unimplementedSites = data["unimplemented_sites"];
            that.loading = false;
          });
        })
        .catch(function (err) {
          that.loading = false;
          console.log("Error fetching structures", err);
        });
    },
    createStructure: function (site) {
      var that = this;
      this.loading = true;
      fetch("/api/structure/create/" + site, { method: "POST" })
        .then(function (response) {
          if (response.status !== 200) {
            console.log(
              "Error creating structure, status code: " + response.status
            );
            return;
          }
          response.json().then(function (data) {
            that.loading = false;
            if (data["error"]) {
              alert(data["error_message"]);
            } else {
              that.$router.push({ path: "/structure/" + site });
            }
          });
        })
        .catch(function (err) {
          that.loading = false;
          console.log("Error creating structure", err);
        });
    },
    linkToEditSite: function (site) {
      return "/structure/" + site;
    },
  },
};
</script>

<template>
  <div>
    <template v-if="loading">
      <div class="loading">
        <img src="/static/loading.gif" alt="Loading" />
      </div>
    </template>
    <template v-else>
      <h2>Edit structures</h2>
      <ul class="implemented-sites">
        <li v-for="site in implementedSites">
          <div>
            <i class="fas fa-sitemap"></i>
            <router-link v-bind:to="linkToEditSite(site.site)">{{ site.name }}</router-link>
            ({{ site.site }})
          </div>
        </li>
      </ul>

      <h2>Define a new structure</h2>
      <ul class="unimplemented-sites">
        <li v-for="site in unimplementedSites">
          <i class="fas fa-sitemap"></i>
          <button v-on:click="createStructure(site)">Create</button>
          <span>
            structure for
            <strong>{{ site }}</strong>
          </span>
        </li>
      </ul>
    </template>
  </div>
</template>

<style scoped>
ul {
  list-style: none;
  padding: 0;
}

ul.implemented-sites a {
  font-weight: bold;
  font-size: 1.2em;
}

ul.implemented-sites li,
ul.unimplemented-sites li {
  margin-bottom: 1em;
}

ul.implemented-sites i,
ul.unimplemented-sites i {
  margin-right: 0.5em;
}
</style>