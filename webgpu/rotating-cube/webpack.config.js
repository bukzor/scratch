// webpack.config.js
module.exports = {
  mode: "development",
  module: {
    rules: [
      {
        test: /\.wgsl$/i,
        use: "raw-loader",
      },
    ],
  },
};
