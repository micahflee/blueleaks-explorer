<style scoped>
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
        <router-link v-bind:to="linkToTable">{{ tableName }}</router-link>
      </h3>

      <ul class="rows">
        <li v-for="row in rows" class="row">
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
    </template>
  </div>
</template>

<script>
import TableRow from "./Table/TableRow.vue";

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
      fields: null,
      joins: null,
    };
  },
  created: function () {
    this.getItem();
  },
  methods: {
    getItem: function () {
      var that = this;
      this.loading = true;
      fetch(
        "/api/" + this.site + "/" + this.table + "/" + this.$route.params.id
      )
        .then(function (response) {
          that.loading = false;

          if (response.status !== 200) {
            console.log("Error fetching item, status code: " + response.status);
            return;
          }
          response.json().then(function (data) {
            that.siteName = data["site_name"];
            that.tableName = data["table_name"];
            that.headers = data["headers"];
            that.rows = data["rows"];
            that.fields = data["fields"];
            that.joins = data["joins"];
          });
        })
        .catch(function (err) {
          that.loading = false;
          console.log("Error fetching item", err);
        });
    },
  },
  computed: {
    linkToSite: function () {
      return "/" + this.site;
    },
    linkToTable: function () {
      return "/" + this.site + "/" + this.table;
    },
  },
  components: {
    TableRow: TableRow,
  },
};
</script>