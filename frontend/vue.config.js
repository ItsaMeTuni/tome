const isDev = process.env.NODE_ENV === 'development';

module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  configureWebpack: {
    devtool: isDev && 'eval-source-map'
  }
}
