<script setup>
import { ref } from 'vue'
import draggable from 'vuedraggable'

import Field from "./Field.vue"
import Join from "./Join.vue"

const props = defineProps({
  table: String,
  tableData: Object,
  structure: Object
})
const emit = defineEmits(["dirty"])

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
  emit("dirty");
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
    emit("dirty");
  }
}

function showToggle() {
  for (var i = 0; i < props.tableData["fields"].length; i++) {
    props.tableData["fields"][i]["show"] = showToggleCheckbox.value;
  }
  makeDirty();
}

function makeDirty() {
  emit("dirty");
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
      <draggable v-model="tableData['fields']" @end="makeDirty" item-key="name">
        <template #item="{ element }">
          <div class="field">
            <Field v-bind:field="element" v-on:dirty="makeDirty()"></Field>
          </div>
        </template>
      </draggable>

      <template v-if="tableData['joins'].length > 0">
        <div class="headers">
          <span class="handle">Sort</span>
          <span class="join-name">Name</span>
          <span class="join-relationship">Relationship</span>
          <span class="join-delete">Delete</span>
        </div>
        <draggable v-model="tableData['joins']" @end="makeDirty">
          <template #item="{ element }">
            <div class="join">
              <Join v-bind:join="element" v-on:dirty="makeDirty()" v-on:delete="deleteJoin(element)"></Join>
            </div>
          </template>
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