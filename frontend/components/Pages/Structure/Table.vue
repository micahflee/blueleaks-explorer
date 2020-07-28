<style scoped>
.table-name {
  font-size: 1.2em;
}

.fields .field:first-child {
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}

.fields .field:last-child {
  margin-bottom: 0;
  border-bottom-right-radius: 4px;
  border-bottom-left-radius: 4px;
}

.fields .field {
  position: relative;
  display: block;
  width: 660px;
  padding: 10px 15px;
  margin-bottom: -1px;
  background-color: #fff;
  border: 1px solid #ddd;
}

.field-headers {
  font-weight: bold;
  position: relative;
  display: block;
  padding: 10px 15px;
  margin-bottom: -1px;
  border: 1px solid transparent;
}
.field-handle {
  display: inline-block;
  width: 40px;
}
i.field-handle {
  color: #999999;
  cursor: grab;
}
.field-name {
  display: inline-block;
  width: 450px;
}
.field-type {
  display: inline-block;
  width: 100px;
}
.field-show {
  display: inline-block;
  width: 50px;
}
</style>

<template>
  <div>
    <p class="table-name">
      <i class="fas fa-table"></i>
      <strong>{{ tableData['display'] }}</strong>
      <span class="meta">({{ table }})</span>
      <button v-on:click="changeDisplay()">Change</button>
      <button v-if="tableData['hidden']" v-on:click="changeHidden(false)">Show</button>
      <button v-else v-on:click="changeHidden(true)">Hide</button>
    </p>
    <template v-if="!tableData['hidden']">
      <div class="field-headers">
        <span class="field-handle">Sort</span>
        <span class="field-name">Field Name</span>
        <span class="field-type">Type</span>
        <span class="field-show">Show</span>
      </div>
      <draggable
        class="fields"
        handle=".field-handle"
        v-model="tableData['fields']"
        @end="makeDirty"
      >
        <div v-for="field in tableData['fields']" class="field">
          <Field v-bind:field="field" v-on:dirty="makeDirty()"></Field>
        </div>
      </draggable>
    </template>
  </div>
</template>

<script>
import Field from "./Field.vue";
import draggable from "vuedraggable";

export default {
  props: ["table", "tableData"],
  methods: {
    changeDisplay: function () {
      var display = prompt("New display name", this.tableData["display"]);
      if (display) {
        this.tableData["display"] = display;
        this.makeDirty();
      }
    },
    changeHidden: function (val) {
      this.tableData["hidden"] = val;
      this.$emit("dirty");
    },
    makeDirty: function () {
      this.$emit("dirty");
    },
  },
  components: {
    Field: Field,
    draggable: draggable,
  },
};
</script>