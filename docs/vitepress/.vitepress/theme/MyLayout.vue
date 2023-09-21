<!--.vitepress/theme/MyLayout.vue-->
<script setup>
import DefaultTheme from 'vitepress/theme'

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