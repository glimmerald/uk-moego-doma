<template>
  <div class="layout-default">
    <AppHeader />
    <main class="layout-default__main">
      <slot />
    </main>
    <AppFooter />
  </div>
</template>

<style scoped>
.layout-default {
  min-height: var(--vh-100);
  display: flex;
  flex-direction: column;
}

.layout-default__main {
  flex: 1;
}
</style>
