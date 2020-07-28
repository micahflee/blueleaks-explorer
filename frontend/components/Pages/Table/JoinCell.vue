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
  <div v-if="value != '' && fieldType != 'join'">
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
    <span v-else>Unimplemented field type: {{ fieldType }}</span>
  </div>
</template>

<script>
export default {
  props: ["siteFolder", "table", "header", "fieldType", "value"],
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
        "/blueleaks-data/" +
        this.siteFolder +
        "/files/" +
        value.replace("\\", "/");
      return url;
    },
  },
};
</script>