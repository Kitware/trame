import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  base: "trame",
  title: "trame",
  description: "Trame lets you weave various components and technologies into a Web Application solely written in Python",
  lastUpdated: true,
  head: [
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
    logo: '/logo-title.svg',
    siteTitle: false,
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Guide', link: '/docs/' },
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
      '/docs/':[
        {
          text: 'Getting Started',
          items: [
            { text: 'Introduction', link: '/docs/' },
            { text: 'How to start', link: '/docs/getting_started' },
            { text: 'API', link: '/docs/api' },
            { text: 'Cheatsheet', link: '/docs/cheatsheet' },
            { text: 'Course', link: '/docs/course_intro' },
            { text: 'Vue 2/3 client', link: '/docs/vue23' },
          ]
        },
        {
          text: 'Roadmap',
          items: [
            { text: 'Introduction', link: '/docs/trame_roadmap_intro' },
            { text: 'From 1 to 2', link: '/docs/trame_v1-2' },
            { text: 'From 2 to 3', link: '/docs/trame_v2-3' },
          ]
        },
        {
          text: 'Tutorial',
          items: [
            { text: 'Overview', link: '/docs/tutorial' },
            { text: 'Download', link: '/docs/tutorial-download' },
            { text: 'Setup for VTK', link: '/docs/tutorial-setup-vtk' },
            { text: 'VTK', link: '/docs/tutorial-vtk' },
            { text: 'Layouts', link: '/docs/tutorial-layouts' },
            { text: 'HTML', link: '/docs/tutorial-html' },
            { text: 'Application', link: '/docs/tutorial-application' },
            { text: 'ParaView', link: '/docs/tutorial-paraview' },
          ]
        },
        {
          text: 'Deployment',
          items: [
            { text: 'Python CLI', link: '/docs/deploy-pypi' },
            { text: 'Jupyter', link: '/docs/deploy-jupyter' },
            { text: 'Desktop', link: '/docs/deploy-desktop' },
            { text: 'Cloud', link: '/docs/deploy-cloud' },
            { text: 'HPC / Clusters', link: '/docs/deploy-hpc' },
            { text: 'NGINX', link: '/docs/deploy-nginx' },
          ]
        },
      ],
      '/examples/':[
        {
          text: 'Basic',
          items: [
            { text: 'Listing', link: '/examples/' },
            { text: 'Files', link: '/examples/files' },
            { text: 'Desktop', link: '/docs/deploy-desktop' },
            { text: 'Cloud', link: '/docs/deploy-cloud' },
            { text: 'HPC / Clusters', link: '/docs/deploy-hpc' },
            { text: 'NGINX', link: '/docs/deploy-nginx' },
          ]
        },
      ],
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/kitware/trame' }
    ],

    footer: {
      message: 'Released under the Apache 2 License.',
      copyright: 'Copyright © 2021-present Kitware Inc.'
    }
  },
})
