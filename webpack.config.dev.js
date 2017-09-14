var HTMLWebpackPlugin = require('html-webpack-plugin');
var UglifyJSPlugin = require('uglifyjs-webpack-plugin');

var HTMLWebpackPluginConfig = new HTMLWebpackPlugin({
   template: __dirname + '/src/index.html',
   filename: 'index.html',
   inject: 'body'
});
var UglifyJSPluginConfig = new UglifyJSPlugin({
   extractComments: true
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
            exclude: /node_modules/,
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
	  UglifyJSPluginConfig
   ]
};
