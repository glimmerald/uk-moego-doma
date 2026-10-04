<template>
  <header :class="['app-header', 'glass-effect', { 'is-menu-open': isMenuOpen }]">
    <div class="app-header__container">
      <div class="app-header__logo">
        <NuxtLink to="/">УК МОЕГО ДОМА</NuxtLink>
      </div>
      
      <!-- Центральное меню убрано по ТЗ -->
      <div class="app-header__spacer"></div>

      <div class="app-header__actions">
        <a :href="contactsData.reception.link" class="app-header__phone">
          <span class="app-header__phone-label">{{ contactsData.reception.label }}:</span> {{ contactsData.reception.phone }}
        </a>
        <a :href="contactsData.dispatch.link" class="app-header__phone">
          <span class="app-header__phone-label">АДС:</span> {{ contactsData.dispatch.phone }}
        </a>
        <button 
          class="app-header__burger" 
          @click="toggleMenu"
          :class="{ 'is-active': isMenuOpen }"
        >
          <span class="app-header__burger-line"></span>
          <span class="app-header__burger-line"></span>
        </button>
      </div>
    </div>

    <!-- Оверлей затемнения -->
    <Transition name="fade">
      <div 
        class="app-menu__overlay" 
        v-if="isMenuOpen" 
        @click="closeMenu"
        @touchmove.prevent
      ></div>
    </Transition>

    <!-- Выезжающая панель меню -->
    <Transition name="slide">
      <div class="app-menu__panel" v-if="isMenuOpen">
        
        <!-- Локальные ссылки (для текущей страницы) -->
        <div class="app-menu__section" v-if="localMenu">
          <div class="app-menu__subtitle">{{ localMenu.title }}</div>
          <nav class="app-menu__nav">
            <a 
              v-for="item in localMenu.items" 
              :key="item.link" 
              :href="item.link"
              class="app-menu__link"
              @click.prevent="handleNavClick(item.link)"
            >
              {{ item.title }}
            </a>
          </nav>
        </div>

        <!-- Разделитель, если есть и локальные, и глобальные ссылки -->
        <div class="app-menu__divider" v-if="localMenu"></div>

        <!-- Глобальные ссылки (для всех страниц) -->
        <div class="app-menu__section">
          <div class="app-menu__subtitle">Разделы</div>
          <nav class="app-menu__nav">
            <a 
              v-for="item in menuData.global" 
              :key="item.link" 
              :href="item.link"
              class="app-menu__link app-menu__link--global"
              @click.prevent="handleNavClick(item.link)"
            >
              {{ item.title }}
            </a>
          </nav>
        </div>
        
      </div>
    </Transition>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { useRoute } from 'nuxt/app'
import menuData from '@/assets/data/menu.json'
import contactsData from '@/assets/data/contacts.json'

const route = useRoute()
const isMenuOpen = ref(false)

const localMenu = computed(() => {
  return menuData.local[route.name] || null
})

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
  isMenuOpen.value = false
}

const handleNavClick = (link) => {
  closeMenu()
  
  if (link.startsWith('/#') && route.path === '/') {
    const hash = link.replace('/', '')
    
    setTimeout(() => {
      const el = document.querySelector(hash)
      if (el) {
        const headerOffset = 80
        const elementPosition = el.getBoundingClientRect().top
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset
        
        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        })
      }
    }, 150)
  } else if (link.includes('#') && route.path === link.split('#')[0]) {
    if (route.path === '/map') {
      navigateTo(link)
      return
    }
    const hash = '#' + link.split('#')[1]
    setTimeout(() => {
      const el = document.querySelector(hash)
      if (el) {
        const headerOffset = 80
        const elementPosition = el.getBoundingClientRect().top
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset
        window.scrollTo({ top: offsetPosition, behavior: 'smooth' })
      }
    }, 150)
  } else {
    navigateTo(link)
  }
}

const handleKeyDown = (e) => {
  if (e.key === 'Escape' && isMenuOpen.value) {
    closeMenu()
  }
}

watch(isMenuOpen, (isOpen) => {
  if (import.meta.client) {
    if (isOpen) {
      document.documentElement.classList.add('is-scroll-locked')
      document.body.classList.add('is-scroll-locked')
      document.documentElement.style.overflow = 'hidden'
      document.body.style.overflow = 'hidden'
      window.addEventListener('keydown', handleKeyDown)
    } else {
      document.documentElement.classList.remove('is-scroll-locked')
      document.body.classList.remove('is-scroll-locked')
      document.documentElement.style.overflow = ''
      document.body.style.overflow = ''
      window.removeEventListener('keydown', handleKeyDown)
    }
  }
})

// При переходе на другую страницу автоматически закрываем меню и разблокируем скролл
watch(() => route.fullPath, () => {
  if (isMenuOpen.value) {
    closeMenu()
  }
})

onUnmounted(() => {
  if (import.meta.client) {
    document.documentElement.classList.remove('is-scroll-locked')
    document.body.classList.remove('is-scroll-locked')
    document.documentElement.style.overflow = ''
    document.body.style.overflow = ''
    window.removeEventListener('keydown', handleKeyDown)
  }
})
</script>

<style scoped>
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: var(--header-height);
  z-index: var(--z-header);
  border-bottom: var(--border-width) solid var(--color-header-border);
  color: var(--color-dark);
  transition: background-color var(--anim-duration-normal) ease, backdrop-filter var(--anim-duration-normal) ease, border-color var(--anim-duration-normal) ease;
  display: flex;
  align-items: center;
}

.app-header .app-header__burger-line {
  background-color: var(--color-dark);
}

.app-header__container {
  width: 100%;
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: 0 var(--space-40);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.app-header__logo {
  font-size: var(--text-body-lg);
  letter-spacing: var(--letter-spacing-uppercase);
  text-transform: uppercase;
  font-weight: var(--font-weight-regular);
  z-index: var(--z-header-content); /* Поверх оверлея */
  position: relative;
  transition: opacity var(--anim-duration-fast) ease;
}

.app-header.is-menu-open .app-header__logo {
  @media (max-width: 1024px) {
    opacity: 0;
    pointer-events: none;
  }
}

.app-header.is-menu-open .app-header__phone {
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
}

.app-header__spacer {
  flex: 1;
}

.app-header__actions {
  display: flex;
  align-items: center;
  gap: var(--space-48);
  z-index: var(--z-header-content); /* Поверх оверлея */
  position: relative;
}

.app-header__phone {
  display: flex;
  align-items: center;
  gap: var(--space-8);
  white-space: nowrap;
  flex-shrink: 0;
  font-size: var(--text-body-sm);
  letter-spacing: var(--letter-spacing-widest);
  opacity: 0.9;
  transition: opacity var(--anim-duration-fast) ease, visibility var(--anim-duration-fast) ease;
  text-decoration: none;
  color: inherit;
}

.app-header__phone-label {
  font-size: var(--text-micro);
  letter-spacing: var(--letter-spacing-uppercase);
  text-transform: uppercase;
  opacity: 0.5;
}

.app-header__phone:hover {
  opacity: 1;
}

.app-header__burger {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
  width: var(--space-32);
  height: var(--space-24);
  justify-content: center;
  align-items: flex-end;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  flex-shrink: 0;
}

.app-header__burger-line {
  display: block;
  width: 100%;
  height: var(--border-width);
  background-color: var(--color-white);
  transition: transform var(--anim-duration-fast) ease, width var(--anim-duration-fast) ease, opacity var(--anim-duration-fast) ease;
  transform-origin: center;
}

.app-header__burger-line:last-child {
  width: 60%;
}

.app-header__burger:hover .app-header__burger-line:last-child {
  width: 100%;
}

/* Анимация бургера в крестик */
.app-header__burger.is-active .app-header__burger-line:first-child {
  transform: translateY(var(--hamburger-offset)) rotate(45deg);
}

.app-header__burger.is-active .app-header__burger-line:last-child {
  width: 100%;
  transform: translateY(calc(var(--hamburger-offset) * -1)) rotate(-45deg);
}

/* Оверлей меню */
.app-menu__overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: var(--vw-100);
  height: var(--vh-100);
  background-color: var(--color-overlay);
  backdrop-filter: blur(var(--space-4));
  z-index: var(--z-overlay);
  touch-action: none;
  overscroll-behavior: contain;
}

/* Выезжающая панель */
.app-menu__panel {
  position: fixed;
  top: 0;
  right: 0;
  width: var(--menu-width);
  max-width: var(--vw-100);
  height: var(--vh-100);
  background-color: var(--color-white);
  z-index: var(--z-menu);
  padding: var(--space-120) var(--space-60) var(--space-60);
  display: flex;
  flex-direction: column;
  gap: var(--space-40);
  box-shadow: var(--shadow-menu);
  overflow-y: auto;
  overscroll-behavior: contain;
  -webkit-overflow-scrolling: touch;
}

.app-menu__section {
  display: flex;
  flex-direction: column;
  gap: var(--space-24);
}

.app-menu__subtitle {
  font-size: var(--text-caption);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-uppercase);
  color: var(--color-gray-300);
  border-bottom: var(--border-width) solid var(--color-gray-100);
  padding-bottom: var(--space-16);
}

.app-menu__nav {
  display: flex;
  flex-direction: column;
  gap: var(--space-16);
}

.app-menu__link {
  font-size: var(--text-subtitle);
  font-weight: var(--font-weight-light);
  color: var(--color-dark);
  text-decoration: none;
  transition: opacity var(--anim-duration-fast) ease, transform var(--anim-duration-fast) ease;
  transform-origin: left;
}

.app-menu__link:hover {
  opacity: 0.6;
  transform: translateX(var(--space-8));
}

.app-menu__link--global {
  font-size: var(--text-body-lg);
  color: var(--color-gray-600);
}

.app-menu__divider {
  height: var(--border-width);
  background-color: var(--color-gray-100);
  width: 100%;
}

/* Анимации Vue */
.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--anim-duration-normal) ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform var(--anim-duration-medium) var(--anim-easing-smooth);
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
}

@media (max-width: 768px) {
  .app-menu__panel {
    width: var(--vw-100);
    padding: var(--space-100) var(--space-32) var(--space-40);
  }
  
  .app-header__actions {
    gap: var(--space-24);
  }
  
  .app-header__phone {
    display: none; /* Прячем телефон на мобильных для чистоты */
  }
}
</style>
