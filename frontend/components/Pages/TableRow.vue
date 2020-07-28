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
      <li v-for="field in importantFields" class="field" v-bind:key="field">
        <TableCell
          v-bind:siteFolder="siteFolder"
          v-bind:table="table"
          v-bind:itemId="itemId"
          v-bind:header="field"
          v-bind:fieldType="fieldTypes[field]"
          v-bind:value="row[headers.indexOf(field)]"
        ></TableCell>
      </li>
    </ul>
    <ul v-if="showAllFields" class="hidden-fields">
      <li v-for="field in hiddenFields" class="field" v-bind:key="field">
        <TableCell
          v-bind:siteFolder="siteFolder"
          v-bind:table="table"
          v-bind:itemId="itemId"
          v-bind:header="field"
          v-bind:fieldType="fieldTypes[field]"
          v-bind:value="row[headers.indexOf(field)]"
        ></TableCell>
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

<script>
import TableCell from "./TableCell.vue";

export default {
  props: [
    "siteFolder",
    "table",
    "row",
    "importantFields",
    "hiddenFields",
    "fieldTypes",
    "headers",
  ],
  data: function () {
    return {
      showAllFields: false,
      toggleHiddenFieldsButtonText: "Show All",
    };
  },
  methods: {
    permalink: function (id) {
      return "/" + this.siteFolder + "/" + this.table + "/" + id;
    },
    toggleHiddenFields: function () {
      if (this.showAllFields) {
        this.showAllFields = false;
        this.toggleHiddenFieldsButtonText = "Show All";
      } else {
        this.showAllFields = true;
        this.toggleHiddenFieldsButtonText = "Hide";
      }
    },
  },
  computed: {
    itemId: function () {
      if (this.row.length > 0) {
        return this.row[0];
      } else {
        return null;
      }
    },
  },
  components: {
    TableCell: TableCell,
  },
};
</script>