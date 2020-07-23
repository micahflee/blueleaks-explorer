#!/usr/bin/env node

const config = require('./webpack.config.js');
const { VueBuilder } = require('vue-builder');

async function main() {
    const builder = new VueBuilder(config);
    let files = await builder.build();
    let source = await builder.compile();
}

main()