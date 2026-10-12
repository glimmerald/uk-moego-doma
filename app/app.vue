<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup>
useHead({
  htmlAttrs: {
    lang: 'ru'
  },
  titleTemplate: (titleChunk) => {
    return titleChunk ? `${titleChunk} | УК МОЕГО ДОМА` : 'УК МОЕГО ДОМА — премиальное управление жилой недвижимостью'
  }
})
</script>
