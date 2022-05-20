<script>
export default {
  props: ["headers", "currentSort", "sortChangeHandler"],
  data: function () {
    return {
      selectedSort: this.currentSort,
    };
  },
  methods: {},
  computed: {
    options: function () {
      return [{ val: null, display: "Sort Option" }].concat(
        this.headers
          //   .filter((h) => badOptions.indexOf(h.toLowerCase()) === -1)
          .reduce((acc, header) => {
            return acc.concat([
              {
                val: `${header}##ASC`,
                display: `${header} ⬆️`,
              },
              {
                val: `${header}##DESC`,
                display: `${header} ⬇️`,
              },
            ]);
          }, [])
      );
    },
  },
};
</script>

<template>
  <div class="sortbar">
    <span class="sort-header">Sort By:</span>
    <select v-model="selectedSort" v-on:change="sortChangeHandler">
      <option v-for="option in options" v-bind:value="option.val" v-bind:key="option.val">{{ option.display }}</option>
    </select>
  </div>
</template>

<style scoped>
.sortbar {
  margin: 10px 0 5px 0;
  background-color: aliceblue;
  padding: 17px 10px 15px 10px;
  display: inline-block;
}

.sort-header {
  display: inline-block;
  margin: 0 5px 0 0;
}
</style>