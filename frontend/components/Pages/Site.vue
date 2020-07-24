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

<template>
  <div>
    <h2>
      <i class="fas fa-sitemap"></i>
      {{ site_name }}
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
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      site_folder: this.$route.path.substring(1),
      site_name: null,
      tables: null,
    };
  },
  created: function () {
    this.getTables();
  },
  methods: {
    getTables: function () {
      var that = this;
      fetch("/api/" + this.site_folder + "/tables")
        .then(function (response) {
          if (response.status !== 200) {
            console.log(
              "Error fetching tables, status code: " + response.status
            );
            return;
          }
          response.json().then(function (data) {
            that.site_name = data["site_name"];
            that.tables = data["tables"];
          });
        })
        .catch(function (err) {
          console.log("Error tables sites", err);
        });
    },
    linkToTable: function (table) {
      return "/" + this.site_folder + "/" + table;
    },
    numberWithCommas: function (x) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },
  },
};
</script>