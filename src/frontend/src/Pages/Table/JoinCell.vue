<script setup>
const props = defineProps({
  site: String,
  table: String,
  field: String,
  value: String
})

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

function htmlValue(html) {
  var html = stripScripts(html)
    .replace(/\\n/g, " ")
    .replace(/\\t/g, " ")
    .replace(/POSITION: absolute;/g, "")
    .replace(/position:absolute;/g, "");
  return html;
}

function preValue(value) {
  return value.replace(/\\n/g, "\n");
}

function attachmentUrl(value) {
  var url =
    "/blueleaks-data/" + site + "/files/" + value.replace("\\", "/");
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

</script>

<template>
  <div v-if="field['show'] && value != ''">
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
      <a v-bind:href="attachmentUrl(value)" target="_blank">{{ value }}</a>
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

ul.survey-results {
  list-style: square;
  padding-left: 1em;
}

ul.survey-results .question {
  font-style: italic;
  color: #666666;
}
</style>