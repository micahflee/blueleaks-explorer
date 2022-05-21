<script setup>
const props = defineProps({
  totalItems: Number,
  perPageCount: Number,
  offset: Number,
  pageNavigateHandler: Function,
})

const currentPage = Math.ceil(this.offset / this.perPageCount) + 1;
const totalPages = Array.from({ length: Math.ceil(this.totalItems / this.perPageCount) }, (_, i) => i + 1);
</script>

<template>
  <ul>
    <template v-if="currentPage !== 1">
      <a href="#" class="prev-next" v-on:click.stop.prevent="pageNavigateHandler(currentPage - 1)">◀️</a>
    </template>
    <li v-for="page in totalPages" v-bind:key="page">
      <template v-if="page === currentPage">{{ page }}</template>
      <template v-else>
        <a href="#" v-on:click.stop.prevent="pageNavigateHandler(page)">{{
            page
        }}</a>
      </template>
    </li>
    <template v-if="currentPage !== totalPages.length">
      <a href="#" class="prev-next" v-on:click.stop.prevent="pageNavigateHandler(currentPage + 1)">▶️</a>
    </template>
  </ul>
</template>

<style scoped>
ul {
  padding: 0;
  margin: 0 0 5px 0;
  display: flex;
  justify-items: flex-start;
  align-items: flex-start;
  width: 95vw;
  flex-wrap: wrap;
}

li {
  list-style-type: none;
  padding: 3px;
}

.prev-next {
  text-decoration: none;
  position: relative;
  top: 4px;
}
</style>