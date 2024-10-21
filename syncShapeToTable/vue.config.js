const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  chainWebpack: (config) => {
    // Add a rule to handle .wasm files
    config.module
      .rule('wasm')
      .test(/\.wasm$/)
      .use('file-loader')
      .loader('file-loader')
      .options({
        name: '[name].[hash:8].[ext]',
        outputPath: 'wasm/', // Adjust the output directory as needed
      });

    // Set up output for the PGLite FS bundle
    config.output
      .globalObject('this'); // Ensure that the global object is set correctly for WebAssembly
  },
  configureWebpack: {
    experiments: {
      asyncWebAssembly: true, // Enable async WebAssembly if required
    },
  },
});
