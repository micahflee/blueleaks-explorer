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

a.button,
button {
  display: inline-block;
  border: 0;
  padding: 2px 6px;
  background: -webkit-gradient(
    linear,
    left top,
    left bottom,
    color-stop(0.05, #c123de),
    color-stop(1, #a20dbd)
  );
  background: -moz-linear-gradient(center top, #c123de 5%, #a20dbd 100%);
  filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#c123de', endColorstr='#a20dbd');
  background-color: #c123de;
  -webkit-border-top-left-radius: 5px;
  -moz-border-radius-topleft: 5px;
  border-top-left-radius: 5px;
  -webkit-border-top-right-radius: 5px;
  -moz-border-radius-topright: 5px;
  border-top-right-radius: 5px;
  -webkit-border-bottom-right-radius: 5px;
  -moz-border-radius-bottomright: 5px;
  border-bottom-right-radius: 5px;
  -webkit-border-bottom-left-radius: 5px;
  -moz-border-radius-bottomleft: 5px;
  border-bottom-left-radius: 5px;
  text-indent: 0;
  display: inline-block;
  color: #ffffff;
  font-family: arial;
  font-size: 13px;
  font-weight: bold;
  font-style: normal;
  line-height: 29px;
  text-decoration: none;
  text-align: center;
}
a.button:hover,
button:hover {
  background: -webkit-gradient(
    linear,
    left top,
    left bottom,
    color-stop(0.05, #a20dbd),
    color-stop(1, #c123de)
  );
  background: -moz-linear-gradient(center top, #a20dbd 5%, #c123de 100%);
  filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#a20dbd', endColorstr='#c123de');
  background-color: #a20dbd;
  cursor: pointer;
}
a.button:active,
button:active {
  position: relative;
  top: 1px;
}

ul.rows {
  list-style: none;
  padding: 0;
}

li.row {
  font-family: "Courier New", Courier, monospace;
  margin-bottom: 1em;
  padding: 1em;
  background-color: aliceblue;
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
