<template>
  <footer class="app-footer">
    <div class="app-footer__container">
      
      <!-- Колонка 1: Бренд и описание -->
      <div class="app-footer__col app-footer__col--brand">
        <NuxtLink to="/" class="app-footer__logo">УК ПРЕМИУМ</NuxtLink>
        <p class="app-footer__desc">
          Профессиональное управление недвижимостью класса комфорт и премиум.
        </p>
      </div>

      <!-- Колонка 2: Локальное меню -->
      <div class="app-footer__col app-footer__col--nav" v-if="localMenu">
        <h4 class="app-footer__title">{{ localMenu.title }}</h4>
        <nav class="app-footer__nav">
          <a 
            v-for="item in localMenu.items" 
            :key="item.link" 
            :href="item.link"
            class="app-footer__link"
            @click.prevent="handleNavClick(item.link)"
          >
            {{ item.title }}
          </a>
        </nav>
      </div>

      <!-- Колонка 3: Общие разделы -->
      <div class="app-footer__col app-footer__col--nav">
        <h4 class="app-footer__title">Разделы</h4>
        <nav class="app-footer__nav">
          <a 
            v-for="item in menuData.global" 
            :key="item.link" 
            :href="item.link"
            class="app-footer__link"
            @click.prevent="handleNavClick(item.link)"
          >
            {{ item.title }}
          </a>
        </nav>
      </div>

      <!-- Колонка 4: Контакты и соцсети -->
      <div class="app-footer__col app-footer__col--contacts">
        <h4 class="app-footer__title">Связь с нами</h4>
        <div class="app-footer__contact-info">
          <a href="tel:+74950000000" class="app-footer__phone">+7 (495) 000-00-00</a>
          <a href="mailto:info@ukpremium.ru" class="app-footer__email">info@ukpremium.ru</a>
        </div>
        
        <div class="app-footer__socials">
          <a href="#" class="app-footer__social-link" target="_blank" aria-label="Telegram">
            Telegram
          </a>
          <a href="#" class="app-footer__social-link" target="_blank" aria-label="VK">
            ВКонтакте
          </a>
          <a href="#" class="app-footer__social-link" target="_blank" aria-label="YouTube">
            YouTube
          </a>
        </div>
      </div>

    </div>

    <!-- Подподвал (Sub-footer) -->
    <div class="app-footer__bottom">
      <div class="app-footer__bottom-container">
        <div class="app-footer__bottom-left">
          © {{ new Date().getFullYear() }} УК Премиум. Все права защищены.
        </div>
        <div class="app-footer__bottom-center">
          Created by <span class="app-footer__author">Yellow Tomato</span>
        </div>
        <div class="app-footer__bottom-right">
          <NuxtLink to="/privacy">Политика конфиденциальности</NuxtLink>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'nuxt/app'
import menuData from '@/assets/data/menu.json'

const route = useRoute()

const localMenu = computed(() => {
  return menuData.local[route.name] || null
})

// Та же логика плавного скролла, что и в шапке
const handleNavClick = (link) => {
  if (link.startsWith('/#') && route.path === '/') {
    const hash = link.replace('/', '')
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
  } else if (link.includes('#') && route.path === link.split('#')[0]) {
    const hash = '#' + link.split('#')[1]
    const el = document.querySelector(hash)
    if (el) {
      const headerOffset = 80
      const elementPosition = el.getBoundingClientRect().top
      const offsetPosition = elementPosition + window.pageYOffset - headerOffset
      window.scrollTo({ top: offsetPosition, behavior: 'smooth' })
    }
  } else {
    navigateTo(link)
  }
}
</script>

<style scoped>
.app-footer {
  background-color: var(--color-black);
  color: #fff;
  padding-top: var(--space-100);
  border-top: var(--border-width) solid var(--color-dark-border);
}

.app-footer__container {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: 0 var(--space-40);
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1.5fr;
  gap: var(--space-60);
}

.app-footer__col {
  display: flex;
  flex-direction: column;
}

.app-footer__logo {
  font-size: var(--text-subtitle);
  letter-spacing: var(--letter-spacing-uppercase);
  text-transform: uppercase;
  font-weight: var(--font-weight-regular);
  color: #fff;
  text-decoration: none;
  margin-bottom: var(--space-24);
}

.app-footer__desc {
  font-size: var(--text-small);
  line-height: var(--line-height-loose);
  color: var(--color-gray-400);
  max-width: 320px;
  margin-bottom: var(--space-40);
}

.app-footer__copy {
  font-size: var(--text-tiny);
  color: var(--color-gray-700);
  line-height: var(--line-height-relaxed);
  margin-top: auto;
}

.app-footer__title {
  font-size: var(--text-micro);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-uppercase);
  color: var(--color-gray-700);
  margin-bottom: var(--space-32);
}

.app-footer__nav {
  display: flex;
  flex-direction: column;
  gap: var(--space-16);
}

.app-footer__link {
  font-size: var(--text-body-sm);
  color: var(--color-gray-200);
  text-decoration: none;
  transition: color var(--anim-duration-fast) ease, transform var(--anim-duration-fast) ease;
  transform-origin: left;
}

.app-footer__link:hover {
  color: #fff;
  transform: translateX(var(--space-4));
}

.app-footer__contact-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-12);
  margin-bottom: var(--space-40);
}

.app-footer__phone {
  font-size: var(--text-subtitle);
  font-weight: var(--font-weight-light);
  color: #fff;
  text-decoration: none;
  transition: opacity var(--anim-duration-fast) ease;
}

.app-footer__email {
  font-size: var(--text-body-sm);
  color: var(--color-gray-200);
  text-decoration: none;
  transition: color var(--anim-duration-fast) ease;
}

.app-footer__phone:hover,
.app-footer__email:hover {
  opacity: 0.8;
  color: #fff;
}

.app-footer__socials {
  display: flex;
  flex-direction: column;
  gap: var(--space-12);
}

.app-footer__social-link {
  font-size: var(--text-small);
  color: var(--color-gray-400);
  text-decoration: none;
  transition: color var(--anim-duration-fast) ease;
}

.app-footer__social-link:hover {
  color: #fff;
}

/* Подподвал */
.app-footer__bottom {
  margin-top: var(--space-80);
  border-top: var(--border-width) solid var(--color-dark-border); /* Разделительная легкая линия */
  padding: var(--space-24) 0;
}

.app-footer__bottom-container {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: 0 var(--space-40);
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  font-size: var(--text-tiny);
  color: var(--color-gray-700);
  letter-spacing: var(--letter-spacing-wider);
}

.app-footer__bottom-left {
  text-align: left;
}

.app-footer__bottom-center {
  text-align: center;
}

.app-footer__author {
  color: #fff;
  font-weight: var(--font-weight-regular);
}

.app-footer__bottom-right {
  text-align: right;
}

.app-footer__bottom-right a {
  color: var(--color-gray-700);
  text-decoration: none;
  transition: color var(--anim-duration-fast) ease;
}

.app-footer__bottom-right a:hover {
  color: #fff;
}

@media (max-width: 1024px) {
  .app-footer__container {
    grid-template-columns: 1fr 1fr;
    row-gap: var(--space-80);
  }
}

@media (max-width: 768px) {
  .app-footer {
    padding-top: var(--space-60);
  }
  
  .app-footer__container {
    grid-template-columns: 1fr;
    gap: var(--space-60);
    padding: 0 var(--space-20);
  }
  
  .app-footer__desc {
    margin-bottom: var(--space-24);
  }

  .app-footer__bottom-container {
    grid-template-columns: 1fr;
    gap: var(--space-16);
    text-align: center;
  }

  .app-footer__bottom-left,
  .app-footer__bottom-center,
  .app-footer__bottom-right {
    text-align: center;
  }
}
</style>
