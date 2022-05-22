<script setup>
import { ref } from 'vue'
import JoinRow from "./JoinRow.vue";

const props = defineProps({
  site: String,
  table: String,
  itemId: Number,
  field: String,
  value: String,
  join: Object,
  isItem: Boolean
})

const loading = ref(false);
const joinTable = ref("");
const joinHeaders = ref([]);
const joinRows = ref([]);
const joinCount = ref(0);
const joinFields = ref([]);

function stripScripts(htmlString) {
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
}

function htmlValue(value) {
  return stripScripts(value)
    .replace(/\\n/g, " ")
    .replace(/\\t/g, " ")
    .replace(/POSITION: absolute;/g, "")
    .replace(/position:absolute;/g, "");
}

function preValue(value) {
  return value.replace(/\\n/g, "\n");
}

function attachmentUrl(value) {
  var url =
    "/blueleaks-data/" + props.site + "/files/" + value.replace("\\", "/");
  return url;
}

function surveyValue(value) {
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
}

function permalink() {
  return "/" + props.site + "/" + props.table + "/" + props.itemId;
}

if (props.join !== false) {
  // Get join
  loading.value = true;
  var url = "/api/" + props.site + "/" + props.table + "/join/" + props.join["name"] + "/" + props.itemId;
  // If this is viewing an item instead of a table, get all join rows instead of a limited set of them
  if (props.isItem) {
    url += "/all";
  }

  fetch(url)
    .then(function (response) {
      if (response.status !== 200) {
        loading.value = false;
        console.log(
          "Error fetching join rows, status code: " + response.status
        );
        return;
      }
      response.json().then(function (data) {
        loading.value = false;
        joinTable.value = data["join_table"];
        joinHeaders.value = data["join_headers"];
        joinRows.value = data["join_rows"];
        joinCount.value = data["join_count"];
        joinFields.value = data["join_fields"];
      });
    })
    .catch(function (err) {
      loading.value = false;
      console.log("Error fetching join rows", err);
    });
}
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