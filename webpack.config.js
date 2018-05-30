const webpack = require('webpack');

module.exports = {
  devtool: 'cheap-module-source-map',
  entry: './frontend/modules/main.js',
  output: {
    filename: './frontend/js/bundle.js'
  },
  plugins: [
 new webpack.DefinePlugin({
  'process.env': {
    'NODE_ENV': JSON.stringify('debug')
  }
 })
 ],
  module: {

    loaders: [
      {
        test: /\.js$/,
        loader: 'babel-loader',
        query: {
          presets: ['es2015', 'react']
        }
      },
      {
        test: /\.json$/,
        loader: 'json-loader'
    },
      { test: /\.less$/, loader: 'style-loader!css-loader!less-loader' }, // use ! to chain loaders
      { test: /\.css$/, loader: 'style-loader!css-loader' },
      { test: /\.(png|jpg)$/, loader: 'url-loader?limit=8192' } // inline base64 URLs for <=8k images, direct URLs for the rest
    ]
  }
};
