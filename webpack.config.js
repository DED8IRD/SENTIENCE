var HTMLWebpackPlugin = require('html-webpack-plugin');
var UglifyJSPlugin = require('uglifyjs-webpack-plugin');
var webpack = require('webpack');

var HTMLWebpackPluginConfig = new HTMLWebpackPlugin({
   template: __dirname + '/src/index.html',
   filename: 'index.html',
   inject: 'body'
});
var UglifyJSPluginConfig = new UglifyJSPlugin({
   extractComments: true
}); 

var WebpackProductionPlugin = new webpack.DefinePlugin({
   'process.env': {
      'NODE_ENV': JSON.stringify('production')
   }
});

module.exports = {
   entry: __dirname + '/src/index.js',
   module: {
      loaders: [
         {
            test: /\.jsx?$/,
            exclude: /node_modules/,
            loader: 'babel-loader'
         },
		 {
            test: /\.html$/,
            loader: 'raw-loader!html-minifier-loader'
         }
      ]
   },
   resolve: {
      extensions: ['.js', '.jsx'],
   },
   output: {
      filename: 'index.js',
      path: __dirname + '/build'
   },
   plugins: [
      HTMLWebpackPluginConfig,
	  UglifyJSPluginConfig,
      WebpackProductionPlugin
   ]
};
