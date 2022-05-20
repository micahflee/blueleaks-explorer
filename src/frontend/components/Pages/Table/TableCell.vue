<script>
import JoinRow from "./JoinRow.vue";

export default {
  props: ["site", "table", "itemId", "field", "value", "join", "isItem"],
  data: function () {
    return {
      loading: false,
      joinTable: null,
      joinHeaders: null,
      joinRows: null,
      joinCount: null,
      joinFields: null,
    };
  },
  created: function () {
    if (this.join) {
      this.getJoin();
    }
  },
  methods: {
    getJoin: function () {
      var that = this;
      this.loading = true;

      var url =
        "/api/" +
        this.site +
        "/" +
        this.table +
        "/join/" +
        this.join["name"] +
        "/" +
        this.itemId;
      // If this is viewing an item instead of a table, get all join rows instead of a limited set of them
      if (this.isItem) {
        url += "/all";
      }

      fetch(url)
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
            that.joinFields = data["join_fields"];
          });
        })
        .catch(function (err) {
          that.loading = false;
          console.log("Error fetching join rows", err);
        });
    },
    stripScripts: function (htmlString) {
      const div = document.createElement("div");
      div.innerHTML = htmlString;
      const scripts = div.getElementsByTagName("script");
      let i = scripts.length;
      while (i--) {
        scripts[i].parentNode.removeChild(scripts[i]);
      }

      const base = div.getElementsByTagName("base");
      i = base.length;
      while (i--) {
        base[i].parentNode.removeChild(base[i]);
      }

      return div.innerHTML;
    },
    htmlValue: function (value) {
      return this.stripScripts(value)
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
        "/blueleaks-data/" + this.site + "/files/" + value.replace("\\", "/");
      return url;
    },
    surveyValue: function (value) {
      var results = [];
      var pairs = value.split(",");
      for (var i = 0; i < pairs.length; i++) {
        var parts = pairs[i].split("=");
        var question = parts[0];
        var answer = parts[1]
          ? decodeURIComponent(parts[1].replace(/\+/g, " "))
          : "";
        if (question != "Submit" && question != "" && answer != "") {
          results.push({ question: question, answer: answer });
        }
      }
      return results;
    },
    permalink: function () {
      return "/" + this.site + "/" + this.table + "/" + this.itemId;
    },
  },
  components: {
    JoinRow: JoinRow,
  },
};
</script>

<template>
  <div>
    <template v-if="loading">
      <div class="loading">
        <img src="/static/loading-small.gif" alt="Loading" />
      </div>
    </template>
    <template v-else>
      <template v-if="join">
        <template v-if="joinCount > 0">
          <span class="label">{{ join['name'] }}:</span>
          <template v-if="joinRows.length != joinCount">
            <p>
              <span class="meta">Showing {{ joinRows.length }} out of {{ joinCount }} items</span>
              <router-link class="button secondary" v-bind:to="permalink()">See All Items</router-link>
            </p>
          </template>
          <template v-else>
            <template v-if="joinCount > 1">
              <p>
                <span class="meta">Showing {{ joinCount }} items</span>
              </p>
            </template>
          </template>
          <ul class="join-rows">
            <li v-for="joinRow in joinRows" class="join">
              <JoinRow v-bind:site="site" v-bind:table="joinTable" v-bind:row="joinRow" v-bind:fields="joinFields"
                v-bind:headers="joinHeaders"></JoinRow>
            </li>
          </ul>
        </template>
      </template>
      <template v-else>
        <template v-if="value != ''">
          <span class="label">{{ field['name'] }}:</span>
          <span v-if="field['type'] == 'text'">{{ value }}</span>
          <span v-else-if="field['type'] == 'pre'">
            <pre>{{ preValue(value) }}</pre>
          </span>
          <span v-else-if="field['type'] == 'html'">
            <div class="html-value" v-html="htmlValue(value)"></div>
          </span>
          <span v-else-if="field['type'] == 'image'">
            <img v-bind:src="attachmentUrl(value)" />
          </span>
          <span v-else-if="field['type'] == 'attachment'">
            <a v-bind:href="attachmentUrl(value)" target="_blank">
              {{
                  value
              }}
            </a>
          </span>
          <span v-else-if="field['type'] == 'survey'">
            <ul class="survey-results">
              <li v-for="result in surveyValue(value)">
                <span class="question">{{ result['question'] }}</span>
                <br />
                <span class="answer">{{ result['answer'] }}</span>
              </li>
            </ul>
          </span>
          <span v-else>Unimplemented field type: {{ field['type'] }}</span>
        </template>
      </template>
    </template>
  </div>
</template>

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

ul {
  list-style: none;
  padding: 0;
}

li.join {
  margin-bottom: 1em;
  padding: 1em;
  background-color: #ddeaf5;
  border: 1px solid #c9d4dd;
}

ul.survey-results {
  list-style: square;
  padding-left: 1em;
}

ul.survey-results .question {
  font-style: italic;
  color: #666666;
}
</style>