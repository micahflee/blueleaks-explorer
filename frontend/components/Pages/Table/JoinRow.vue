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

<template>
  <div>
    <ul class="fields">
      <li v-for="field in importantFields" class="field">
        <JoinCell
          v-bind:siteFolder="siteFolder"
          v-bind:table="table"
          v-bind:header="field"
          v-bind:fieldType="fieldTypes[field]"
          v-bind:value="row[headers.indexOf(field)]"
        ></JoinCell>
      </li>
    </ul>
    <ul class="buttons">
      <li>
        <router-link class="button" v-bind:to="permalink(row[0])">Permalink</router-link>
      </li>
    </ul>
  </div>
</template>

<script>
import JoinCell from "./JoinCell.vue";

export default {
  props: [
    "siteFolder",
    "table",
    "row",
    "importantFields",
    "fieldTypes",
    "headers",
  ],
  methods: {
    permalink: function (id) {
      return "/" + this.siteFolder + "/" + this.table + "/" + id;
    },
  },
  components: {
    JoinCell: JoinCell,
  },
};
</script>