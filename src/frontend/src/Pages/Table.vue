<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import TableRow from "./Table/TableRow.vue"
import Paging from "./Table/Paging.vue"
import SortBar from "./Table/SortBar.vue"
import SearchBar from "./Table/SearchBar.vue"
const route = useRoute()

const site = route.path.split("/")[1];
const table = route.path.split("/")[2];
const linkToSite = "/" + site;

const loading = ref(false);
const siteName = ref(null);
const tableName = ref(null);
const headers = ref(null);
const rows = ref(null);
const count = ref(null);
const fields = ref(null);
const joins = ref(null);
const sortFields = ref(null);
const offset = ref(0);
const perPageCount = ref(50);
const currentSort = ref("Chronologically##DESC");
const searchTerm = ref(null);

function buildURL() {
  if (currentSort.value) {
    const [sortCol, sortDir] = currentSort.value.split("##");

    if (searchTerm.value) {
      return `/api/${site.value}/${table.value}/search?search_term=${encodeURIComponent(searchTerm.value)}&count=${perPageCount.value}&offset=${offset.value}&sortCol=${encodeURIComponent(sortCol)}&sortDir=${sortDir}`;
    }

    return `/api/${site.value}/${table.value}?count=${perPageCount.value}&offset=${offset.value}&sortCol=${encodeURIComponent(sortCol)}&sortDir=${sortDir}`;
  }

  return searchTerm.value
    ? `/api/${site.value}/${table.value}/search?search_term=${encodeURIComponent(searchTerm.value)}&count=${perPageCount.value}&offset=${offset.value}`
    : `/api/${site.value}/${table.value}?count=${perPageCount.value}&offset=${offset.value}`;
}

async function getRows() {
  loading.value = true;
  try {
    const response = await fetch(buildURL());
    if (response.status !== 200) {
      loading.value = false;
      console.log("Error fetching rows, status code: " + response.status);
      return;
    }
    const data = await response.json();

    siteName.value = data["site_name"];
    tableName.value = data["table_name"];
    headers.value = data["headers"];
    rows.value = data["rows"];
    count.value = data["count"];
    fields.value = data["fields"];
    joins.value = data["joins"];

    // sortFields
    const badOptions = ["content"];
    sortFields.value = fields.value.filter((f) => f.show && badOptions.indexOf(f.name.toLowerCase()) === -1).map((f) => f.name);
    sortFields.value.unshift("Chronologically");

    loading.value = false;
  } catch (err) {
    loading.value = false;
    console.log("Error fetching rows", err);
  }
}

function numberWithCommas(x) {
  if (x == 0) return "0";
  if (!x) return "...";
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

async function pageNavigateHandler(page) {
  offset.value = perPageCount.value * (page - 1);
  await getRows();
}

async function sortChangeHandler(evt) {
  const sortOption = evt.target.selectedOptions[0].value;
  currentSort.value = sortOption;
  await getRows();
}

async function searchHandler(evt) {
  const fd = new FormData(evt.target);
  const term = fd.get("searchTerm");
  if (term) {
    searchTerm.value = term;
    await getRows();
  }
}

await getRows();
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