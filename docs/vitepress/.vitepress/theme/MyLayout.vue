<!--.vitepress/theme/MyLayout.vue-->
<script setup>
import DefaultTheme from 'vitepress/theme'
import GithubButton from 'vue-github-button'

const { Layout } = DefaultTheme
</script>

<template>
  <Layout>
    <template #home-hero-image>
        <iframe
            class="hero-video"
            src="https://player.vimeo.com/video/764741737?h=bd3c37ebfb&title=0&byline=0&portrait=0&muted=1&autoplay=1&loop=1&background=1"
            frameborder="0"
            allow="autoplay;"
            allowfullscreen
            muted
        >
        </iframe>
    </template>
    <template #nav-bar-content-after>
      <github-button
          style="margin: 5px 1rem 0 1rem;"
          href="https://github.com/kitware/trame"
          data-icon="octicon-star"
          data-show-count="false"
          aria-label="Star kitware/trame on GitHub"
      />
      <img src="https://img.shields.io/pypi/dm/trame" />
    </template>
  </Layout>
</template>

<style scoped>
  .hero-video {
    margin-top: calc((var(--vp-nav-height) + var(--vp-layout-top-height, 0px)) * -1);
    padding: calc(var(--vp-nav-height) + var(--vp-layout-top-height, 0px) + 48px) 24px 48px;
    height: 300px;
  }

  @media (min-width: 640px) {
    .hero-video {
      height: 400px;
    }
  }
  @media (min-width: 960px) {
    .hero-video {
      margin-left: 2rem; 
      width: 100%; 
      height: 450px;
    }
  }
</style>