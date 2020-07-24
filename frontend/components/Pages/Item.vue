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
            v-bind:row="row"
            v-bind:importantFields="importantFields"
            v-bind:hiddenFields="hiddenFields"
            v-bind:fieldTypes="fieldTypes"
            v-bind:headers="headers"
            v-bind:siteFolder="siteFolder"
            v-bind:table="table"
          ></TableRow>
        </li>
      </ul>
    </template>
  </div>
</template>

<script>
import TableRow from "./TableRow.vue";

export default {
  data: function () {
    return {
      loading: false,
      siteFolder: this.$route.path.split("/")[1],
      table: this.$route.path.split("/")[2],
      siteName: null,
      tableName: null,
      headers: null,
      rows: null,
      importantFields: null,
      hiddenFields: null,
      fieldTypes: null,
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
        "/api/" +
          this.siteFolder +
          "/" +
          this.table +
          "/" +
          this.$route.params.id
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
            that.importantFields = data["important_fields"];
            that.fieldTypes = data["field_types"];

            // Fill in the hidden fields
            that.hiddenFields = [];
            for (var i in that.headers) {
              if (!that.importantFields.includes(that.headers[i])) {
                that.hiddenFields.push(that.headers[i]);
              }
            }

            // Fill in the default field types
            for (var i in that.headers) {
              if (!that.fieldTypes[that.headers[i]]) {
                that.fieldTypes[that.headers[i]] = "text";
              }
            }
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
      return "/" + this.siteFolder;
    },
    linkToTable: function () {
      return "/" + this.siteFolder + "/" + this.table;
    },
  },
  components: {
    TableRow: TableRow,
  },
};
</script>