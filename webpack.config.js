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
            test: /\.js$/,
            exclude: /node_modules/,
            loader: 'babel-loader'
         },
		 {
            test: /\.html$/,
            loader: 'raw-loader!html-minifier-loader'
         }
      ]
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
