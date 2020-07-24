<style>
body {
  margin: 0;
  padding: 0 20px;
  font-family: sans-serif;
}

p {
  line-height: 150%;
}

li {
  line-height: 150%;
}

a:link,
a:visited {
  color: #28404f;
  text-decoration: underline;
}
a:active,
a:hover {
  color: #5d8fad;
  text-decoration: none;
}
</style>

<style scoped>
h1 {
  font-size: 2.3em;
  border-bottom: 5px solid cornflowerblue;
}
h1 i {
  color: cornflowerblue;
}
h1 a:link,
h1 a:visited,
h1 a:active,
h1 a:hover {
  text-decoration: none;
  color: cornflowerblue;
}
</style>

<template>
  <div>
    <h1>
      <i class="fas fa-cat"></i>
      <router-link to="/">BlueLeaks Explorer</router-link>
    </h1>
    <router-view></router-view>
  </div>
</template>
