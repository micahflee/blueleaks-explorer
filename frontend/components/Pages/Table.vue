<style scoped>
.meta {
  color: #333333;
  font-style: italic;
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
      <h2>
        <i class="fas fa-sitemap"></i>
        <router-link v-bind:to="linkToSite">{{ siteName }}</router-link>
      </h2>
      <h3>
        <i class="fas fa-table"></i>
        {{ tableName }}
      </h3>
      <div class="meta">Displaying {{ numberWithCommas(count) }} rows</div>
      <ul class="rows">
        <li v-for="row in rows" class="row" v-bind:key="row[0]">
          <TableRow
            v-bind:site="site"
            v-bind:table="table"
            v-bind:row="row"
            v-bind:fields="fields"
            v-bind:joins="joins"
            v-bind:headers="headers"
          ></TableRow>
        </li>
      </ul>
      <template v-if="count">
        <Paging
          v-bind:totalItems="count"
          v-bind:perPageCount="perPageCount"
          v-bind:offset="offset"
          v-bind:pageNavigateHandler="pageNavigateHandler"
        ></Paging>
      </template>
    </template>
  </div>
</template>

<script>
import TableRow from "./Table/TableRow.vue";
import Paging from "./Table/Paging.vue";

export default {
  data: function () {
    return {
      loading: false,
      site: this.$route.path.split("/")[1],
      table: this.$route.path.split("/")[2],
      siteName: null,
      tableName: null,
      headers: null,
      rows: null,
      count: null,
      fields: null,
      joins: null,
      offset: 0,
      perPageCount: 50,
    };
  },
  created: function () {
    this.getRows();
  },
  methods: {
    getRows: async function () {
      this.loading = true;
      // console.log(`count: ${this.perPageCount} offset: ${this.offset}`);
      try {
        const response = await fetch(
          `/api/${this.site}/${this.table}?count=${this.perPageCount}&offset=${this.offset}`
        );
        if (response.status !== 200) {
          this.loading = false;
          console.log("Error fetching rows, status code: " + response.status);
          return;
        }
        const data = await response.json();

        this.siteName = data["site_name"];
        this.tableName = data["table_name"];
        this.headers = data["headers"];
        this.rows = data["rows"];
        this.count = data["count"];
        this.fields = data["fields"];
        this.joins = data["joins"];

        this.loading = false;
      } catch (err) {
        this.loading = false;
        console.log("Error fetching rows", err);
      }
    },
    numberWithCommas: function (x) {
      if (!x) return "...";
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },
    pageNavigateHandler: function (page) {
      this.offset = this.perPageCount * (page - 1);
      this.getRows();
    },
  },
  computed: {
    linkToSite: function () {
      return "/" + this.site;
    },
  },
  components: {
    TableRow,
    Paging,
  },
};
</script>
