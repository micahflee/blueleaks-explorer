<script>
import Table from "./Structure/Table.vue";

export default {
  data: function () {
    return {
      loading: false,
      site: this.$route.path.split("/")[2],
      dirty: false,
      structure: null,
    };
  },
  created: function () {
    this.getStructure();
  },
  methods: {
    getStructure: function () {
      var that = this;
      this.loading = true;
      fetch("/api/structure/" + this.site)
        .then(function (response) {
          that.loading = false;

          if (response.status !== 200) {
            console.log(
              "Error fetching structure, status code: " + response.status
            );
            return;
          }
          response.json().then(function (data) {
            if (data["error"]) {
              alert(data["error_message"]);
              that.$router.push({ path: "/structure" });
            } else {
              that.structure = data["structure"];
            }
          });
        })
        .catch(function (err) {
          that.loading = false;
          console.log("Error fetching structure", err);
        });
    },
    save: function () {
      var that = this;
      this.loading = true;
      fetch("/api/structure/" + this.site, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(this.structure),
      })
        .then(function (response) {
          that.loading = false;

          if (response.status !== 200) {
            console.log(
              "Error saving structure, status code: " + response.status
            );
            return;
          }
          response.json().then(function (data) {
            if (data["error"]) {
              alert(data["error_message"]);
            } else {
              that.dirty = false;
            }
          });
        })
        .catch(function (err) {
          that.loading = false;
          console.log("Error saving structure", err);
        });
    },
    changeName: function () {
      var name = prompt(
        "What's the name of this site?",
        this.structure["name"]
      );
      if (name) {
        this.structure["name"] = name;
        this.dirty = true;
      }
    },
    makeDirty: function () {
      this.dirty = true;
    },
  },
  components: {
    Table: Table,
  },
};
</script>

<template>
  <div>
    <template v-if="loading">
      <div class="loading">
        <img src="/static/loading.gif" alt="Loading" />
      </div>
    </template>
    <template v-else>
      <template v-if="dirty">
        <p class="dirty">
          You have unsaved changed.
          <button v-on:click="save">Save</button>
        </p>
      </template>
      <template v-if="structure != null">
        <h2>
          <i class="fas fa-sitemap"></i>
          {{ structure["name"] }}
          <span class="meta">({{ site }})</span>
          <button v-on:click="changeName">Rename</button>
        </h2>

        <ul class="tables">
          <li v-for="(tableData, table) in structure['tables']" class="table">
            <Table v-bind:table="table" v-bind:tableData="tableData" v-bind:structure="structure"
              v-on:dirty="makeDirty()"></Table>
          </li>
        </ul>
      </template>
    </template>
  </div>
</template>

<style scoped>
.dirty {
  color: red;
  font-style: italic;
}

.meta {
  font-weight: 100;
  color: #666666;
}

ul {
  list-style: none;
  padding: 0;
}

ul.tables li.table {
  margin-bottom: 2em;
}
</style>