<style scoped>
.join {
  display: inline-block;
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
.join-name {
  display: inline-block;
  width: 250px;
}
.join-relationship {
  display: inline-block;
  width: 500px;
}
.join-delete {
  display: inline-block;
  width: 80px;
}
</style>

<template>
  <div class="join">
    <i class="handle fas fa-grip-horizontal"></i>
    <span class="join-name">{{ join['name'] }}</span>
    <span class="join-relationship">
      {{ join['from'] }}
      <i class="fas fa-hand-point-right"></i>
      {{ join['to'] }}
    </span>
    <span class="join-delete">
      <button v-on:click="deleteJoin">Delete</button>
    </span>
  </div>
</template>

<script>
export default {
  props: ["join"],
  methods: {
    makeDirty: function () {
      this.$emit("dirty");
    },
    deleteJoin: function () {
      this.$emit("delete");
    },
  },
};
</script>