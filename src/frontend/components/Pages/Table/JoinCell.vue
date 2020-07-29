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
</style>

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
    <span v-else>Unimplemented field type: {{ field['type'] }}</span>
  </div>
</template>

<script>
export default {
  props: ["site", "table", "field", "value"],
  methods: {
    htmlValue: function (html) {
      var html = html
        .replace(/\\n/g, " ")
        .replace(/\\t/g, " ")
        .replace(/POSITION: absolute;/g, "")
        .replace(/position:absolute;/g, "");
      return html;
    },
    preValue: function (value) {
      return value.replace(/\\n/g, "\n");
    },
    attachmentUrl: function (value) {
      var url =
        "/blueleaks-data/" + this.site + "/files/" + value.replace("\\", "/");
      return url;
    },
  },
};
</script>