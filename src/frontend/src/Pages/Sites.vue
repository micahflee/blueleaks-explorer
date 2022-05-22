<script setup>
import { ref } from 'vue'

const loading = ref(false);
const sites = ref(null);

function linkToSite(folder) {
  return "/" + folder;
}

// Get sites
loading.value = true;
fetch("/api/sites")
  .then(function (response) {
    if (response.status !== 200) {
      console.log(
        "Error fetching sites, status code: " + response.status
      );
      return;
    }
    response.json().then(function (data) {
      sites.value = data;
      loading.value = false;
    });
  })
  .catch(function (err) {
    loading.value = false;
    console.log("Error fetching sites", err);
  });
</script>

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