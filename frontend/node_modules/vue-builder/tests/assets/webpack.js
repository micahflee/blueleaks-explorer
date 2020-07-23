const {join} = require('path');
const webpack = require('webpack');

module.exports = (mode) => ({
  context: join(__dirname, 'app'),
  target: mode === 'client' ? 'web' : 'node',
  devtool: '#eval-source-map',
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      },
      {
        test: /\.json$/,
        loader: 'json-loader'
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        loader: 'file-loader',
        options: {
          name: `[path][name].[ext]?[hash]`
        }
      }
    ]
  },
  entry: [
    join(__dirname, 'app', `${mode}-entry.js`)
  ],
  output: {
    path: join(__dirname, '..', '..', 'dist', mode),
    filename: `bundle.js?[hash]`,
    publicPath: '/',
    libraryTarget: mode === 'client' ? 'var' : 'commonjs2'
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('production'),
      'process.env.VUE_ENV': JSON.stringify(mode)
    })
  ]
});
