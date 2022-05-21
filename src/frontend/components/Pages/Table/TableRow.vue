<script setup>
import TableCell from "./TableCell.vue";

const props = defineProps({
  site: String,
  table: String,
  row: Object,
  fields: Array,
  joins: Array,
  headers: Array,
  isItem: Boolean
})

let showAllFields = false;
let toggleHiddenFieldsButtonText = "Show All";

if (row.length > 0) {
  const itemId = row[0];
} else {
  const itemId = null;
}

function permalink: function (id) {
  return "/" + site + "/" + table + "/" + id;
}

function toggleHiddenFields() {
  if (showAllFields) {
    showAllFields = false;
    toggleHiddenFieldsButtonText = "Show All";
  } else {
    showAllFields = true;
    toggleHiddenFieldsButtonText = "Hide";
  }
}
</script>

<template>
  <div>
    <ul class="fields">
      <li v-for="field in fields" class="field">
        <template v-if="field['show']">
          <TableCell v-bind:site="site" v-bind:table="table" v-bind:itemId="itemId" v-bind:field="field"
            v-bind:value="row[headers.indexOf(field['name'])]" v-bind:isItem="isItem"></TableCell>
        </template>
      </li>
    </ul>
    <ul class="join-fields">
      <li v-for="join in joins" class="field">
        <TableCell v-bind:site="site" v-bind:table="table" v-bind:itemId="itemId" v-bind:join="join"
          v-bind:isItem="isItem"></TableCell>
      </li>
    </ul>
    <ul v-if="showAllFields" class="hidden-fields">
      <li v-for="field in fields" class="field">
        <template v-if="!field['show']">
          <TableCell v-bind:site="site" v-bind:table="table" v-bind:itemId="itemId" v-bind:field="field"
            v-bind:value="row[headers.indexOf(field['name'])]" v-bind:isItem="isItem"></TableCell>
        </template>
      </li>
    </ul>
    <ul class="buttons">
      <li>
        <router-link class="button" v-bind:to="permalink(row[0])">Permalink</router-link>
      </li>
      <li>
        <button v-on:click="toggleHiddenFields">{{ toggleHiddenFieldsButtonText }}</button>
      </li>
    </ul>
  </div>
</template>

<style scoped>
ul {
  list-style: none;
  padding: 0;
}

ul.buttons {
  list-style: none;
  padding: 0;
  margin-top: 1em;
}

ul.buttons li {
  display: inline-block;
  margin: 0 10px 0 0;
}
</style>