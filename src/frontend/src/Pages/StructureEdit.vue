<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Table from "./Structure/Table.vue"
const router = useRouter()
const route = useRoute()

const site = route.path.split("/")[2];

const loading = ref(false);
const dirty = ref(false);
const structure = ref(null);

function save() {
  loading.value = true;
  fetch("/api/structure/" + site, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(structure.value),
  })
    .then(function (response) {
      loading.value = false;

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
          dirty.value = false;
        }
      });
    })
    .catch(function (err) {
      loading.value = false;
      console.log("Error saving structure", err);
    });
}

function changeName() {
  var name = prompt(
    "What's the name of this site?",
    structure.value["name"]
  );
  if (name) {
    structure.value["name"] = name;
    dirty.value = true;
  }
}

function makeDirty() {
  dirty.value = true;
}

// Get structure
loading.value = true;
fetch("/api/structure/" + site)
  .then(function (response) {
    loading.value = false;

    if (response.status !== 200) {
      console.log(
        "Error fetching structure, status code: " + response.status
      );
      return;
    }
    response.json().then(function (data) {
      if (data["error"]) {
        alert(data["error_message"]);
        router.push({ path: "/structure" });
      } else {
        structure.value = data["structure"];
      }
    });
  })
  .catch(function (err) {
    loading.value = false;
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
      <template v-if="structure != null">
        <h2>
          <i class="fas fa-sitemap"></i>
          {{ structure["name"] }}
          <span class="meta">({{ site }})</span>
          <button v-on:click="changeName">Rename</button>
        </h2>

        <ul class="tables">
          <li v-for="(tableData, table) in structure['tables']" class="table">
            <Table :table="table" :tableData="tableData" :structure="structure" v-on:dirty="makeDirty()"></Table>
          </li>
        </ul>
      </template>

      <template v-if="dirty">
        <p id="dirty">
          You have unsaved changed.
          <button v-on:click="save">Save</button>
        </p>
      </template>
    </template>
  </div>
</template>

<style scoped>
h2 i {
  margin-right: 0.5em;
}

.table-name i {
  margin-right: 0.5em;
}

#dirty {
  color: red;
  font-style: italic;
  position: fixed;
  bottom: 0;
  right: 0;
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