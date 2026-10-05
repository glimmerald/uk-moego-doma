<template>
  <div class="news-page">
    <div class="news-page__container">
      
      <!-- Хлебные крошки -->
      <nav class="news-page__breadcrumb" aria-label="Хлебные крошки">
        <NuxtLink to="/" class="news-page__back-link">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>Главная</span>
        </NuxtLink>
        <span class="news-page__breadcrumb-sep" aria-hidden="true">/</span>
        <span class="news-page__breadcrumb-current">Пресс-центр</span>
      </nav>

      <!-- Шапка каталога новостей -->
      <header class="news-page__header">
        <div class="news-page__title-group">
          <span class="news-page__kicker">Журнал и пресс-центр</span>
          <h1 class="news-page__title">Новости компании</h1>
          <p class="news-page__subtitle">
            Официальные сообщения, статистика аварийно-диспетчерской службы, регламенты эксплуатации и события из жизни наших жилых комплексов.
          </p>
        </div>

        <div class="news-page__stats">
          <div class="news-page__stat-num">{{ allArticles.length }}</div>
          <div class="news-page__stat-label">публикаций в архиве</div>
        </div>
      </header>

      <!-- Фильтры по категориям (рубрикатор) -->
      <div class="news-filters" role="tablist" aria-label="Фильтрация новостей по рубрикам">
        <button
          v-for="cat in newsCategories"
          :key="cat.slug"
          class="news-filters__btn"
          :class="{ 'is-active': activeCategory === cat.slug }"
          role="tab"
          :aria-selected="activeCategory === cat.slug"
          @click="setCategory(cat.slug)"
        >
          <span>{{ cat.title }}</span>
          <span class="news-filters__badge">{{ getCategoryCount(cat.slug) }}</span>
        </button>
      </div>

      <!-- Главная новость в фокусе (Featured Story) -->
      <section v-if="featuredArticle && activeCategory === 'all'" class="news-featured" aria-label="Главный материал">
        <NuxtLink :to="`/news/${featuredArticle.slug}`" class="news-featured__card">
          <div class="news-featured__media">
            <img
              :src="featuredArticle.coverImage"
              :alt="featuredArticle.title"
              class="news-featured__img"
              loading="eager"
            />
            <span class="news-featured__tag">В фокусе</span>
          </div>

          <div class="news-featured__content">
            <div class="news-featured__meta">
              <span class="news-featured__category">{{ featuredArticle.category }}</span>
              <span class="news-featured__dot" aria-hidden="true">•</span>
              <time class="news-featured__date">{{ featuredArticle.displayDate }}</time>
              <span class="news-featured__dot" aria-hidden="true">•</span>
              <span class="news-featured__read-time">{{ featuredArticle.readTime }}</span>
            </div>

            <h2 class="news-featured__title">{{ featuredArticle.title }}</h2>
            <p class="news-featured__excerpt">{{ featuredArticle.excerpt }}</p>

            <div class="news-featured__footer">
              <span class="news-featured__btn">
                <span>Читать публикацию</span>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
            </div>
          </div>
        </NuxtLink>
      </section>

      <!-- Сетка публикаций (Editorial Grid) -->
      <section class="news-grid-section" aria-label="Список публикаций">
        <div v-if="displayedArticles.length > 0" class="news-grid">
          <article
            v-for="article in displayedArticles"
            :key="article.id"
            class="news-card"
          >
            <NuxtLink :to="`/news/${article.slug}`" class="news-card__link">
              <div class="news-card__media">
                <img
                  :src="article.coverImage"
                  :alt="article.title"
                  class="news-card__img"
                  loading="lazy"
                />
              </div>

              <div class="news-card__body">
                <div class="news-card__meta">
                  <span class="news-card__category">{{ article.category }}</span>
                  <span class="news-card__sep" aria-hidden="true">•</span>
                  <time class="news-card__date">{{ article.displayDate }}</time>
                </div>

                <h3 class="news-card__title">{{ article.title }}</h3>
                <p class="news-card__excerpt">{{ article.excerpt }}</p>

                <div class="news-card__footer">
                  <span class="news-card__read-time">{{ article.readTime }}</span>
                  <span class="news-card__arrow" aria-hidden="true">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                      <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </span>
                </div>
              </div>
            </NuxtLink>
          </article>
        </div>

        <!-- Состояние, когда в рубрике пусто -->
        <div v-else class="news-empty">
          <p class="news-empty__text">В выбранной рубрике пока нет опубликованных материалов.</p>
          <button class="news-empty__btn" @click="setCategory('all')">
            Смотреть все публикации
          </button>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { newsCategories, getAllNews } from '~/data/news'

// SEO Мета-теги
useHead({
  title: 'Пресс-центр и новости — УК МОЕГО ДОМА',
  meta: [
    {
      name: 'description',
      content: 'Новости, отчетность аварийно-диспетчерской службы, регламенты сезонных работ и события жилых комплексов Управляющей Компании.'
    },
    { property: 'og:title', content: 'Пресс-центр и новости — УК МОЕГО ДОМА' },
    { property: 'og:type', content: 'website' }
  ]
})

const route = useRoute()
const router = useRouter()

const allArticles = getAllNews()
const activeCategory = ref('all')

// Инициализация категории из URL Query (?category=...)
onMounted(() => {
  const queryCat = route.query.category
  if (queryCat && newsCategories.some(c => c.slug === queryCat)) {
    activeCategory.value = String(queryCat)
  }
})

// Реактивное отслеживание смены категории (например, при клике из меню)
watch(() => route.query.category, (newCat) => {
  if (newCat && newsCategories.some(c => c.slug === newCat)) {
    activeCategory.value = String(newCat)
  } else if (!newCat) {
    activeCategory.value = 'all'
  }
})

const setCategory = (slug) => {
  activeCategory.value = slug
  router.replace({
    query: slug === 'all' ? {} : { category: slug }
  })
}

// Количество публикаций в категории
const getCategoryCount = (slug) => {
  if (slug === 'all') return allArticles.length
  return allArticles.filter(item => item.categorySlug === slug).length
}

// Главная новость (Featured)
const featuredArticle = computed(() => {
  return allArticles.find(item => item.featured) || allArticles[0]
})

// Статьи для сетки (если выбрано 'all', исключаем главную из обычной сетки)
const displayedArticles = computed(() => {
  if (activeCategory.value === 'all') {
    return allArticles.filter(item => item.id !== featuredArticle.value?.id)
  }
  return allArticles.filter(item => item.categorySlug === activeCategory.value)
})
</script>

<style scoped>
.news-page {
  padding-top: calc(var(--header-height) + var(--space-40));
  padding-bottom: var(--space-120);
  background-color: var(--color-bg);
  min-height: var(--vh-100);
}

.news-page__container {
  max-width: var(--container-max-width);
  margin-inline: auto;
  padding-inline: var(--container-padding);
}

/* Хлебные крошки */
.news-page__breadcrumb {
  display: flex;
  align-items: center;
  gap: var(--space-8);
  font-size: var(--text-body-sm);
  color: var(--color-gray-400);
  margin-bottom: var(--space-32);
}

.news-page__back-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-6);
  color: var(--color-gray-600);
  transition: color var(--anim-duration-fast) var(--anim-easing-smooth);
}

.news-page__back-link:hover {
  color: var(--color-black);
}

.news-page__breadcrumb-sep {
  color: var(--color-gray-300);
}

.news-page__breadcrumb-current {
  color: var(--color-black);
  font-weight: var(--font-weight-medium);
}

/* Шапка каталога */
.news-page__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: var(--space-40);
  margin-bottom: var(--space-48);
  padding-bottom: var(--space-32);
  border-bottom: var(--border-width) solid var(--color-border);
}

.news-page__kicker {
  display: block;
  font-family: var(--font-family);
  font-size: var(--text-caption);
  font-weight: var(--font-weight-semibold);
  letter-spacing: var(--letter-spacing-uppercase);
  text-transform: uppercase;
  color: var(--color-gray-500);
  margin-bottom: var(--space-12);
}

.news-page__title {
  font-size: var(--text-h1);
  font-weight: var(--font-weight-light);
  line-height: var(--line-height-hero);
  letter-spacing: var(--letter-spacing-tight);
  text-transform: uppercase;
  color: var(--color-black);
  margin-bottom: var(--space-16);
}

.news-page__subtitle {
  font-size: var(--text-subtitle);
  font-weight: var(--font-weight-light);
  line-height: var(--line-height-relaxed);
  color: var(--color-gray-600);
  max-width: var(--max-width-text);
}

.news-page__stats {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: flex-end;
  flex-shrink: 0;
  gap: var(--space-8);
}

.news-page__stat-num {
  font-family: var(--font-family-serif);
  font-size: var(--text-hero);
  font-variant-numeric: lining-nums;
  -moz-font-feature-settings: "lnum" 1;
  -webkit-font-feature-settings: "lnum" 1;
  font-feature-settings: "lnum" 1;
  line-height: var(--line-height-hero);
  color: var(--color-black);
}

.news-page__stat-label {
  font-family: var(--font-family);
  font-size: var(--text-caption);
  color: var(--color-gray-500);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
  white-space: nowrap;
}

/* Рубрикатор / Фильтры */
.news-filters {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-10);
  margin-bottom: var(--space-48);
}

.news-filters__btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-8);
  padding: var(--space-10) var(--space-20);
  background-color: var(--color-bg-alt);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--editorial-badge-radius);
  font-family: var(--font-family);
  font-size: var(--text-body-sm);
  color: var(--color-gray-700);
  cursor: pointer;
  transition: all var(--anim-duration-fast) var(--anim-easing-smooth);
}

.news-filters__btn:hover {
  border-color: var(--color-gray-400);
  color: var(--color-black);
}

.news-filters__btn.is-active {
  background-color: var(--color-black);
  border-color: var(--color-black);
  color: var(--color-white);
}

.news-filters__badge {
  font-size: var(--text-tiny);
  font-weight: var(--font-weight-medium);
  padding: var(--space-2) var(--space-6);
  border-radius: var(--editorial-badge-radius);
  background-color: var(--color-badge-bg);
  color: inherit;
}

.news-filters__btn.is-active .news-filters__badge {
  background-color: var(--color-white-20);
}

/* Главная новость (Featured) */
.news-featured {
  margin-bottom: var(--space-64);
}

.news-featured__card {
  display: grid;
  grid-template-columns: var(--news-grid-left-col) 1fr;
  gap: var(--space-48);
  align-items: center;
  background-color: var(--color-bg-alt);
  border: var(--border-width) solid var(--color-border);
  padding: var(--space-32);
  transition: border-color var(--anim-duration-normal) var(--anim-easing-smooth);
}

.news-featured__card:hover {
  border-color: var(--color-gray-400);
}

.news-featured__media {
  position: relative;
  width: 100%;
  height: var(--editorial-featured-thumb-height);
  overflow: hidden;
  background-color: var(--color-gray-100);
}

.news-featured__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--anim-duration-slow) var(--anim-easing-smooth);
}

.news-featured__card:hover .news-featured__img {
  transform: scale(var(--scale-featured-hover));
}

.news-featured__tag {
  position: absolute;
  top: var(--space-16);
  left: var(--space-16);
  background: var(--color-tag-bg);
  backdrop-filter: blur(var(--space-10));
  color: var(--color-white);
  font-family: var(--font-family);
  font-size: var(--text-tiny);
  font-weight: var(--font-weight-semibold);
  letter-spacing: var(--letter-spacing-uppercase);
  text-transform: uppercase;
  padding: var(--space-4) var(--space-12);
  border-radius: var(--editorial-badge-radius);
}

.news-featured__content {
  display: flex;
  flex-direction: column;
}

.news-featured__meta {
  display: flex;
  align-items: center;
  gap: var(--space-8);
  font-family: var(--font-family);
  font-size: var(--text-caption);
  color: var(--color-gray-500);
  margin-bottom: var(--space-16);
}

.news-featured__category {
  font-weight: var(--font-weight-semibold);
  color: var(--color-dark);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
}

.news-featured__dot {
  color: var(--color-gray-300);
}

.news-featured__title {
  font-family: var(--font-family-serif);
  font-size: var(--text-h2);
  font-weight: var(--font-weight-regular);
  line-height: var(--line-height-heading);
  color: var(--color-black);
  margin-bottom: var(--space-16);
  letter-spacing: var(--letter-spacing-tight);
}

.news-featured__excerpt {
  font-family: var(--font-family);
  font-size: var(--text-body);
  font-weight: var(--font-weight-light);
  line-height: var(--line-height-loose);
  color: var(--color-gray-700);
  margin-bottom: var(--space-32);
}

.news-featured__footer {
  margin-top: auto;
}

.news-featured__btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-8);
  font-family: var(--font-family);
  font-size: var(--text-body-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-black);
  transition: gap var(--anim-duration-fast) var(--anim-easing-smooth);
}

.news-featured__card:hover .news-featured__btn {
  gap: var(--space-12);
}

/* Сетка карточек новостей (Editorial Smart Grid) */
.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(clamp(280px, calc(25vw + 40px), 380px), 1fr));
  gap: var(--space-32);
}

.news-card {
  display: flex;
  flex-direction: column;
  background-color: var(--color-bg);
  border: var(--border-width) solid var(--color-border);
  transition: border-color var(--anim-duration-fast) var(--anim-easing-smooth), transform var(--anim-duration-fast) var(--anim-easing-smooth);
}

.news-card:hover {
  border-color: var(--color-gray-400);
  transform: translateY(calc(var(--space-2) * -1));
}

.news-card__link {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.news-card__media {
  width: 100%;
  height: var(--editorial-card-thumb-height);
  overflow: hidden;
  background-color: var(--color-gray-100);
}

.news-card__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--anim-duration-medium) var(--anim-easing-smooth);
}

.news-card:hover .news-card__img {
  transform: scale(var(--scale-card-hover));
}

.news-card__body {
  padding: var(--space-24);
  display: flex;
  flex-direction: column;
  flex: 1;
}

.news-card__meta {
  display: flex;
  align-items: center;
  gap: var(--space-8);
  font-family: var(--font-family);
  font-size: var(--text-tiny);
  color: var(--color-gray-500);
  margin-bottom: var(--space-12);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
}

.news-card__category {
  font-weight: var(--font-weight-semibold);
  color: var(--color-dark);
}

.news-card__sep {
  color: var(--color-gray-300);
}

.news-card__title {
  font-family: var(--font-family-serif);
  font-size: var(--text-h4);
  font-weight: var(--font-weight-regular);
  line-height: var(--line-height-heading);
  color: var(--color-black);
  margin-bottom: var(--space-12);
}

.news-card__excerpt {
  font-family: var(--font-family);
  font-size: var(--text-body-sm);
  font-weight: var(--font-weight-light);
  line-height: var(--line-height-relaxed);
  color: var(--color-gray-600);
  margin-bottom: var(--space-24);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-card__footer {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--space-16);
  border-top: var(--border-width) solid var(--color-gray-100);
}

.news-card__read-time {
  font-family: var(--font-family);
  font-size: var(--text-tiny);
  color: var(--color-gray-500);
}

.news-card__arrow {
  color: var(--color-black);
  transition: transform var(--anim-duration-fast) var(--anim-easing-smooth);
}

.news-card:hover .news-card__arrow {
  transform: translateX(var(--space-4));
}

/* Пустое состояние */
.news-empty {
  text-align: center;
  padding-block: var(--space-80);
  background-color: var(--color-bg-alt);
  border: var(--border-width) solid var(--color-border);
}

.news-empty__text {
  font-size: var(--text-body);
  color: var(--color-gray-600);
  margin-bottom: var(--space-20);
}

.news-empty__btn {
  display: inline-block;
  padding: var(--space-12) var(--space-24);
  background-color: var(--color-black);
  color: var(--color-white);
  border-radius: var(--editorial-badge-radius);
  font-size: var(--text-body-sm);
  cursor: pointer;
}

/* Адаптивные перестроения сетки (только стандартизированные брейкпоинты 1024px, 768px, 480px) */
@media (max-width: 1024px) {
  .news-featured__card {
    grid-template-columns: 1fr;
    gap: var(--space-32);
    padding: var(--space-24);
  }
}

@media (max-width: 768px) {
  .news-page__header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-24);
  }

  .news-page__stats {
    align-items: flex-start;
  }
}

@media (max-width: 480px) {
  .news-filters {
    gap: var(--space-6);
  }
  
  .news-filters__btn {
    width: 100%;
    justify-content: space-between;
  }
}
</style>
