<style scoped>
.label {
  font-weight: bold;
}

.html-value {
  background-color: white;
  max-width: 100%;
  max-height: 600px;
  overflow: auto;
}

ul.join-rows {
  list-style: none;
  padding: 0 0 0 1em;
}

li.join-row {
  margin-bottom: 1em;
  padding: 1em;
  background-color: #ddeaf5;
  border: 1px solid #c9d4dd;
}
</style>

<template>
  <div>
    <template v-if="loading">
      <div class="loading">
        <img src="/static/loading-small.gif" alt="Loading" />
      </div>
    </template>
    <template v-else>
      <div v-if="value != ''">
        <span class="label">{{ header }}:</span>
        <span v-if="fieldType == 'text'">{{ value }}</span>
        <span v-else-if="fieldType == 'pre'">
          <pre>{{ preValue(value) }}</pre>
        </span>
        <span v-else-if="fieldType == 'html'">
          <div class="html-value" v-html="htmlValue(value)"></div>
        </span>
        <span v-else-if="fieldType == 'image'">
          <img v-bind:src="attachmentUrl(value)" />
        </span>
        <span v-else-if="fieldType == 'attachment'">
          <a v-bind:href="attachmentUrl(value)" target="_blank">{{ value }}</a>
        </span>
        <span v-else-if="fieldType == 'join'">
          <ul class="join-rows">
            <li v-for="joinRow in joinRows" class="join-row">
              <JoinRow
                v-bind:siteFolder="siteFolder"
                v-bind:table="joinTable"
                v-bind:row="joinRow"
                v-bind:importantFields="joinImportantFields"
                v-bind:fieldTypes="joinFieldTypes"
                v-bind:headers="joinHeaders"
              ></JoinRow>
            </li>
          </ul>
        </span>
        <span v-else>Unimplemented field type: {{ fieldType }}</span>
      </div>
    </template>
  </div>
</template>

<script>
import JoinRow from "./JoinRow.vue";

export default {
  props: ["siteFolder", "table", "itemId", "header", "fieldType", "value"],
  data: function () {
    return {
      loading: false,
      joinTable: null,
      joinHeaders: null,
      joinRows: null,
      joinCount: null,
      joinImportantFields: null,
      joinFieldTypes: null,
    };
  },
  created: function () {
    if (this.fieldType == "join") {
      this.getJoin();
    }
  },
  methods: {
    getJoin: function () {
      var that = this;
      this.loading = true;
      fetch(
        "/api/" +
          this.siteFolder +
          "/" +
          this.table +
          "/join/" +
          this.header +
          "/" +
          this.itemId
      )
        .then(function (response) {
          if (response.status !== 200) {
            that.loading = false;
            console.log(
              "Error fetching join rows, status code: " + response.status
            );
            return;
          }
          response.json().then(function (data) {
            that.loading = false;
            that.joinTable = data["join_table"];
            that.joinHeaders = data["join_headers"];
            that.joinRows = data["join_rows"];
            that.joinCount = data["join_count"];
            that.joinImportantFields = data["join_important_fields"];
            that.joinFieldTypes = data["join_field_types"];

            // Fill in the default field types
            for (var i in that.joinHeaders) {
              if (!that.joinFieldTypes[that.joinHeaders[i]]) {
                that.joinFieldTypes[that.joinHeaders[i]] = "text";
              }
            }
          });
        })
        .catch(function (err) {
          that.loading = false;
          console.log("Error fetching join rows", err);
        });
    },
    htmlValue: function (value) {
      return value
        .replace(/\\n/g, " ")
        .replace(/\\t/g, " ")
        .replace(/POSITION: absolute;/g, "")
        .replace(/position:absolute;/g, "");
    },
    preValue: function (value) {
      return value.replace(/\\n/g, "\n");
    },
    attachmentUrl: function (value) {
      var url =
        "/blueleaks-data/" +
        this.siteFolder +
        "/files/" +
        value.replace("\\", "/");
      return url;
    },
  },
  components: {
    JoinRow: JoinRow,
  },
};
</script>