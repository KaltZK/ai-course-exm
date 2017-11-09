module.exports = {
  entry: "./src/main.js",
  output: {
      path: __dirname+'/dist/',
      filename: "index.js"
  },
  module: {
    loaders: [
      { test: /\.js$/, exclude: /node_modules/, loader: "babel-loader"}
    ]
  }
};