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
  width: 100px;
}
.field-show {
  display: inline-block;
  width: 50px;
}

.join-name {
  display: inline-block;
  width: 250px;
}
.join-relationship {
  display: inline-block;
  width: 450px;
}
.join-delete {
  display: inline-block;
  width: 80px;
}
</style>

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
        <span class="field-show">Show</span>
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
            <option v-for="field in tableData['fields']">{{ field['name'] }}</option>
          </select>
          maps to table
          <select v-model="newRelationshipToTable">
            <option v-for="(otherTableData, otherTable) in structure['tables']">{{ otherTable }}</option>
          </select>
          <template v-if="newRelationshipToTable">
            field
            <select v-model="newRelationshipToField">
              <option
                v-for="field in structure['tables'][newRelationshipToTable]['fields']"
              >{{ field['name'] }}</option>
            </select>
            <button v-on:click="createRelationship">Create Relationship</button>
          </template>
        </p>
      </div>
    </template>
  </div>
</template>

<script>
import Field from "./Field.vue";
import Join from "./Join.vue";
import draggable from "vuedraggable";
import StructureVue from "../Structure.vue";

export default {
  props: ["table", "tableData", "structure"],
  data: function () {
    return {
      newRelationshipFromField: "",
      newRelationshipToTable: "",
      newRelationshipToField: "",
    };
  },
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
    createRelationship: function () {
      var name = prompt("What is the name of this relationship?");
      if (name) {
        this.structure["tables"][this.table]["joins"].push({
          name: name,
          from: this.table + "." + this.newRelationshipFromField,
          to: this.newRelationshipToTable + "." + this.newRelationshipToField,
        });
        this.newRelationshipFromField = "";
        this.newRelationshipToTable = "";
        this.newRelationshipToField = "";
        this.makeDirty();
      }
    },
    deleteJoin: function (join) {
      if (confirm("Are you sure?")) {
        var index = this.tableData["joins"].indexOf(join);
        this.tableData["joins"].splice(index, 1);
        this.$emit("dirty");
      }
    },
    makeDirty: function () {
      this.$emit("dirty");
    },
  },
  components: {
    Field: Field,
    Join: Join,
    draggable: draggable,
  },
};
</script>