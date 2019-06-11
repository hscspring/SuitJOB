export default {
  treeShaking: true,
  plugins: [
    ['umi-plugin-react', {
      antd: true,
      dva: true,
      dynamicImport: false,
      title: 'SuitJOB',
      dll: false,
      
      routes: {
        exclude: [
          /models\//,
          /services\//,
          /model\.(t|j)sx?$/,
          /service\.(t|j)sx?$/,
          /components\//,
        ],
      },
    }],
  ],
  routes: [
    {
      path: '/', component: '../layouts/index',
      routes: [
        { path: '/', component: '../pages/index' },
        { path: '/select', component: '../pages/select' },
        { path: '/submit', component: '../pages/submit' },
      ]
    }
  ],

  proxy: {
    '/api': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true,
    }
  },

    // cssLoaderOptions: {
    //     localIdentName: '[local]'
    // },

    // theme: './src/assets/css/theme.js',
  exportStatic: {},  
}
