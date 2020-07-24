<style scoped>
.meta {
  color: #333333;
  font-style: italic;
}

ul.rows {
  list-style: none;
  padding: 0;
}

li.row {
  font-family: "Courier New", Courier, monospace;
  margin-bottom: 1em;
  padding: 1em;
  background-color: aliceblue;
}

ul.fields {
  list-style: none;
  padding: 0;
}

li.field .label {
  font-weight: bold;
}
</style>

<template>
  <div>
    <h2>
      <i class="fas fa-sitemap"></i>
      <router-link v-bind:to="linkToSite">{{ site_name }}</router-link>
    </h2>
    <h3>
      <i class="fas fa-table"></i>
      {{ table }}
    </h3>
    <div class="meta">Displaying {{ numberWithCommas(count) }} rows</div>
    <ul class="rows">
      <li v-for="row in rows" class="row">
        <ul class="fields">
          <li v-for="field in important_fields" class="field">
            <span class="label">{{ field }}:</span>
            <span
              class="value"
              v-if="field_types[field] == 'text'"
            >{{ row[headers.indexOf(field)] }}</span>
            <span class="value" v-else-if="field_types[field] == 'join'">TODO: join</span>
            <span class="value" v-else>Unimplemented field type: {{ field_types[field] }}</span>
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      site_folder: this.$route.path.split("/")[1],
      table: this.$route.path.split("/")[2],
      site_name: null,
      headers: null,
      rows: null,
      count: null,
      important_fields: null,
      hidden_fields: null,
      field_types: null,
    };
  },
  created: function () {
    this.getRows();
  },
  methods: {
    getRows: function () {
      var that = this;
      fetch("/api/" + this.site_folder + "/" + this.table + "/rows")
        .then(function (response) {
          if (response.status !== 200) {
            console.log("Error fetching rows, status code: " + response.status);
            return;
          }
          response.json().then(function (data) {
            that.site_name = data["site_name"];
            that.headers = data["headers"];
            that.rows = data["rows"];
            that.count = data["count"];
            that.important_fields = data["important_fields"];
            that.field_types = data["field_types"];

            // Fill in the hidden fields
            that.hidden_fields = [];
            for (var i in that.headers) {
              if (!that.important_fields.includes(that.headers[i])) {
                that.hidden_fields.push(that.headers[i]);
              }
            }

            // Fill in the default field types
            for (var i in that.headers) {
              if (!that.field_types[that.headers[i]]) {
                that.field_types[that.headers[i]] = "text";
              }
            }
          });
        })
        .catch(function (err) {
          console.log("Error fetching rows", err);
        });
    },
    numberWithCommas: function (x) {
      if (!x) return "...";
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },
  },
  computed: {
    linkToSite: function () {
      return "/" + this.site_folder;
    },
  },
};
</script>