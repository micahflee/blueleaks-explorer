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

div.loading {
  text-align: center;
  margin: 100px 0;
}

pre {
  white-space: pre-wrap;
  background-color: white;
}

.meta {
  color: #333333;
  font-style: italic;
}
</style>

  <style scoped>
header {
  border-bottom: 5px solid cornflowerblue;
}
h1 {
  font-size: 2.3em;
  display: inline-block;
  padding-right: 1em;
  margin: 1em 0 0 0;
  color: cornflowerblue;
}
h1 i {
  color: cornflowerblue;
}

ul {
  display: inline-block;
  list-style: none;
  margin: 0;
  padding: 0;
  vertical-align: middle;
}
ul li {
  display: inline-block;
  padding: 3px 10px;
}
ul li a {
  border: 0;
  padding: 5px;
  text-decoration: none;
  color: #5d8fad;
  font-weight: bold;
}
ul li i {
  color: #5d8fad;
}
</style>

<template>
  <div>
    <header>
      <h1>
        <i class="fas fa-cat"></i> BlueLeaks Explorer
      </h1>
      <ul>
        <li>
          <i class="fas fa-user-astronaut"></i>
          <router-link to="/">Explore Data</router-link>
        </li>
        <li>
          <i class="fas fa-tools"></i>
          <router-link to="/structure">Define Structure</router-link>
        </li>
        <li>
          <i class="fas fa-folder-open"></i>
          <a href="/blueleaks-data/">Browse Files</a>
        </li>
      </ul>
    </header>
    <router-view></router-view>
  </div>
</template>
