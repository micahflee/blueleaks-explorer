<style scoped>
.field {
  position: relative;
  display: block;
  width: 660px;
  padding: 10px 15px;
  margin-bottom: -1px;
  background-color: #fff;
  border: 1px solid #ddd;
}

.handle {
  display: inline-block;
  width: 40px;
}
i.handle {
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
  <div class="field">
    <i class="handle fas fa-grip-horizontal"></i>
    <span class="field-name">{{ field['name'] }}</span>
    <span class="field-type">
      <select v-model="field['type']" v-on:change="makeDirty()">
        <option>text</option>
        <option>html</option>
        <option>pre</option>
        <option>image</option>
        <option>attachment</option>
      </select>
    </span>
    <span class="field-show">
      <input type="checkbox" v-model="field['show']" v-on:change="makeDirty()" />
    </span>
  </div>
</template>

<script>
export default {
  props: ["field"],
  methods: {
    makeDirty: function () {
      this.$emit("dirty");
    },
  },
};
</script>