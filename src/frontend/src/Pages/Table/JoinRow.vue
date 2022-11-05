<script setup>
import JoinCell from "./JoinCell.vue";

const props = defineProps({
  site: String,
  table: String,
  row: Array,
  fields: Array,
  headers: Array
})
</script>

<template>
  <div>
    <ul class="fields">
      <li v-for="field in fields" class="field">
        <JoinCell v-bind:site="site" v-bind:table="table" v-bind:field="field"
          v-bind:value="row[headers.indexOf(field['name'])]"></JoinCell>
      </li>
    </ul>
    <ul class="buttons">
      <li>
        <router-link class="button secondary" v-bind:to="`/${site}/${table}/${row[0]}`">Permalink</router-link>
      </li>
    </ul>
  </div>
</template>

<style scoped>
ul.fields,
ul.hidden-fields {
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