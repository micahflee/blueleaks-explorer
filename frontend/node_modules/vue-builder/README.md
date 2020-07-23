![Build Status](https://travis-ci.org/xpepermint/vue-builder.svg?branch=master)&nbsp;[![NPM Version](https://badge.fury.io/js/vue-builder.svg)](https://badge.fury.io/js/vue-builder)&nbsp;[![Dependency Status](https://gemnasium.com/xpepermint/vue-builder.svg)](https://gemnasium.com/xpepermint/vue-builder)

# [vue](http://vuejs.org)-[builder](https://webpack.github.io)

> Server-side and client-side rendering for Vue.js.

<img src="logo.png" height="60" style="margin-bottom: 20px" />

This package provides tools for rendering [Vue.js](http://vuejs.org) applications server-side and client-side using the [Webpack](https://webpack.github.io) module bundler.

This is an open source package for [Vue.js](http://vuejs.org/). The source code is available on [GitHub](https://github.com/xpepermint/vue-builder) where you can also find our [issue tracker](https://github.com/xpepermint/vue-builder/issues).

## Related

### Packages

* [express-vue-builder](https://github.com/xpepermint/express-vue-builder): Vue.js server-side rendering middleware for Express.js.
* [express-vue-dev](https://github.com/xpepermint/express-vue-dev): Vue.js development server middleware for Express.js.
* [koa-vue-builder](https://github.com/kristianmandrup/koa-vue-builder): Vue.js server-side rendering middleware for Koa.js.
* [koa-vue-dev](https://github.com/kristianmandrup/koa-vue-dev): Vue.js development server middleware for Koa.js.
* [vue-cli-template](https://github.com/xpepermint/vue-cli-template): A simple server-side rendering CLI template for Vue.js.

### Examples

* [vue-example](https://github.com/xpepermint/vue-example): Vue.js example application

## Install

Run the command below to install the package.

```
$ npm install --save-dev vue vue-server-renderer
$ npm install --save-dev vue-builder
```

## Usage

Create a Webpack configuration object then use the `VueBuilder` class to build and compile the application.

```js
const config = require('./webpack.config.js'); /* your webpack configuration */
const {VueBuilder} = require('vue-builder');

// create Vue.js builder
const builder = new VueBuilder(config);
// build application to ./dist
let files = await builder.build();
// build application entry to string
let source = await builder.compile();
```

Use the `VueRender` class to render the application.

```js
const {VueBuilder} = require('vue-builder');

// create Vue.js renderer
const render = new VueRender(source); // source=builder.render()
// render to stream
let stream = render.renderToStream();
// render to string
let html = await render.renderToString();
```

## API

**VueBuilder(config)**

> Core class for building server-side and client-side bundles.

| Option | Type | Required | Default | Description
|--------|------|----------|---------|------------
| config | Object | Yes | - | Webpack configuration object.

**VueBuilder.prototype.build()**:Promise

> Returns a promise which saves application files to the destination folder.

**VueBuilder.prototype.compile()**:Promise

> Returns a promise which compiles the application bundle and returns the the source code as string.

**VueRender(source, options)**

> Core class for server-side application rendering.

| Option | Type | Required | Default | Description
|--------|------|----------|---------|------------
| source | String | Yes | - | Bundle source code.
| options | Object | No | - | [Renderer options](https://www.npmjs.com/package/vue-server-renderer#renderer-options).

**VueRender.prototype.renderToStream(ctx)**:Stream

> Renders the application and returns a stream.

| Option | Type | Required | Default | Description
|--------|------|----------|---------|------------
| ctx | Object | No | {} | Application context object.

**VueRender.prototype.renderToString(ctx)**:Promise

> Returns a promise which renders the application and returns a string.

| Option | Type | Required | Default | Description
|--------|------|----------|---------|------------
| ctx | Object | No | {} | Application context object.

## License (MIT)

```
Copyright (c) 2016 Kristijan Sedlak <xpepermint@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```
