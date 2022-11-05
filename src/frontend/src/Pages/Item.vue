<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import TableRow from "./Table/TableRow.vue";
const route = useRoute()

const site = route.path.split("/")[1];
const table = route.path.split("/")[2];
const linkToSite = "/" + site;
const linkToTable = "/" + site + "/" + table;

const loading = ref(false);
const siteName = ref(null);
const tableName = ref(null);
const headers = ref(null);
const rows = ref(null);
const fields = ref(null);
const joins = ref(null);

// Get item
loading.value = true;
fetch(`/api/${site}/${table}/${route.params.id}`)
  .then(function (response) {
    loading.value = false;

    if (response.status !== 200) {
      console.log("Error fetching item, status code: " + response.status);
      return;
    }
    response.json().then(function (data) {
      siteName.value = data["site_name"];
      tableName.value = data["table_name"];
      headers.value = data["headers"];
      rows.value = data["rows"];
      fields.value = data["fields"];
      joins.value = data["joins"];
    });
  })
  .catch(function (err) {
    loading.value = false;
    console.log("Error fetching item", err);
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
      <h2>
        <i class="fas fa-sitemap"></i>
        <router-link v-bind:to="linkToSite">{{ siteName }}</router-link>
      </h2>
      <h3>
        <i class="fas fa-table"></i>
        <router-link v-bind:to="linkToTable">{{ tableName }}</router-link>
      </h3>

      <ul class="rows">
        <li v-for="row in rows" class="row">
          <TableRow v-bind:site="site" v-bind:table="table" v-bind:row="row" v-bind:fields="fields" v-bind:joins="joins"
            v-bind:headers="headers" v-bind:isItem="true"></TableRow>
        </li>
      </ul>
    </template>
  </div>
</template>

<style scoped>

</style>