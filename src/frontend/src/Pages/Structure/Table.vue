<script setup>
import { ref } from 'vue'

import Field from "./Field.vue";
import Join from "./Join.vue";
import draggable from "vuedraggable";

const props = defineProps({
  table: String,
  tableData: Object,
  structure: Object
})

const newRelationshipFromField = ref("");
const newRelationshipToTable = ref("");
const newRelationshipToField = ref("");
const showToggleCheckbox = ref(true);

function sortedFieldNames() {
  var sorted = [];
  for (var i in props.tableData["fields"]) {
    sorted.push(props.tableData["fields"][i]["name"]);
  }
  sorted.sort();
  return sorted;
}

function sortedTableNames() {
  var sorted = [];
  for (var table in props.structure["tables"]) {
    if (table != props.table) {
      sorted.push(table);
    }
  }
  sorted.sort();
  return sorted;
}

function sortedOtherFieldNames() {
  if (newRelationshipToTable.value == "") return [];
  var sorted = [];
  for (var i in props.structure["tables"][newRelationshipToTable.value][
    "fields"
  ]) {
    sorted.push(
      props.structure["tables"][newRelationshipToTable.value]["fields"][i][
      "name"
      ]
    );
  }
  sorted.sort();
  return sorted;
}

function changeDisplay() {
  var display = prompt("New display name", props.tableData["display"]);
  if (display) {
    props.tableData["display"] = display;
    makeDirty();
  }
}

function changeHidden(val) {
  props.tableData["hidden"] = val;
  this.$emit("dirty");
}

function createRelationship() {
  var name = prompt("What is the name of this relationship?");
  if (name) {
    props.structure["tables"][props.table]["joins"].push({
      name: name,
      from: props.table + "." + newRelationshipFromField.value,
      to: newRelationshipToTable.value + "." + newRelationshipToField.value,
    });
    newRelationshipFromField.value = "";
    newRelationshipToTable.value = "";
    newRelationshipToField.value = "";
    makeDirty();
  }
}

function deleteJoin(join) {
  if (confirm("Are you sure?")) {
    var index = props.tableData["joins"].indexOf(join);
    props.tableData["joins"].splice(index, 1);
    this.$emit("dirty");
  }
}

function showToggle() {
  for (var i = 0; i < props.tableData["fields"].length; i++) {
    props.tableData["fields"][i]["show"] = showToggleCheckbox;
  }
  makeDirty();
}

function makeDirty() {
  this.$emit("dirty");
}
</script>

<template>
  <div>
    <p class="table-name">
      <i class="fas fa-table"></i>
      <strong>{{ tableData['display'] }}</strong>
      <span class="meta">({{ table }})</span>
      <button v-on:click="changeDisplay()">Rename</button>
      <button v-if="tableData['hidden']" v-on:click="changeHidden(false)">Show</button>
      <button v-else v-on:click="changeHidden(true)">Hide</button>
    </p>
    <template v-if="!tableData['hidden']">
      <div class="headers">
        <span class="handle">Sort</span>
        <span class="field-name">Field Name</span>
        <span class="field-type">Type</span>
        <span class="field-show">
          Show
          <input type="checkbox" v-model="showToggleCheckbox" v-on:change="showToggle()" />
        </span>
      </div>
      <draggable class="fields" handle=".handle" v-model="tableData['fields']" @end="makeDirty">
        <div v-for="field in tableData['fields']" class="field">
          <Field v-bind:field="field" v-on:dirty="makeDirty()"></Field>
        </div>
      </draggable>

      <template v-if="tableData['joins'].length > 0">
        <div class="headers">
          <span class="handle">Sort</span>
          <span class="join-name">Name</span>
          <span class="join-relationship">Relationship</span>
          <span class="join-delete">Delete</span>
        </div>
        <draggable class="joins" handle=".handle" v-model="tableData['joins']" @end="makeDirty">
          <div v-for="join in tableData['joins']" class="join">
            <Join v-bind:join="join" v-on:dirty="makeDirty()" v-on:delete="deleteJoin(join)"></Join>
          </div>
        </draggable>
      </template>

      <div>
        <p>
          Field
          <select v-model="newRelationshipFromField">
            <option v-for="field in sortedFieldNames()">{{ field }}</option>
          </select>
          maps to table
          <select v-model="newRelationshipToTable">
            <option v-for="table in sortedTableNames()">{{ table }}</option>
          </select>
          <template v-if="newRelationshipToTable">
            field
            <select v-model="newRelationshipToField">
              <option v-for="field in sortedOtherFieldNames()">{{ field }}</option>
            </select>
            <button v-on:click="createRelationship">Create Relationship</button>
          </template>
        </p>
      </div>
    </template>
  </div>
</template>

<style scoped>
.table-name {
  font-size: 1.2em;
}

.headers {
  font-weight: bold;
  position: relative;
  display: block;
  padding: 10px 15px;
  margin-bottom: -1px;
  border: 1px solid transparent;
}

.handle {
  display: inline-block;
  width: 40px;
}

.field-name {
  display: inline-block;
  width: 450px;
}

.field-type {
  display: inline-block;
  width: 130px;
}

.field-show {
  display: inline-block;
  width: 80px;
}

.join-name {
  display: inline-block;
  width: 250px;
}

.join-relationship {
  display: inline-block;
  width: 500px;
}

.join-delete {
  display: inline-block;
  width: 80px;
}
</style>