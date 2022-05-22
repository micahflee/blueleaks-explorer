<script setup>
import { ref } from 'vue'
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

const showAllFields = ref(false);
const toggleHiddenFieldsButtonText = ref("Show All");
const itemId = ref(null);
if (props.row.length > 0) {
  itemId.value = props.row[0];
}

function permalink(id) {
  return "/" + props.site + "/" + props.table + "/" + id;
}

function toggleHiddenFields() {
  if (showAllFields.value) {
    showAllFields.value = false;
    toggleHiddenFieldsButtonText.value = "Show All";
  } else {
    showAllFields.value = true;
    toggleHiddenFieldsButtonText.value = "Hide";
  }
}
</script>

<template>
  <div>
    <ul class="fields">
      <li v-for="field in fields" class="field">
        <template v-if="field['show']">
          <TableCell :site="site" :table="table" :itemId="itemId" :field="field"
            :value="row[headers.indexOf(field['name'])]" :join="false" :isItem="isItem">
          </TableCell>
        </template>
      </li>
    </ul>
    <ul class="join-fields">
      <li v-for="join in joins" class="field">
        <TableCell :site="site" :table="table" :itemId="itemId" :field="false" :value="false" :join="join"
          :isItem="isItem"></TableCell>
      </li>
    </ul>
    <ul v-if="showAllFields" class="hidden-fields">
      <li v-for="field in fields" class="field">
        <template v-if="!field['show']">
          <TableCell :site="site" :table="table" :itemId="itemId" :field="field"
            :value="row[headers.indexOf(field['name'])]" :join="false" :isItem="isItem"></TableCell>
        </template>
      </li>
    </ul>
    <ul class="buttons">
      <li>
        <router-link class="button" :to="permalink(row[0])">Permalink</router-link>
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