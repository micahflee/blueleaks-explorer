<script setup>
import TableRow from "./Table/TableRow.vue";

const site = this.$route.path.split("/")[1];
const table = this.$route.path.split("/")[2];
const linkToSite = "/" + this.site;
const linkToTable = "/" + this.site + "/" + this.table;
let loading = false;
let siteName = null;
let tableName = null;
let headers = null;
let rows = null;
let fields = null;
let joins = null;

// Get item
loading = true;
fetch(
  "/api/" + site + "/" + table + "/" + this.$route.params.id
)
  .then(function (response) {
    loading = false;

    if (response.status !== 200) {
      console.log("Error fetching item, status code: " + response.status);
      return;
    }
    response.json().then(function (data) {
      siteName = data["site_name"];
      tableName = data["table_name"];
      headers = data["headers"];
      rows = data["rows"];
      fields = data["fields"];
      joins = data["joins"];
    });
  })
  .catch(function (err) {
    loading = false;
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