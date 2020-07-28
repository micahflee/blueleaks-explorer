<style scoped>
.dirty {
  color: red;
  font-style: italic;
}

.meta {
  font-weight: 100;
  color: #666666;
}

ul {
  list-style: none;
  padding: 0;
}

ul.tables li.table {
  margin-bottom: 2em;
}

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
  width: 610px;
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
  width: 50px;
}
.field-show {
  display: inline-block;
  width: 50px;
}
</style>

<template>
  <div>
    <template v-if="loading">
      <div class="loading">
        <img src="/static/loading.gif" alt="Loading" />
      </div>
    </template>
    <template v-else>
      <template v-if="dirty">
        <p class="dirty">
          You have unsaved changed.
          <button v-on:click="save">Save</button>
        </p>
      </template>
      <template v-if="structure != null">
        <h2>
          <i class="fas fa-sitemap"></i>
          {{ structure["name"] }}
          <span class="meta">({{ site }})</span>
          <button v-on:click="changeName">Change</button>
        </h2>

        <ul class="tables">
          <li v-for="(table_data, table) in structure['tables']" class="table">
            <p class="table-name">
              <i class="fas fa-table"></i>
              <strong>{{ table_data['display'] }}</strong>
              <span class="meta">({{ table }})</span>
              <button v-on:click="changeTableDisplay">Change</button>
            </p>
            <div class="field-headers">
              <span class="field-handle">Sort</span>
              <span class="field-name">Field Name</span>
              <span class="field-type">Type</span>
              <span class="field-show">Show</span>
            </div>
            <draggable
              class="fields"
              handle=".field-handle"
              v-model="structure['tables'][table]['fields']"
              @end="changeFieldOrder"
            >
              <div v-for="field in structure['tables'][table]['fields']" class="field">
                <i class="field-handle fas fa-grip-horizontal"></i>
                <span class="field-name">{{ field['name'] }}</span>
                <span class="field-type">{{ field['type'] }}</span>
                <span class="field-show">
                  <input type="checkbox" />
                </span>
              </div>
            </draggable>
          </li>
        </ul>
      </template>
    </template>
  </div>
</template>

<script>
import draggable from "vuedraggable";

export default {
  data: function () {
    return {
      loading: false,
      site: this.$route.path.split("/")[2],
      dirty: false,
      structure: null,
    };
  },
  created: function () {
    this.getStructure();
  },
  methods: {
    getStructure: function () {
      var that = this;
      this.loading = true;
      fetch("/api/structure/" + this.site)
        .then(function (response) {
          that.loading = false;

          if (response.status !== 200) {
            console.log(
              "Error fetching structure, status code: " + response.status
            );
            return;
          }
          response.json().then(function (data) {
            if (data["error"]) {
              alert(data["error_message"]);
              that.$router.push({ path: "/structure" });
            } else {
              that.structure = data["structure"];
            }
          });
        })
        .catch(function (err) {
          that.loading = false;
          console.log("Error fetching structure", err);
        });
    },
    save: function () {
      var that = this;
      this.loading = true;
      fetch("/api/structure/" + this.site, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(this.structure),
      })
        .then(function (response) {
          that.loading = false;

          if (response.status !== 200) {
            console.log(
              "Error saving structure, status code: " + response.status
            );
            return;
          }
          response.json().then(function (data) {
            if (data["error"]) {
              alert(data["error_message"]);
            } else {
              that.dirty = false;
            }
          });
        })
        .catch(function (err) {
          that.loading = false;
          console.log("Error saving structure", err);
        });
    },
    changeName: function () {
      var name = prompt(
        "What's the name of this site?",
        this.structure["name"]
      );
      if (name) {
        this.structure["name"] = name;
        this.dirty = true;
      }
    },
    changeTableDisplay: function (table) {
      var display = prompt(
        "New display name",
        this.structure["tables"][table]["display"]
      );
      if (display) {
        this.structure["tables"][table]["display"] = display;
        this.dirty = true;
      }
    },
    changeFieldOrder: function (event) {
      this.dirty = true;
    },
  },
  components: {
    draggable: draggable,
  },
};
</script>