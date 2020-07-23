const vsr = require('vue-server-renderer');
const MemoryFS = require('memory-fs');

/*
* Core class for building server-side and client-side bundles.
*/

exports.VueBuilder = class {

  /*
  * Class constructor.
  */

  constructor (config) {
    this._config = config; // instance of webpack compiler
  }

  /*
  * Returns a promise which saves application files to the destination folder.
  */

  build () {
    return new Promise((resolve, reject) => {
      let config = Object.assign({}, this._config); // webpack modifies input
      let webpack = require("webpack");

      let compiler = webpack(config);
      compiler.run((err, stats) => {
        if (err) {
          reject(err);
        }
        else {
          resolve(stats.compilation.assets)
        }
      });
    });
  }

  /*
  * Returns a promise which renders the application bundle and returns the
  * the source code as string.
  */

  compile () {
    return new Promise((resolve, reject) => {
      let mfs = new MemoryFS();
      let config = Object.assign({}, this._config); // webpack modifies input
      let webpack = require("webpack");

      let compiler = webpack(config);
      compiler.outputFileSystem = mfs;
      compiler.run((err, stats) => {
        if (err) {
          reject(err);
        }
        else {
          let filePath = `${compiler.options.output.path}/${compiler.options.output.filename}`.split('?')[0];
          let code = mfs.readFileSync(filePath, 'utf8');
          resolve(code);
        }
      });
    });
  }

}

/*
* Core class for server-side application rendering.
*/

exports.VueRender = class {

  /*
  * Class constructor.
  */

  constructor (source, options={}) {
    process.env.VUE_ENV = 'server';

    this.render = vsr.createBundleRenderer(source, options);
  }

  /*
  * Renders the application and returns a stream.
  */

  renderToStream (ctx={}) {
    let data = this.render.renderToStream(ctx);

    data.once('data', (chunk) => data.emit('init', ctx));

    return data;
  }

  /*
  * Returns a promise which renders the application and returns a string.
  */

  renderToString (ctx={}) {
    return new Promise((resolve, reject) => {
      this.render.renderToString(ctx, (err, data) => {
        if (err) {
          reject(err);
        }
        else {
          resolve(data);
        }
      });
    });
  }

}
