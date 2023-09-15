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
    ]
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
      { text: 'Guide', link: '/guide/' },
      { text: 'Examples', link: '/examples/' },
      {
        text: 'Resources',
        items: [
          { text: 'API', link: 'https://trame.readthedocs.io/en/latest/index.html' },
          { text: 'Discussions', link: 'https://github.com/Kitware/trame/discussions' },
          { text: 'Bugs', link: 'https://github.com/Kitware/trame/issues' },
          { text: 'Contact Us', link: 'https://www.kitware.com/contact-us/' },
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
          text: 'Deployment',
          items: [
            { text: 'Python CLI', link: '/guide/deployment/pypi' },
            { text: 'Jupyter', link: '/guide/deployment/jupyter' },
            { text: 'Desktop', link: '/guide/deployment/desktop' },
            { text: 'Cloud', link: '/guide/deployment/cloud' },
            { text: 'HPC / Clusters', link: '/guide/deployment/hpc' },
            { text: 'NGINX', link: '/guide/deployment/nginx' },
          ]
        },
      ],
      '/examples/':[
        {
          text: 'Applications',
          items: [
            { text: 'Introduction', link: '/examples/apps/applications' },
            { text: 'ArrowFlow', link: '/examples/apps/arrow-flow' },
            { text: 'Vera Core', link: '/examples/apps/vera-core' },
            { text: 'XAITK', link: '/examples/apps/xaitk' },
            { text: 'MNIST', link: '/examples/apps/mnist' },
            { text: 'Peacock', link: '/examples/apps/peacock' },
            { text: 'PFB Viewer', link: 'https://github.com/Kitware/pfb-viewer' },
            { text: 'Conceptual Modeler', link: '/examples/apps/conceptual-modeler' },
            { text: 'ParFlow Simulation Modeler', link: 'https://github.com/Kitware/pf-simulation-modeler' },
            { text: 'Visualizer', link: 'https://github.com/Kitware/paraview-visualizer' },
            { text: 'Asynchronous ParaView', link: 'https://github.com/Kitware/async-paraview-app' },
          ]
        },
        {
          text: 'VTK',
          items: [
            { text: 'Finite Element Analysis', link: '/examples/vtk/fea' },
            { text: 'Multi-Filters', link: '/examples/vtk/multi' },
            { text: 'Selection', link: '/examples/vtk/selection' },
            { text: 'Surface Picking', link: '/examples/vtk/picking' },
            { text: 'PolyData Viewer', link: '/examples/vtk/vtp' },
            { text: 'ZARR Viewer', link: '/examples/vtk/zarr' },
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
        {
          text: 'Core functionalities',
          items: [
            { text: 'CLI', link: 'https://github.com/Kitware/trame/blob/master/examples/00_howdoi/cli.py' },
            { text: 'File Upload', link: 'https://github.com/Kitware/trame/blob/master/examples/00_howdoi/upload.py' },
            { text: 'Router', link: 'https://github.com/Kitware/trame/blob/master/examples/validation/core/10_router.py' },
            { text: 'Favicon', link: 'https://github.com/Kitware/trame/blob/master/examples/validation/core/12_reserved_state.py' },
            { text: 'MouseTrap', link: 'https://github.com/Kitware/trame/blob/master/examples/validation/core/16_mousetrap.py'},
            { text: 'Download text', link: 'https://github.com/Kitware/trame/blob/master/examples/validation/core/22_download_server_content.py' },
            { text: 'Download binary', link: 'https://github.com/Kitware/trame/blob/master/examples/validation/core/24_vtk_download_image.py' },
            { text: 'CSS', link: 'https://github.com/Kitware/trame/blob/master/examples/validation/core/28_css.py' },
            { text: 'Class decorator', link: 'https://github.com/Kitware/trame/blob/master/examples/validation/decorators/default_class_decorator.py' },
            { text: 'Panel comparison', link: 'https://github.com/Kitware/trame/blob/master/examples/validation/panel' },
            { text: 'Docker', link: 'https://github.com/Kitware/trame/blob/master/examples/deploy/docker/SingleFile' },
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
