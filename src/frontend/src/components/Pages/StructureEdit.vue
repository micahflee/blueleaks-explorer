<script setup>
import Table from "./Structure/Table.vue";

let loading = false;
let site = this.$route.path.split("/")[2];
let dirty = false;
let structure = null;

function save() {
  loading = true;
  fetch("/api/structure/" + site, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(structure),
  })
    .then(function (response) {
      loading = false;

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
          dirty = false;
        }
      });
    })
    .catch(function (err) {
      loading = false;
      console.log("Error saving structure", err);
    });
}

function changeName() {
  var name = prompt(
    "What's the name of this site?",
    structure["name"]
  );
  if (name) {
    structure["name"] = name;
    dirty = true;
  }
}

function makeDirty() {
  dirty = true;
}

// Get structure
loading = true;
fetch("/api/structure/" + site)
  .then(function (response) {
    loading = false;

    if (response.status !== 200) {
      console.log(
        "Error fetching structure, status code: " + response.status
      );
      return;
    }
    response.json().then(function (data) {
      if (data["error"]) {
        alert(data["error_message"]);
        this.$router.push({ path: "/structure" });
      } else {
        structure = data["structure"];
      }
    });
  })
  .catch(function (err) {
    loading = false;
    console.log("Error fetching structure", err);
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