<template>
  <header :class="['app-header', 'glass-effect', { 'is-menu-open': isMenuOpen }]">
    <div class="app-header__container">
      <div class="app-header__logo">
        <NuxtLink to="/">УК МОЕГО ДОМА</NuxtLink>
      </div>
      
      <!-- Центральное меню убрано по ТЗ -->
      <div class="app-header__spacer"></div>

      <div class="app-header__actions">
        <a href="tel:+74950000000" class="app-header__phone">+7 (495) 000-00-00</a>
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
      <div class="app-menu__overlay" v-if="isMenuOpen" @click="closeMenu"></div>
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
  
  // Если ссылка ведет на якорь на главной странице (например, /#news)
  if (link.startsWith('/#') && route.path === '/') {
    const hash = link.replace('/', '')
    
    // Небольшая задержка, чтобы меню успело начать закрываться 
    // и разблокировался скролл (overflow: hidden убрался)
    setTimeout(() => {
      const el = document.querySelector(hash)
      if (el) {
        // Учитываем высоту хедера (около 80px)
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
    // Если это локальный якорь на другой странице (например, /documents#general и мы находимся на /documents)
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
    // Иначе это переход на другую страницу (или главную с другой страницы)
    navigateTo(link)
  }
}

// Блокируем скролл на body при открытом меню
watch(isMenuOpen, (isOpen) => {
  if (import.meta.client) { // Проверка, что код выполняется в браузере (на клиенте)
    if (isOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
  }
})
</script>

<style scoped>
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: var(--z-header);
  padding: var(--space-24) 0;
  border-bottom: var(--border-width) solid var(--color-header-border);
  color: var(--color-dark);
  transition: background-color var(--anim-duration-normal) ease, backdrop-filter var(--anim-duration-normal) ease, border-color var(--anim-duration-normal) ease;
}

.app-header .app-header__burger-line {
  background-color: var(--color-dark);
}

.app-header__container {
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
  font-size: var(--text-body-sm);
  letter-spacing: var(--letter-spacing-widest);
  opacity: 0.9;
  transition: opacity var(--anim-duration-fast) ease;
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
}

.app-header__burger-line {
  display: block;
  width: 100%;
  height: var(--border-width);
  background-color: #fff;
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
  transform: translateY(3.5px) rotate(45deg);
}

.app-header__burger.is-active .app-header__burger-line:last-child {
  width: 100%;
  transform: translateY(-3.5px) rotate(-45deg);
}

/* Оверлей меню */
.app-menu__overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: var(--color-overlay);
  backdrop-filter: blur(var(--space-4));
  z-index: var(--z-overlay);
}

/* Выезжающая панель */
.app-menu__panel {
  position: fixed;
  top: 0;
  right: 0;
  width: 480px;
  max-width: 100vw;
  height: 100vh;
  background-color: #fff;
  z-index: var(--z-menu);
  padding: var(--space-120) var(--space-60) var(--space-60);
  display: flex;
  flex-direction: column;
  gap: var(--space-40);
  box-shadow: var(--shadow-menu);
  overflow-y: auto;
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
    width: 100vw;
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
