<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()

const loading = ref(false);
const implementedSites = ref([]);
const unimplementedSites = ref([]);

function createStructure(site) {
  loading.value = true;
  fetch("/api/structure/create/" + site, { method: "POST" })
    .then(function (response) {
      if (response.status !== 200) {
        console.log(
          "Error creating structure, status code: " + response.status
        );
        return;
      }
      response.json().then(function (data) {
        loading.value = false;
        if (data["error"]) {
          alert(data["error_message"]);
        } else {
          router.push({ path: "/structure/" + site });
        }
      });
    })
    .catch(function (err) {
      loading.value = false;
      console.log("Error creating structure", err);
    });
}

function linkToEditSite(site) {
  return "/structure/" + site;
}

// Get structures
loading.value = true;
fetch("/api/structures")
  .then(function (response) {
    if (response.status !== 200) {
      console.log(
        "Error fetching structures, status code: " + response.status
      );
      return;
    }
    response.json().then(function (data) {
      implementedSites.value = data["implemented_sites"];
      unimplementedSites.value = data["unimplemented_sites"];
      loading.value = false;
    });
  })
  .catch(function (err) {
    loading.value = false;
    console.log("Error fetching structures", err);
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