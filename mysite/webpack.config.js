var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
  context: __dirname,

  entry: './assets/js/index.js',

  output: {
      path: path.resolve('./assets/bundles/'),
      filename: "[name]-[hash].js",
  },


  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      jquery: "jquery"
    })
  ],

   module: {
    rules: [
      { test: /\.jsx?$/, exclude: /node_modules/, loader: 'babel-loader' }, // to transform JSX into JS
      { test: /\.(scss)?$/, loader: 'style-loader' },
      { test: /\.(scss)?$/, loader: 'css-loader' },
      { test: /\.(scss)?$/, loader: 'sass-loader' },
      { test: /\.(css)?$/, loader: 'css-loader' },
      { test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "file-loader" },
      { test: /\.(jpe?g|png|gif|svg)$/i, loader: 'file-loader' },
      { test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "url-loader" },
   ],
  },

  resolve: {
      extensions: ['.js', '.jsx'],
      modules: [ path.resolve(__dirname, 'node_modules')] // modulesDirectories: ['node_modules', 'bower_components'], on Webpack 1
  }
}
