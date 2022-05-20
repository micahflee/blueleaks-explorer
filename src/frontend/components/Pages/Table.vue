<script setup>
import TableRow from "./Table/TableRow.vue";
import Paging from "./Table/Paging.vue";
import SortBar from "./Table/SortBar.vue";
import SearchBar from "./Table/SearchBar.vue";

const site = this.$route.path.split("/")[1];
const table = this.$route.path.split("/")[2];
const linkToSite = "/" + site;

let loading = false;
let siteName = null;
let tableName = null;
let headers = null;
let rows = null;
let count = null;
let fields = null;
let joins = null;
let sortFields = null;
let offset = 0;
let perPageCount = 50;
let currentSort = "Chronologically##DESC";
let searchTerm = null;

function getRows() {
  loading = true;
  // console.log(`current sort: ${this.currentSort}`);
  // console.log(`count: ${this.perPageCount} offset: ${this.offset}`);
  try {
    const response = await fetch(this.buildURL());
    if (response.status !== 200) {
      loading = false;
      console.log("Error fetching rows, status code: " + response.status);
      return;
    }
    const data = await response.json();

    siteName = data["site_name"];
    tableName = data["table_name"];
    headers = data["headers"];
    rows = data["rows"];
    count = data["count"];
    fields = data["fields"];
    joins = data["joins"];

    // sortFields
    const badOptions = ["content"];
    sortFields = fields.filter((f) => f.show && badOptions.indexOf(f.name.toLowerCase()) === -1).map((f) => f.name);
    sortFields.unshift("Chronologically");

    loading = false;
  } catch (err) {
    loading = false;
    console.log("Error fetching rows", err);
  }
}

function buildURL() {
  if (this.currentSort) {
    const [sortCol, sortDir] = this.currentSort.split("##");

    if (this.searchTerm) {
      return `/api/${this.site}/${this.table
        }/search?search_term=${encodeURIComponent(this.searchTerm)}&count=${this.perPageCount
        }&offset=${this.offset}&sortCol=${encodeURIComponent(
          sortCol
        )}&sortDir=${sortDir}`;
    }

    return `/api/${this.site}/${this.table}?count=${this.perPageCount
      }&offset=${this.offset}&sortCol=${encodeURIComponent(
        sortCol
      )}&sortDir=${sortDir}`;
  }

  return this.searchTerm
    ? `/api/${this.site}/${this.table
    }/search?search_term=${encodeURIComponent(this.searchTerm)}&count=${this.perPageCount
    }&offset=${this.offset}`
    : `/api/${this.site}/${this.table}?count=${this.perPageCount}&offset=${this.offset}`;
}

function numberWithCommas(x) {
  if (x == 0) return "0";
  if (!x) return "...";
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function pageNavigateHandler(page) {
  offset = perPageCount * (page - 1);
  getRows();
}

function sortChangeHandler(evt) {
  const sortOption = evt.target.selectedOptions[0].value;
  currentSort = sortOption;
  getRows();
}

function searchHandler(evt) {
  const fd = new FormData(evt.target);
  const term = fd.get("searchTerm");
  if (term) {
    searchTerm = term;
    getRows();
  }
}
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
        {{ tableName }}
      </h3>
      <div class="meta">Displaying {{ numberWithCommas(count) }} rows</div>
      <SortBar v-bind:headers="sortFields" v-bind:currentSort="currentSort"
        v-bind:sortChangeHandler="sortChangeHandler"></SortBar>
      <SearchBar v-bind:searchTerm="searchTerm" v-bind:handleSearchSubmit="searchHandler"></SearchBar>
      <ul class="rows">
        <li v-for="row in rows" class="row" v-bind:key="row[0]">
          <TableRow v-bind:site="site" v-bind:table="table" v-bind:row="row" v-bind:fields="fields" v-bind:joins="joins"
            v-bind:headers="headers" v-bind:isItem="false"></TableRow>
        </li>
      </ul>
      <template v-if="count">
        <Paging v-bind:totalItems="count" v-bind:perPageCount="perPageCount" v-bind:offset="offset"
          v-bind:pageNavigateHandler="pageNavigateHandler"></Paging>
      </template>
    </template>
  </div>
</template>

<style scoped>
.meta {
  color: #333333;
  font-style: italic;
}
</style>