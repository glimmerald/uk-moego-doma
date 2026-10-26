<template>
  <div class="article-page about-page">
    
    <!-- Индикатор прогресса чтения -->
    <div class="reading-progress-track" aria-hidden="true">
      <div class="reading-progress-bar" :style="{ width: `${readingProgress}%` }"></div>
    </div>

    <div class="article-page__container">
      
      <!-- Хлебные крошки и возврат на главную -->
      <nav class="article-page__nav" aria-label="Хлебные крошки">
        <NuxtLink to="/" class="article-page__back-link">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>Главная</span>
        </NuxtLink>
        <span class="article-page__nav-sep" aria-hidden="true">/</span>
        <span class="article-page__nav-current">О компании</span>
      </nav>

      <!-- Шапка страницы (Editorial Header) -->
      <header class="article-header">
        <div class="article-header__meta">
          <span class="article-header__category">{{ aboutData.header.kicker }}</span>
        </div>

        <h1 class="article-header__title">{{ aboutData.header.title }}</h1>

        <p class="article-header__subtitle">
          {{ aboutData.header.subtitle }}
        </p>
      </header>

      <!-- Заглавная фотография страницы (Hero Cover) -->
      <figure class="article-cover">
        <div class="article-cover__media">
          <img
            :src="aboutData.coverImage.src"
            :alt="aboutData.coverImage.alt"
            class="article-cover__img"
            loading="eager"
          />
        </div>
        <figcaption v-if="aboutData.coverImage.caption" class="editorial-caption">
          {{ aboutData.coverImage.caption }}
        </figcaption>
      </figure>

      <!-- Журнальное тело страницы (Editorial Longread) -->
      <main class="editorial-article">
        
        <!-- Секция: Миссия и принципы -->
        <section id="principles" class="about-section" aria-labelledby="heading-principles">
          <p class="editorial-lead">
            {{ aboutData.manifest.lead }}
          </p>

          <p class="editorial-p">
            {{ aboutData.manifest.paragraph }}
          </p>

          <h2 id="heading-principles" class="editorial-h2">
            {{ aboutData.manifest.principlesHeading }}
          </h2>

          <div class="editorial-principles">
            <article
              v-for="principle in aboutData.manifest.principles"
              :key="principle.id"
              class="editorial-principle-item"
            >
              <span class="editorial-principle-num" aria-hidden="true">{{ principle.number }}</span>
              <div class="editorial-principle-content">
                <h3 class="editorial-principle-title">{{ principle.title }}</h3>
                <p class="editorial-principle-desc">{{ principle.description }}</p>
              </div>
            </article>
          </div>

          <!-- Выносная цитата -->
          <blockquote class="editorial-quote">
            <p class="editorial-quote__text">
              «{{ aboutData.manifest.conclusionQuote.text }}»
            </p>
            <cite class="editorial-quote__author">
              {{ aboutData.manifest.conclusionQuote.author }}
            </cite>
          </blockquote>
        </section>

        <!-- Внутренний медиаблок: фотографии меньшего формата (диптих) -->
        <section
          v-if="aboutData.inlineGallery && aboutData.inlineGallery.images?.length"
          class="about-gallery"
          aria-label="Фотографии объектов и сервиса"
        >
          <div v-if="aboutData.inlineGallery.heading" class="about-gallery__header">
            <h3 class="editorial-h3">{{ aboutData.inlineGallery.heading }}</h3>
            <p v-if="aboutData.inlineGallery.description" class="about-gallery__desc">
              {{ aboutData.inlineGallery.description }}
            </p>
          </div>

          <div class="editorial-figure-grid">
            <figure
              v-for="(img, idx) in aboutData.inlineGallery.images"
              :key="idx"
              class="editorial-figure"
            >
              <div class="editorial-figure__media">
                <img
                  :src="img.src"
                  :alt="img.alt"
                  class="editorial-figure__img"
                  loading="lazy"
                />
              </div>
              <figcaption v-if="img.caption" class="editorial-caption">
                {{ img.caption }}
              </figcaption>
            </figure>
          </div>
        </section>

        <!-- Секция: Организационная структура -->
        <section id="departments" class="about-section about-section--structure" aria-labelledby="heading-departments">
          <h2 id="heading-departments" class="editorial-h2">
            {{ aboutData.structure.heading }}
          </h2>

          <p class="editorial-p">
            {{ aboutData.structure.lead }}
          </p>

          <div class="editorial-depts">
            <div
              v-for="group in aboutData.structure.groups"
              :key="group.id"
              class="editorial-depts-group"
            >
              <h3 class="editorial-depts-group__title">
                {{ group.category }}
              </h3>

              <div class="editorial-depts-grid">
                <div
                  v-for="dept in group.departments"
                  :key="dept.id"
                  class="editorial-dept-card"
                >
                  <div class="editorial-dept-card__header">
                    <h4 class="editorial-dept-card__title">{{ dept.name }}</h4>
                    <span v-if="dept.badge" class="editorial-dept-card__badge">
                      {{ dept.badge }}
                    </span>
                  </div>
                  <p class="editorial-dept-card__desc">
                    {{ dept.description }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

      </main>

      <!-- Подвал материала: Поделиться -->
      <footer class="article-footer">
        <div class="article-share">
          <span class="article-share__label">Поделиться информацией:</span>
          
          <div class="article-share__actions">
            <button
              class="article-share__btn"
              @click="copyPageLink"
              aria-label="Скопировать ссылку на страницу"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>{{ isCopied ? 'Ссылка скопирована' : 'Скопировать ссылку' }}</span>
            </button>

            <a
              :href="`https://t.me/share/url?url=${encodeURIComponent(currentUrl)}&text=${encodeURIComponent(aboutData.header.title)}`"
              target="_blank"
              rel="noopener noreferrer"
              class="article-share__btn article-share__btn--telegram"
              aria-label="Поделиться в Telegram"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 0 0-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.75-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .37z"/>
              </svg>
              <span>Telegram</span>
            </a>
          </div>
        </div>
      </footer>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { aboutData } from '~/data/about'

// SEO метаданные
useSeoMeta({
  title: aboutData.seo.title,
  description: aboutData.seo.description,
  ogTitle: aboutData.seo.title,
  ogDescription: aboutData.seo.description,
  ogImage: aboutData.coverImage.src,
  ogType: 'website'
})

// Индикатор скролла и прогресса чтения
const readingProgress = ref(0)
const updateProgress = () => {
  if (typeof window === 'undefined') return
  const scrollTop = window.scrollY
  const docHeight = document.documentElement.scrollHeight - window.innerHeight
  if (docHeight <= 0) {
    readingProgress.value = 0
    return
  }
  const pct = Math.min(100, Math.max(0, (scrollTop / docHeight) * 100))
  readingProgress.value = Math.round(pct)
}

// Поделиться ссылкой
const isCopied = ref(false)
const currentUrl = ref('')

const copyPageLink = async () => {
  if (typeof window === 'undefined') return
  try {
    await navigator.clipboard.writeText(window.location.href)
    isCopied.value = true
    setTimeout(() => {
      isCopied.value = false
    }, 2500)
  } catch (err) {
    console.error('Ошибка копирования ссылки:', err)
  }
}

onMounted(() => {
  if (typeof window !== 'undefined') {
    currentUrl.value = window.location.href
    window.addEventListener('scroll', updateProgress, { passive: true })
    updateProgress()
  }
})

onUnmounted(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('scroll', updateProgress)
  }
})
</script>

<style scoped>
.article-page {
  padding-top: calc(var(--header-height) + var(--space-40));
  padding-bottom: var(--space-120);
  background-color: var(--color-bg);
  min-height: var(--vh-100);
}

.article-page__container {
  max-width: var(--container-max-width);
  margin-inline: auto;
  padding-inline: var(--container-padding);
}

/* Навигация и крошки */
.article-page__nav {
  display: flex;
  align-items: center;
  gap: var(--space-8);
  font-size: var(--text-body-sm);
  color: var(--color-gray-400);
  margin-bottom: var(--space-32);
}

.article-page__back-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-6);
  color: var(--color-gray-600);
  transition: color var(--anim-duration-fast) var(--anim-easing-smooth);
}

.article-page__back-link:hover {
  color: var(--color-black);
}

.article-page__nav-sep {
  color: var(--color-gray-300);
}

.article-page__nav-current {
  color: var(--color-black);
  font-weight: var(--font-weight-medium);
}

/* Шапка страницы */
.article-header {
  max-width: var(--reading-measure);
  margin-inline: auto;
  margin-bottom: var(--space-40);
  text-align: left;
}

.article-header__meta {
  display: flex;
  align-items: center;
  gap: var(--space-8);
  font-family: var(--font-family);
  font-size: var(--editorial-meta-size);
  color: var(--color-gray-500);
  margin-bottom: var(--space-20);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
}

.article-header__category {
  font-weight: var(--font-weight-semibold);
  color: var(--color-dark);
}

.article-header__title {
  font-family: var(--font-family-serif);
  font-size: var(--text-h1);
  font-weight: var(--font-weight-regular);
  line-height: var(--line-height-heading);
  letter-spacing: var(--letter-spacing-tight);
  color: var(--color-black);
  margin-bottom: var(--space-16);
}

.article-header__subtitle {
  font-family: var(--font-family);
  font-size: var(--text-subtitle);
  font-weight: var(--font-weight-light);
  line-height: var(--line-height-relaxed);
  color: var(--color-gray-700);
  margin-bottom: var(--space-0);
}

/* Обложка (Hero Cover) с защитой кинематографических пропорций */
.article-cover {
  max-width: var(--reading-measure-wide);
  margin-inline: auto;
  margin-bottom: var(--space-56);
}

.article-cover__media {
  width: 100%;
  aspect-ratio: var(--editorial-hero-aspect-ratio);
  max-height: var(--editorial-hero-max-height);
  overflow: hidden;
  background-color: var(--color-gray-100);
  border: var(--border-width) solid var(--color-border);
}

.article-cover__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Секции лонгрида */
.about-section {
  margin-bottom: var(--space-64);
}

.about-section--structure {
  margin-top: var(--space-64);
}

/* Внутренняя галерея */
.about-gallery {
  margin-block: var(--space-64);
}

.about-gallery__header {
  margin-bottom: var(--space-20);
}

.about-gallery__desc {
  font-family: var(--font-family);
  font-size: var(--text-caption);
  color: var(--color-gray-500);
  line-height: var(--line-height-base);
  margin-top: var(--space-4);
}

/* Подвал статьи и шеринг */
.article-footer {
  max-width: var(--reading-measure);
  margin-inline: auto;
  margin-top: var(--space-64);
  padding-top: var(--space-32);
  border-top: var(--border-width) solid var(--color-border);
}

.article-share {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--space-16);
}

.article-share__label {
  font-family: var(--font-family);
  font-size: var(--text-body-sm);
  color: var(--color-gray-600);
  font-weight: var(--font-weight-medium);
}

.article-share__actions {
  display: flex;
  gap: var(--space-12);
}

.article-share__btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-8);
  padding: var(--space-8) var(--space-16);
  background-color: var(--color-bg-alt);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--editorial-badge-radius);
  font-family: var(--font-family);
  font-size: var(--text-caption);
  color: var(--color-dark);
  cursor: pointer;
  transition: all var(--anim-duration-fast) var(--anim-easing-smooth);
}

.article-share__btn:hover {
  background-color: var(--color-black);
  border-color: var(--color-black);
  color: var(--color-white);
}

.article-share__btn--telegram:hover {
  background-color: var(--color-telegram);
  border-color: var(--color-telegram);
  color: var(--color-white);
}

/* Адаптивные правила */
@media (max-width: 768px) {
  .article-share {
    flex-direction: column;
    align-items: flex-start;
  }

  .article-share__actions {
    width: 100%;
  }

  .article-share__btn {
    flex: 1;
    justify-content: center;
  }
}
</style>
