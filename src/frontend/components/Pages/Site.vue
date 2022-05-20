<script setup>
let loading = false;
let site = this.$route.path.split("/")[1];
let siteName = null;
let tables = null;

function linkToTable(table) {
  return "/" + this.site + "/" + table;
}

function numberWithCommas(x) {
  if (x == 0) return "0";
  if (!x) return "...";
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Get tables
var that = this;
loading = true;
fetch("/api/" + site + "/tables")
  .then(function (response) {
    that.loading = false;

    if (response.status !== 200) {
      console.log(
        "Error fetching tables, status code: " + response.status
      );
      return;
    }
    response.json().then(function (data) {
      that.siteName = data["site_name"];
      that.tables = data["tables"];
    });
  })
  .catch(function (err) {
    that.loading = false;
    console.log("Error fetching tables", err);
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
        {{ siteName }}
      </h2>
      <ul>
        <li v-for="table in tables">
          <div class="table-link">
            <i class="fas fa-table"></i>
            <router-link v-bind:to="linkToTable(table.name)">{{ table.display_name }}</router-link>
          </div>
          <div class="meta">{{ numberWithCommas(table.count) }} rows</div>
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
  display: inline-block;
  padding: 0 20px 20px 0;
  width: 400px;
}

li .table-link {
  font-weight: bold;
}

li .meta {
  color: #333333;
  font-style: italic;
}
</style>