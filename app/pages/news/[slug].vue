<template>
  <div v-if="article" class="article-page">
    
    <!-- Индикатор прогресса чтения -->
    <div class="reading-progress-track" aria-hidden="true">
      <div class="reading-progress-bar" :style="{ width: `${readingProgress}%` }"></div>
    </div>

    <div class="article-page__container">
      
      <!-- Хлебные крошки и возврат -->
      <nav class="article-page__nav" aria-label="Хлебные крошки">
        <NuxtLink to="/news" class="article-page__back-link">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>Все публикации</span>
        </NuxtLink>
        <span class="article-page__nav-sep" aria-hidden="true">/</span>
        <span class="article-page__nav-current">{{ article.category }}</span>
      </nav>

      <!-- Шапка статьи (Editorial Header) -->
      <header class="article-header">
        <div class="article-header__meta">
          <span class="article-header__category">{{ article.category }}</span>
          <span class="article-header__dot" aria-hidden="true">•</span>
          <time class="article-header__date" :datetime="article.date">{{ article.displayDate }}</time>
          <span class="article-header__dot" aria-hidden="true">•</span>
          <span class="article-header__read-time">{{ article.readTime }}</span>
        </div>

        <h1 class="article-header__title">{{ article.title }}</h1>

        <div v-if="article.author" class="article-header__author">
          <span class="article-header__author-label">Источник:</span>
          <span class="article-header__author-name">{{ article.author }}</span>
        </div>
      </header>

      <!-- Обложка статьи (Hero Cover) с защитой пропорций -->
      <figure class="article-cover">
        <div class="article-cover__media">
          <img
            :src="article.coverImage"
            :alt="article.title"
            class="article-cover__img"
            loading="eager"
          />
        </div>
        <figcaption v-if="article.coverCaption" class="editorial-caption">
          {{ article.coverCaption }}
        </figcaption>
      </figure>

      <!-- Тело статьи (Editorial Article Body) -->
      <div class="editorial-article">
        <template v-for="(block, index) in article.blocks" :key="index">
          
          <!-- Вводный лид -->
          <p v-if="block.type === 'lead'" class="editorial-lead">
            {{ block.text }}
          </p>

          <!-- Параграф текста -->
          <p v-else-if="block.type === 'paragraph'" class="editorial-p">
            {{ block.text }}
          </p>

          <!-- Подзаголовок -->
          <h2 v-else-if="block.type === 'heading'" class="editorial-h2">
            {{ block.title }}
          </h2>

          <!-- Выносная цитата -->
          <blockquote v-else-if="block.type === 'quote'" class="editorial-quote">
            <p class="editorial-quote__text">{{ block.text }}</p>
            <cite v-if="block.author" class="editorial-quote__author">{{ block.author }}</cite>
          </blockquote>

          <!-- Карточки с ключевыми показателями (KPI) -->
          <div v-else-if="block.type === 'kpis' && block.kpis" class="editorial-kpi-grid">
            <div
              v-for="(kpi, kIdx) in block.kpis"
              :key="kIdx"
              class="editorial-kpi-card"
            >
              <div class="editorial-kpi-card__val">{{ kpi.value }}</div>
              <div class="editorial-kpi-card__label">{{ kpi.label }}</div>
              <div v-if="kpi.sub" class="editorial-kpi-card__sub">{{ kpi.sub }}</div>
            </div>
          </div>

          <!-- Сервисные врезки (Callout) -->
          <div
            v-else-if="block.type === 'callout' && block.callout"
            :class="['editorial-callout', `editorial-callout--${block.callout.type || 'info'}`]"
          >
            <span v-if="block.callout.badge" class="editorial-callout__badge">
              {{ block.callout.badge }}
            </span>
            <h3 v-if="block.callout.title" class="editorial-callout__title">
              {{ block.callout.title }}
            </h3>
            <p class="editorial-callout__text">{{ block.callout.text }}</p>
          </div>

          <!-- Списки -->
          <ul v-else-if="block.type === 'list' && block.items" class="editorial-list">
            <li
              v-for="(item, lIdx) in block.items"
              :key="lIdx"
              class="editorial-list__item"
            >
              {{ item }}
            </li>
          </ul>

          <!-- Внутренняя одиночная фотография лонгрида -->
          <figure v-else-if="block.type === 'image' && block.image" class="editorial-figure">
            <div class="editorial-figure__media">
              <img
                :src="block.image.src"
                :alt="block.image.alt || ''"
                class="editorial-figure__img"
                loading="lazy"
              />
            </div>
            <figcaption v-if="block.image.caption" class="editorial-caption">
              {{ block.image.caption }}
            </figcaption>
          </figure>

          <!-- Внутренняя галерея / диптих из нескольких фотографий -->
          <div v-else-if="block.type === 'gallery' && block.images" class="editorial-figure-grid">
            <figure
              v-for="(img, gIdx) in block.images"
              :key="gIdx"
              class="editorial-figure"
            >
              <div class="editorial-figure__media">
                <img
                  :src="img.src"
                  :alt="img.alt || ''"
                  class="editorial-figure__img"
                  loading="lazy"
                />
              </div>
              <figcaption v-if="img.caption" class="editorial-caption">
                {{ img.caption }}
              </figcaption>
            </figure>
          </div>

        </template>
      </div>

      <!-- Панель «Поделиться» и теги -->
      <footer class="article-footer">
        <div class="article-share">
          <span class="article-share__label">Поделиться материалом:</span>
          
          <div class="article-share__actions">
            <button
              class="article-share__btn"
              @click="copyArticleLink"
              aria-label="Скопировать ссылку на новость"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>{{ isCopied ? 'Ссылка скопирована' : 'Скопировать ссылку' }}</span>
            </button>

            <a
              :href="`https://t.me/share/url?url=${encodeURIComponent(currentUrl)}&text=${encodeURIComponent(article.title)}`"
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

      <!-- Блок «Читайте также» -->
      <section v-if="relatedArticles.length > 0" class="article-related" aria-label="Другие публикации">
        <div class="article-related__header">
          <span class="article-related__kicker">Рекомендуем к чтению</span>
          <h2 class="article-related__title">Другие публикации</h2>
        </div>

        <div class="article-related__grid">
          <article
            v-for="rel in relatedArticles"
            :key="rel.id"
            class="article-related__card"
          >
            <NuxtLink :to="`/news/${rel.slug}`" class="article-related__link">
              <div class="article-related__media">
                <img
                  :src="rel.coverImage"
                  :alt="rel.title"
                  class="article-related__img"
                  loading="lazy"
                />
              </div>

              <div class="article-related__body">
                <div class="article-related__meta">
                  <span class="article-related__category">{{ rel.category }}</span>
                  <span class="article-related__sep" aria-hidden="true">•</span>
                  <time class="article-related__date">{{ rel.displayDate }}</time>
                </div>

                <h3 class="article-related__card-title">{{ rel.title }}</h3>
                <span class="article-related__read-time">{{ rel.readTime }}</span>
              </div>
            </NuxtLink>
          </article>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { getNewsBySlug, getRelatedNews } from '~/data/news'

const route = useRoute()
const slug = String(route.params.slug)
const article = getNewsBySlug(slug)

if (!article) {
  throw createError({
    statusCode: 404,
    statusMessage: 'Публикация не найдена',
    fatal: true
  })
}

// SEO метаданные
useSeoMeta({
  title: article.title,
  description: article.excerpt,
  ogTitle: article.title,
  ogDescription: article.excerpt,
  ogImage: article.coverImage,
  ogType: 'article'
})

// Статьи по теме
const relatedArticles = computed(() => getRelatedNews(slug, 3))

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

const copyArticleLink = async () => {
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

/* Шапка статьи */
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

.article-header__dot {
  color: var(--color-gray-300);
}

.article-header__title {
  font-family: var(--font-family-serif);
  font-size: var(--text-h1);
  font-weight: var(--font-weight-regular);
  line-height: var(--line-height-heading);
  letter-spacing: var(--letter-spacing-tight);
  color: var(--color-black);
  margin-bottom: var(--space-24);
}

.article-header__author {
  display: flex;
  align-items: center;
  gap: var(--space-6);
  font-family: var(--font-family);
  font-size: var(--text-caption);
  color: var(--color-gray-500);
  padding-top: var(--space-16);
  border-top: var(--border-width) solid var(--color-border);
}

.article-header__author-label {
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
}

.article-header__author-name {
  color: var(--color-dark);
  font-weight: var(--font-weight-medium);
}

/* Обложка (Hero Cover) с защитой кинематографических пропорций (Rule 3) */
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

/* Блок «Читайте также» */
.article-related {
  margin-top: var(--space-100);
  padding-top: var(--space-64);
  border-top: var(--border-width) solid var(--color-border);
}

.article-related__header {
  margin-bottom: var(--space-40);
  text-align: left;
}

.article-related__kicker {
  display: block;
  font-family: var(--font-family);
  font-size: var(--text-tiny);
  font-weight: var(--font-weight-semibold);
  letter-spacing: var(--letter-spacing-uppercase);
  text-transform: uppercase;
  color: var(--color-gray-500);
  margin-bottom: var(--space-8);
}

.article-related__title {
  font-family: var(--font-family-serif);
  font-size: var(--text-h2);
  font-weight: var(--font-weight-regular);
  color: var(--color-black);
}

.article-related__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(clamp(260px, calc(25vw + 40px), 360px), 1fr));
  gap: var(--space-32);
}

.article-related__card {
  background-color: var(--color-bg);
  border: var(--border-width) solid var(--color-border);
  transition: border-color var(--anim-duration-fast) var(--anim-easing-smooth), transform var(--anim-duration-fast) var(--anim-easing-smooth);
}

.article-related__card:hover {
  border-color: var(--color-gray-400);
  transform: translateY(calc(var(--space-2) * -1));
}

.article-related__link {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.article-related__media {
  width: 100%;
  height: var(--editorial-card-thumb-height);
  overflow: hidden;
  background-color: var(--color-gray-100);
}

.article-related__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--anim-duration-medium) var(--anim-easing-smooth);
}

.article-related__card:hover .article-related__img {
  transform: scale(var(--scale-card-hover));
}

.article-related__body {
  padding: var(--space-20);
  display: flex;
  flex-direction: column;
  flex: 1;
}

.article-related__meta {
  display: flex;
  align-items: center;
  gap: var(--space-6);
  font-family: var(--font-family);
  font-size: var(--text-tiny);
  color: var(--color-gray-500);
  margin-bottom: var(--space-10);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
}

.article-related__category {
  font-weight: var(--font-weight-semibold);
  color: var(--color-dark);
}

.article-related__sep {
  color: var(--color-gray-300);
}

.article-related__card-title {
  font-family: var(--font-family-serif);
  font-size: var(--text-h5);
  font-weight: var(--font-weight-regular);
  line-height: var(--line-height-heading);
  color: var(--color-black);
  margin-bottom: var(--space-12);
}

.article-related__read-time {
  margin-top: auto;
  font-family: var(--font-family);
  font-size: var(--text-tiny);
  color: var(--color-gray-500);
  padding-top: var(--space-10);
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
