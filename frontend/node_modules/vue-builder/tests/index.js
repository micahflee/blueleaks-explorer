const test = require('ava');
const fs = require('fs');
const webpack = require('./assets/webpack');
const {VueBuilder, VueRender} = require('../src');

test('VueBuilder.prototype.build', async (t) => {
  let config = webpack('client');

  let builder = new VueBuilder(config);
  await builder.build();

  t.is(fs.existsSync(`${__dirname}/../dist/client/images/logo.png`), true);
  t.is(fs.existsSync(`${__dirname}/../dist/client/bundle.js`), true);
});

test('VueBuilder.prototype.compile', async (t) => {
  let config = webpack('server');
  let builder = new VueBuilder(config);
  let source = await builder.compile();

  t.is(source.indexOf('module.exports ='), 0);
});

test('VueRender.prototype.renderToStream', async (t) => {
  let config = webpack('server');
  let builder = new VueBuilder(config);
  let source = await builder.compile();
  let render = new VueRender(source);
  let stream = render.renderToStream();

  t.is(!!stream.pipe, true);
});

test('VueRender.prototype.renderToString', async (t) => {
  let config = webpack('server');
  let builder = new VueBuilder(config);
  let source = await builder.compile();
  let render = new VueRender(source);
  let html = await render.renderToString();

  t.is(typeof html, 'string');
  t.is(html.indexOf('<div id="app" server-rendered="true">'), 0);
});
