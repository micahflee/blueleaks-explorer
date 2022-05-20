<script>
import TableCell from "./TableCell.vue";
import JoinRow from "./JoinRow.vue";

export default {
  props: ["site", "table", "row", "fields", "joins", "headers", "isItem"],
  data: function () {
    return {
      showAllFields: false,
      toggleHiddenFieldsButtonText: "Show All",
    };
  },
  methods: {
    permalink: function (id) {
      return "/" + this.site + "/" + this.table + "/" + id;
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
    JoinRow: JoinRow,
  },
};
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