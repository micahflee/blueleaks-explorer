<style scoped>
.searchbar {
  margin: 10px 0 5px 0;
  background-color: aliceblue;
  padding: 10px 10px 8px 10px;
  display: inline-block;
}

.search-header {
  display: inline-block;
  margin: 0 5px 0 0;
}

.search-form {
  display: inline-block;
}

.search-form input {
  padding: 5px 2px;
}
</style>

<template>
  <div class="searchbar">
    <span class="search-header">Search:</span>
    <form class="search-form" v-on:submit.prevent="handleSearchSubmit">
      <input type="text" v-model="term" name="searchTerm" />
      <button type="submit">Search</button>
    </form>
  </div>
</template>

<script>
export default {
  props: ["searchTerm", "handleSearchSubmit"],
  data: function () {
    return {
      term: this.searchTerm,
    };
  },
  methods: {},
  computed: {},
};
</script>
