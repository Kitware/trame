import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  base: "/trame",
  title: "trame",
  description: "Trame lets you weave various components and technologies into a Web Application solely written in Python",
  lastUpdated: true,
  head: [
    ['link', { rel: "apple-touch-icon", sizes: "196x196", href: "/trame/logos/favicon-196x196.png"}],
    ['link', { rel: "icon", type: "image/png", sizes: "32x32", href: "/trame/logos/favicon-32x32.png"}],
    ['link', { rel: "icon", type: "image/png", sizes: "16x16", href: "/trame/logos/favicon-16x16.png"}],
    [
      'script',
      { async: '', src: 'https://www.googletagmanager.com/gtag/js?id=G-H4W9XHTJ7X' }
    ],
    [
      'script',
      {},
      `window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-H4W9XHTJ7X');`
    ],
    [
      'script',
      { 
        async: '', 
        src: 'https://widget.gurubase.io/widget.latest.min.js', 
        id: 'guru-widget-id',
        'data-widget-id': 'RC2sPqrQBnNKn3MJcyQacPVdhrHIQUJgiKg8nmgBiSs',
        'data-icon-url': 'https://kitware.github.io/trame/logos/favicon-196x196.png',
      }
    ],
  ],
  themeConfig: {
    search: {
      provider: 'local'
    },
    logo: '/logos/trame-text.svg',
    siteTitle: false,
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'News', link: '/news' },
      { text: 'Guide', link: '/guide/' },
      { text: 'Examples', link: '/examples/' },
      {
        text: 'Resources',
        items: [
          { text: 'API', link: 'https://trame.readthedocs.io/en/latest/index.html' },
          { text: 'Discussions', link: 'https://github.com/Kitware/trame/discussions' },
          { text: 'Bugs', link: 'https://github.com/Kitware/trame/issues' },
          { text: 'Services', link: 'https://www.kitware.com/trame/' },
        ]
      }
    ],

    sidebar: {
      '/guide/':[
        {
          text: 'Getting Started',
          items: [
            { text: 'Introduction', link: '/guide/' },
            { text: 'How to start', link: '/guide/intro/getting_started' },
            { text: 'API', link: '/guide/intro/api' },
            { text: 'Cheatsheet', link: '/guide/intro/cheatsheet' },
            { text: 'Course', link: '/guide/intro/course' },
            // { text: 'Vue 2/3 client', link: '/guide/intro/vue23' },
            { text: 'Widgets', link: '/guide/intro/widgets' },
            { text: 'Citing', link: '/guide/intro/citing' },
          ]
        },
        {
          text: 'Versions: 1, 2, 3',
          items: [
            { text: 'Introduction', link: '/guide/versions/' },
            { text: 'From 1 to 2', link: '/guide/versions/trame_v1-2' },
            { text: 'From 2 to 3', link: '/guide/versions/trame_v2-3' },
          ]
        },
        {
          text: 'Tutorial',
          items: [
            { text: 'Overview', link: '/guide/tutorial/' },
            { text: 'Download', link: '/guide/tutorial/download' },
            { text: 'Setup for VTK', link: '/guide/tutorial/setup' },
            { text: 'VTK', link: '/guide/tutorial/vtk' },
            { text: 'Layouts', link: '/guide/tutorial/layouts' },
            { text: 'HTML', link: '/guide/tutorial/html' },
            { text: 'Application', link: '/guide/tutorial/application' },
            { text: 'ParaView', link: '/guide/tutorial/paraview' },
          ]
        },
        {
          text: 'Jupyter',
          items: [
            { text: 'Trame in Jupyter', link: '/guide/jupyter/intro' },
            { text: 'Code example', link: '/guide/jupyter/sample-code' },
            { text: 'How it works', link: '/guide/jupyter/how-it-works' },
            { text: 'Advanced usecase', link: '/guide/jupyter/advanced' },
            { text: 'Trame extension', link: '/guide/jupyter/extension' },
          ]
        },
        {
          text: 'Deployment',
          items: [
            { text: 'Python CLI', link: '/guide/deployment/pypi' },
            { text: 'Jupyter', link: '/guide/jupyter/intro' },
            { text: 'Desktop', link: '/guide/deployment/desktop' },
            { text: 'Cloud', link: '/guide/deployment/cloud' },
            { text: 'HPC / Clusters', link: '/guide/deployment/hpc' },
            { text: 'NGINX', link: '/guide/deployment/nginx' },
            { text: 'Docker', link: '/guide/deployment/docker' },
          ]
        },
      ],
      '/examples/':[
        {
          text: 'Core functionalities',
          items: [
            { text: 'Basics', link: '/examples/core/basics' },
            { text: 'Files', link: '/examples/core/files' },
            { text: 'Jupyter', link: '/examples/core/jupyter' },
            { text: 'Plotly', link: '/examples/core/plotly' },
            { text: 'Docker', link: '/examples/core/docker' },
            // router, docker
          ]
        },
        {
          text: 'Applications',
          items: [
            { text: 'Introduction', link: '/examples/apps/applications' },
            { text: 'ArrowFlow', link: '/examples/apps/arrow-flow' },
            { text: 'Vera Core', link: '/examples/apps/vera-core' },
            { text: 'XAITK', link: '/examples/apps/xaitk' },
            { text: 'MNIST', link: '/examples/apps/mnist' },
            { text: 'Peacock', link: '/examples/apps/peacock' },
            { text: 'Visualizer', link: '/examples/apps/visualizer' },
            { text: 'Conceptual Modeler', link: '/examples/apps/conceptual-modeler' },
            // { text: 'Asynchronous ParaView', link: 'https://github.com/Kitware/async-paraview-app' },
            // { text: 'PFB Viewer', link: 'https://github.com/Kitware/pfb-viewer' },
            // { text: 'ParFlow Simulation Modeler', link: 'https://github.com/Kitware/pf-simulation-modeler' },
            { text: 'Community', link: '/examples/apps/community' },
          ]
        },
        {
          text: 'VTK',
          items: [
            { text: 'WASM', link: '/examples/vtk/wasm' },
            { text: 'Finite Element Analysis', link: '/examples/vtk/fea' },
            { text: 'Multi-Filters', link: '/examples/vtk/multi' },
            { text: 'Selection', link: '/examples/vtk/selection' },
            { text: 'Surface Picking', link: '/examples/vtk/picking' },
            { text: 'PolyData Viewer', link: '/examples/vtk/vtp' },
            { text: 'ZARR Viewer', link: '/examples/vtk/zarr' },
            { text: 'More examples', link: '/examples/vtk/examples' },
          ]
        },
        {
          text: 'ParaView',
          items: [
            { text: 'Contour Geometry', link: '/examples/paraview/contour' },
            { text: 'Picking', link: '/examples/paraview/picking' },
            { text: 'Simple Cone', link: '/examples/paraview/cone' },
            { text: 'State loader', link: '/examples/paraview/state' },
          ]
        },
      ],
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/kitware/trame' }
    ],

    footer: {
      copyright: 'Copyright © 2021-present Kitware Inc.'
    }
  },
})
