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
  <div>
    <span class="label">{{ header }}:</span>
    <span class="value" v-if="fieldType == 'text'">{{ value }}</span>
    <span class="value" v-else-if="fieldType == 'html'">
      <div class="html-value" v-html="htmlValue(value)"></div>
    </span>
    <span class="value" v-else-if="fieldType == 'join'">TODO: join</span>
    <span class="value" v-else>Unimplemented field type: {{ fieldType }}</span>
  </div>
</template>

<script>
export default {
  props: ["header", "fieldType", "value"],
  methods: {
    htmlValue: function (html) {
      var html = html
        .replace(/\\n/g, " ")
        .replace(/\\t/g, " ")
        .replace(/POSITION: absolute;/g, "")
        .replace(/position:absolute;/g, "");
      return html;
    },
  },
};
</script>