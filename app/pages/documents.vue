<template>
  <div class="documents-page">
    <div class="documents-page__container">
      
      <!-- Хлебные крошки / Навигация назад -->
      <nav class="documents-page__breadcrumb" aria-label="Хлебные крошки">
        <NuxtLink to="/" class="documents-page__back-link">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>Главная</span>
        </NuxtLink>
        <span class="documents-page__breadcrumb-sep" aria-hidden="true">/</span>
        <span class="documents-page__breadcrumb-current">Документы</span>
      </nav>

      <!-- Заголовок страницы (Hero) -->
      <header class="documents-page__header">
        <div class="documents-page__title-group">
          <h1 class="documents-page__title">Документы</h1>
          <p class="documents-page__subtitle">
            Официальные сведения, лицензии, отчетность и регламенты по объектам управления в строгом соответствии с федеральными стандартами раскрытия информации.
          </p>
        </div>

        <!-- Поисковая строка -->
        <div class="documents-search">
          <div class="documents-search__icon" aria-hidden="true">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <input
            v-model="searchQuery"
            type="text"
            class="documents-search__input"
            placeholder="Поиск по названию, номеру или категории документа..."
            aria-label="Поиск по документам"
          />
          <button
            v-if="searchQuery"
            class="documents-search__clear"
            @click="searchQuery = ''"
            aria-label="Очистить поиск"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </header>

      <!-- Якорные метки для прямой навигации из хедера/футера -->
      <div id="general" class="documents-anchor"></div>
      <div id="complexes" class="documents-anchor"></div>

      <!-- Главные вкладки (Вариант А) -->
      <div class="documents-tabs" role="tablist" aria-label="Категории документов">
        <button
          ref="generalTabRef"
          class="documents-tab"
          :class="{ 'is-active': activeTab === 'general' }"
          role="tab"
          :aria-selected="activeTab === 'general'"
          aria-controls="panel-general"
          :tabindex="activeTab === 'general' ? 0 : -1"
          @click="selectTab('general')"
          @keydown.right.prevent="selectTab('complexes', true)"
          @keydown.left.prevent="selectTab('complexes', true)"
        >
          <span class="documents-tab__name">Общие документы компании</span>
          <span class="documents-tab__count">{{ displayedGeneralCount }}</span>
        </button>

        <button
          ref="complexesTabRef"
          class="documents-tab"
          :class="{ 'is-active': activeTab === 'complexes' }"
          role="tab"
          :aria-selected="activeTab === 'complexes'"
          aria-controls="panel-complexes"
          :tabindex="activeTab === 'complexes' ? 0 : -1"
          @click="selectTab('complexes')"
          @keydown.left.prevent="selectTab('general', true)"
          @keydown.right.prevent="selectTab('general', true)"
        >
          <span class="documents-tab__name">Документы по объектам (ЖК)</span>
          <span class="documents-tab__count">{{ displayedComplexCount }}</span>
        </button>
      </div>

      <!-- Плавный переход между вкладками -->
      <Transition name="tab-fade" mode="out-in">
        <!-- ПАНЕЛЬ 1: ОБЩИЕ ДОКУМЕНТЫ -->
        <section
          v-if="activeTab === 'general'"
          id="panel-general"
          key="general"
          class="documents-panel"
          role="tabpanel"
          tabindex="0"
          aria-label="Общие документы компании"
        >
          <!-- Категории-чипсы общих документов -->
          <div class="documents-filter-bar">
            <div class="documents-chips" role="group" aria-label="Фильтр по категориям">
              <button
                v-for="cat in documentsData.generalCategories"
                :key="cat.id"
                class="documents-chip"
                :class="{ 'is-active': activeGeneralCategory === cat.id }"
                @click="activeGeneralCategory = cat.id"
              >
                <span>{{ cat.name }}</span>
                <span class="documents-chip__count">{{ getGeneralCategoryCount(cat.id) }}</span>
              </button>
            </div>
          </div>

          <!-- Список общих документов -->
          <div class="documents-list" v-if="filteredGeneralDocs.length > 0">
            <article
              v-for="doc in filteredGeneralDocs"
              :key="doc.id"
              class="document-item"
            >
              <div class="document-item__icon-wrapper" aria-hidden="true">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" class="document-item__icon">
                  <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M14 2V8H20" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M16 13H8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M16 17H8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M10 9H8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>

              <div class="document-item__main">
                <h2 class="document-item__title">{{ doc.title }}</h2>
                <div class="document-item__meta">
                  <span class="document-item__category">{{ doc.categoryName }}</span>
                  <span class="document-item__dot" aria-hidden="true">•</span>
                  <span class="document-item__date">Утвержден: {{ doc.date }}</span>
                  <span class="document-item__dot" aria-hidden="true">•</span>
                  <span class="document-item__badge">{{ doc.fileType }} · {{ doc.fileSize }}</span>
                </div>
              </div>

              <div class="document-item__actions">
                <a
                  :href="doc.url"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="document-action-btn"
                  title="Открыть для чтения"
                >
                  <span>Открыть</span>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M7 17L17 7M17 7H7M17 7V17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </a>
                <a
                  :href="doc.url"
                  :download="doc.title + '.' + doc.fileType.toLowerCase()"
                  class="document-action-btn document-action-btn--download"
                  title="Скачать файл"
                >
                  <span>Скачать</span>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M12 4V16M12 16L7 11M12 16L17 11M4 20H20" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </a>
              </div>
            </article>
          </div>

          <!-- Пустой результат -->
          <div v-else class="documents-empty">
            <div class="documents-empty__icon" aria-hidden="true">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
                <path d="M9 13H15M9 17H13M10 3H6C4.89543 3 4 3.89543 4 5V19C4 20.1046 4.89543 21 6 21H18C19.1046 21 20 20.1046 20 19V9L14 3H10Z" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h3 class="documents-empty__title">Документы не найдены</h3>
            <p class="documents-empty__text">
              {{ searchQuery ? `По вашему запросу «${searchQuery}» ничего не найдено в общих документах.` : 'В выбранной категории документов пока нет.' }}
            </p>
            <button class="documents-empty__reset" @click="resetFilters">Сбросить фильтры</button>
          </div>
        </section>

        <!-- ПАНЕЛЬ 2: ДОКУМЕНТЫ ПО ОБЪЕКТАМ (ЖК) -->
        <section
          v-else-if="activeTab === 'complexes'"
          id="panel-complexes"
          key="complexes"
          class="documents-panel"
          role="tabpanel"
          tabindex="0"
          aria-label="Документы по объектам (ЖК)"
        >
          <!-- Выбор города -->
          <div class="documents-cities-bar">
            <span class="documents-control-label">Регион / Город:</span>
            <div class="documents-city-tabs" role="group" aria-label="Выбор города">
              <button
                v-for="city in documentsData.cities"
                :key="city.id"
                class="documents-city-btn"
                :class="{ 'is-active': activeCityId === city.id }"
                @click="selectCity(city.id)"
              >
                <span>{{ city.name }}</span>
                <span class="documents-city-btn__count">{{ getCityComplexesCount(city.id) }}</span>
              </button>
            </div>
          </div>

          <!-- Выбор конкретного ЖК в выбранном городе -->
          <div class="documents-complexes-bar">
            <span class="documents-control-label">Жилой комплекс:</span>
            <div class="documents-complex-chips" role="group" aria-label="Выбор жилого комплекса">
              <button
                v-for="complex in availableComplexes"
                :key="complex.id"
                class="documents-complex-chip"
                :class="{ 'is-active': activeComplexId === complex.id }"
                @click="activeComplexId = complex.id"
              >
                <span class="documents-complex-chip__name">{{ complex.name }}</span>
              </button>
            </div>
          </div>

          <!-- Карточка активного ЖК -->
          <div v-if="currentComplex" class="complex-banner glass-effect">
            <div class="complex-banner__info">
              <div class="complex-banner__badge">Объект управления</div>
              <h2 class="complex-banner__title">{{ currentComplex.name }}</h2>
              <p class="complex-banner__address">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <path d="M12 13C13.6569 13 15 11.6569 15 10C15 8.34315 13.6569 7 12 7C10.3431 7 9 8.34315 9 10C9 11.6569 10.3431 13 12 13Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M12 21C16 17 20 13.4183 20 10C20 5.58172 16.4183 2 12 2C7.58172 2 4 5.58172 4 10C4 13.4183 8 17 12 21Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>{{ currentComplex.address }}</span>
              </p>
            </div>
            <div class="complex-banner__stat">
              <span class="complex-banner__stat-number">{{ currentComplex.documents.length }}</span>
              <span class="complex-banner__stat-label">Документов в архиве</span>
            </div>
          </div>

          <!-- Категории документов внутри ЖК -->
          <div class="documents-filter-bar">
            <div class="documents-chips" role="group" aria-label="Фильтр по категориям ЖК">
              <button
                v-for="cat in documentsData.complexCategories"
                :key="cat.id"
                class="documents-chip"
                :class="{ 'is-active': activeComplexCategory === cat.id }"
                @click="activeComplexCategory = cat.id"
              >
                <span>{{ cat.name }}</span>
                <span class="documents-chip__count">{{ getComplexCategoryCount(cat.id) }}</span>
              </button>
            </div>
          </div>

          <!-- Список документов ЖК -->
          <div class="documents-list" v-if="filteredComplexDocs.length > 0">
            <article
              v-for="doc in filteredComplexDocs"
              :key="doc.id"
              class="document-item"
            >
              <div class="document-item__icon-wrapper" aria-hidden="true">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" class="document-item__icon">
                  <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M14 2V8H20" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M16 13H8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M16 17H8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M10 9H8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>

              <div class="document-item__main">
                <h2 class="document-item__title">{{ doc.title }}</h2>
                <div class="document-item__meta">
                  <span class="document-item__category">{{ doc.categoryName }}</span>
                  <span class="document-item__dot" aria-hidden="true">•</span>
                  <span class="document-item__date">Дата: {{ doc.date }}</span>
                  <span class="document-item__dot" aria-hidden="true">•</span>
                  <span class="document-item__badge">{{ doc.fileType }} · {{ doc.fileSize }}</span>
                </div>
              </div>

              <div class="document-item__actions">
                <a
                  :href="doc.url"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="document-action-btn"
                  title="Открыть для чтения"
                >
                  <span>Открыть</span>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M7 17L17 7M17 7H7M17 7V17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </a>
                <a
                  :href="doc.url"
                  :download="doc.title + '.' + doc.fileType.toLowerCase()"
                  class="document-action-btn document-action-btn--download"
                  title="Скачать файл"
                >
                  <span>Скачать</span>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M12 4V16M12 16L7 11M12 16L17 11M4 20H20" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </a>
              </div>
            </article>
          </div>

          <!-- Пустой результат -->
          <div v-else class="documents-empty">
            <div class="documents-empty__icon" aria-hidden="true">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
                <path d="M9 13H15M9 17H13M10 3H6C4.89543 3 4 3.89543 4 5V19C4 20.1046 4.89543 21 6 21H18C19.1046 21 20 20.1046 20 19V9L14 3H10Z" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h3 class="documents-empty__title">Документы не найдены</h3>
            <p class="documents-empty__text">
              {{ searchQuery ? `По вашему запросу «${searchQuery}» в выбранном жилом комплексе ничего не найдено.` : 'В выбранной категории документов пока нет.' }}
            </p>
            <button class="documents-empty__reset" @click="resetFilters">Сбросить фильтры</button>
          </div>
        </section>
      </Transition>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute } from 'nuxt/app'
import documentsData from '@/assets/data/documents.json'

// Ссылки на элементы табов для клавиатурной навигации
const generalTabRef = ref(null)
const complexesTabRef = ref(null)

// SEO метаданные
useHead({
  title: 'Документы и отчетность — УК МОЕГО ДОМА',
  meta: [
    {
      name: 'description',
      content: 'Официальные документы компании, лицензии на управление МКД, тарифы, протоколы общих собраний и отчетность по объектам управления.'
    }
  ]
})

const route = useRoute()

// Активная главная вкладка: 'general' | 'complexes' (с учетом hash на старте)
const activeTab = ref(route.hash === '#complexes' ? 'complexes' : 'general')

// Поисковая строка
const searchQuery = ref('')

// Фильтр общих категорий
const activeGeneralCategory = ref('all')

// Фильтр городов и ЖК
const activeCityId = ref(documentsData.cities[0]?.id || 'krasnodar')
const availableComplexes = computed(() => {
  return documentsData.complexes.filter(c => c.cityId === activeCityId.value)
})

const activeComplexId = ref(availableComplexes.value[0]?.id || '')

// Фильтр категорий документов ЖК
const activeComplexCategory = ref('all')

// При смене города переключаем активный ЖК на первый доступный
const selectCity = (cityId) => {
  activeCityId.value = cityId
  const firstComplex = documentsData.complexes.find(c => c.cityId === cityId)
  if (firstComplex) {
    activeComplexId.value = firstComplex.id
  }
}

// Текущий выбранный ЖК
const currentComplex = computed(() => {
  return documentsData.complexes.find(c => c.id === activeComplexId.value) || availableComplexes.value[0] || null
})

// Базовый подсчет количества документов
const generalDocsCount = computed(() => documentsData.general.length)

const complexDocsTotalCount = computed(() => {
  return documentsData.complexes.reduce((total, comp) => total + comp.documents.length, 0)
})

// Подсчет при активном поиске
const displayedGeneralCount = computed(() => {
  if (!searchQuery.value.trim()) return generalDocsCount.value
  return filteredGeneralDocs.value.length
})

const displayedComplexCount = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()
  if (!query) return complexDocsTotalCount.value
  return documentsData.complexes.reduce((total, comp) => {
    const matches = comp.documents.filter(doc => 
      doc.title.toLowerCase().includes(query) ||
      doc.categoryName.toLowerCase().includes(query) ||
      doc.date.toLowerCase().includes(query)
    )
    return total + matches.length
  }, 0)
})

const getCityComplexesCount = (cityId) => {
  return documentsData.complexes.filter(c => c.cityId === cityId).length
}

const getGeneralCategoryCount = (categoryId) => {
  if (categoryId === 'all') return documentsData.general.length
  return documentsData.general.filter(d => d.category === categoryId).length
}

const getComplexCategoryCount = (categoryId) => {
  if (!currentComplex.value) return 0
  if (categoryId === 'all') return currentComplex.value.documents.length
  return currentComplex.value.documents.filter(d => d.category === categoryId).length
}

// Фильтрация общих документов с учетом поиска и категории
const filteredGeneralDocs = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()
  return documentsData.general.filter(doc => {
    const matchesCategory = activeGeneralCategory.value === 'all' || doc.category === activeGeneralCategory.value
    if (!matchesCategory) return false

    if (!query) return true
    return (
      doc.title.toLowerCase().includes(query) ||
      doc.categoryName.toLowerCase().includes(query) ||
      doc.date.toLowerCase().includes(query)
    )
  })
})

// Фильтрация документов ЖК с учетом поиска и категории
const filteredComplexDocs = computed(() => {
  if (!currentComplex.value) return []
  const query = searchQuery.value.trim().toLowerCase()

  return currentComplex.value.documents.filter(doc => {
    const matchesCategory = activeComplexCategory.value === 'all' || doc.category === activeComplexCategory.value
    if (!matchesCategory) return false

    if (!query) return true
    return (
      doc.title.toLowerCase().includes(query) ||
      doc.categoryName.toLowerCase().includes(query) ||
      doc.date.toLowerCase().includes(query)
    )
  })
})

// Переключение таба с обновлением хэша в URL и переносом фокуса
const selectTab = (tab, shouldFocus = false) => {
  activeTab.value = tab
  if (typeof window !== 'undefined') {
    const hash = '#' + tab
    if (window.location.hash !== hash) {
      window.history.replaceState(null, '', hash)
    }
  }
  if (shouldFocus) {
    nextTick(() => {
      if (tab === 'general') {
        generalTabRef.value?.focus()
      } else {
        complexesTabRef.value?.focus()
      }
    })
  }
}

// Сброс фильтров поиска
const resetFilters = () => {
  searchQuery.value = ''
  activeGeneralCategory.value = 'all'
  activeComplexCategory.value = 'all'
}

// Синхронизация таба с URL хэшем (#general / #complexes)
const syncTabWithHash = () => {
  if (typeof window === 'undefined') return
  const hash = window.location.hash
  if (hash === '#complexes') {
    activeTab.value = 'complexes'
  } else if (hash === '#general') {
    activeTab.value = 'general'
  }
}

watch(() => route.hash, () => {
  syncTabWithHash()
})

onMounted(() => {
  syncTabWithHash()
  window.addEventListener('hashchange', syncTabWithHash)
})

onUnmounted(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('hashchange', syncTabWithHash)
  }
})
</script>

<style scoped>
.documents-page {
  padding-top: calc(var(--header-height) + var(--space-40));
  padding-bottom: var(--space-120);
  background-color: var(--color-bg);
  min-height: var(--vh-100);
}

.documents-page__container {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: 0 var(--container-padding);
}

/* Скрытые якорные метки для точного скролла */
.documents-anchor {
  position: relative;
  top: calc(var(--header-height) * -1);
  visibility: hidden;
  height: 0;
  margin: 0;
  padding: 0;
}

/* Хлебные крошки */
.documents-page__breadcrumb {
  display: flex;
  align-items: center;
  gap: var(--space-8);
  font-size: var(--text-body-sm);
  color: var(--color-gray-400);
  margin-bottom: var(--space-32);
}

.documents-page__back-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-6);
  color: var(--color-gray-600);
  transition: color var(--anim-duration-fast) var(--anim-easing-smooth);
}

.documents-page__back-link:hover {
  color: var(--color-black);
}

.documents-page__breadcrumb-sep {
  color: var(--color-gray-300);
}

.documents-page__breadcrumb-current {
  color: var(--color-black);
  font-weight: var(--font-weight-medium);
}

/* Hero Header страницы */
.documents-page__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: var(--space-40);
  margin-bottom: var(--space-64);
  padding-bottom: var(--space-40);
  border-bottom: var(--border-width) solid var(--color-border);
}

.documents-page__title-group {
  flex: 1;
  max-width: var(--documents-header-max-width);
}

.documents-page__title {
  font-size: var(--text-h1);
  font-weight: var(--font-weight-light);
  line-height: var(--line-height-hero);
  letter-spacing: var(--letter-spacing-tight);
  text-transform: uppercase;
  margin-bottom: var(--space-16);
  color: var(--color-black);
}

.documents-page__subtitle {
  font-size: var(--text-body);
  line-height: var(--line-height-relaxed);
  color: var(--color-gray-600);
  max-width: var(--max-width-text);
}

/* Поисковая строка */
.documents-search {
  flex: 0 0 var(--documents-search-width);
  position: relative;
  display: flex;
  align-items: center;
}

.documents-search__icon {
  position: absolute;
  left: var(--space-16);
  color: var(--color-gray-400);
  pointer-events: none;
  display: flex;
  align-items: center;
  justify-content: center;
}

.documents-search__input {
  width: 100%;
  height: var(--documents-input-height);
  padding: 0 var(--space-48) 0 var(--space-48);
  font-family: inherit;
  font-size: var(--text-body-sm);
  color: var(--color-black);
  background-color: var(--color-bg-light);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--radius-sm);
  outline: none;
  transition: border-color var(--anim-duration-fast) var(--anim-easing-smooth), background-color var(--anim-duration-fast) var(--anim-easing-smooth);
}

.documents-search__input:focus {
  border-color: var(--color-black);
  background-color: var(--color-white);
}

.documents-search__input::placeholder {
  color: var(--color-gray-400);
}

.documents-search__clear {
  position: absolute;
  right: var(--space-12);
  width: var(--space-32);
  height: var(--space-32);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-gray-500);
  border-radius: var(--radius-round);
  transition: color var(--anim-duration-fast) var(--anim-easing-smooth), background-color var(--anim-duration-fast) var(--anim-easing-smooth);
}

.documents-search__clear:hover {
  color: var(--color-black);
  background-color: var(--color-gray-200);
}

/* Главные вкладки */
.documents-tabs {
  display: flex;
  gap: var(--space-12);
  margin-bottom: var(--space-40);
  border-bottom: var(--border-width) solid var(--color-border);
  padding-bottom: var(--space-16);
}

.documents-tab {
  display: inline-flex;
  align-items: center;
  gap: var(--space-12);
  padding: var(--space-12) var(--space-24);
  border-radius: var(--radius-pill);
  font-size: var(--text-body-lg);
  font-weight: var(--font-weight-regular);
  color: var(--color-gray-500);
  background-color: transparent;
  border: var(--border-width) solid transparent;
  transition: all var(--anim-duration-fast) var(--anim-easing-smooth);
}

.documents-tab:hover {
  color: var(--color-black);
  background-color: var(--color-bg-light);
}

.documents-tab.is-active {
  color: var(--color-white);
  background-color: var(--color-black);
  border-color: var(--color-black);
}

.documents-tab__count {
  font-size: var(--text-tiny);
  font-weight: var(--font-weight-semibold);
  padding: var(--space-2) var(--space-8);
  border-radius: var(--radius-pill);
  background-color: var(--color-gray-100);
  color: var(--color-gray-700);
  transition: all var(--anim-duration-fast) var(--anim-easing-smooth);
}

.documents-tab.is-active .documents-tab__count {
  background-color: var(--color-white-20);
  color: var(--color-white);
}

/* Плавный переход между вкладками */
.tab-fade-enter-active,
.tab-fade-leave-active {
  transition: opacity var(--anim-duration-fast) var(--anim-easing-smooth), transform var(--anim-duration-fast) var(--anim-easing-smooth);
}

.tab-fade-enter-from {
  opacity: 0;
  transform: translateY(var(--space-8));
}

.tab-fade-leave-to {
  opacity: 0;
  transform: translateY(calc(var(--space-8) * -1));
}

/* Фильтры и панели */
.documents-panel {
  display: flex;
  flex-direction: column;
  outline: none;
}

.documents-filter-bar {
  margin-bottom: var(--space-32);
}

.documents-chips {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-8);
}

.documents-chip {
  display: inline-flex;
  align-items: center;
  gap: var(--space-8);
  padding: var(--space-8) var(--space-16);
  font-size: var(--text-small);
  color: var(--color-gray-600);
  background-color: var(--color-bg-light);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--radius-pill);
  transition: all var(--anim-duration-fast) var(--anim-easing-smooth);
}

.documents-chip:hover {
  color: var(--color-black);
  border-color: var(--color-gray-400);
}

.documents-chip.is-active {
  color: var(--color-black);
  background-color: var(--color-white);
  border-color: var(--color-black);
  font-weight: var(--font-weight-medium);
  box-shadow: var(--shadow-sm);
}

.documents-chip__count {
  font-size: var(--text-micro);
  color: var(--color-gray-400);
}

.documents-chip.is-active .documents-chip__count {
  color: var(--color-black);
}

/* Выбор города и ЖК для Панели 2 */
.documents-cities-bar,
.documents-complexes-bar {
  display: flex;
  align-items: center;
  gap: var(--space-20);
  margin-bottom: var(--space-24);
}

.documents-control-label {
  font-size: var(--text-caption);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-gray-400);
  min-width: var(--documents-label-min-width);
}

.documents-city-tabs,
.documents-complex-chips {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-8);
}

.documents-city-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-8);
  padding: var(--space-8) var(--space-20);
  font-size: var(--text-body-sm);
  color: var(--color-gray-600);
  background-color: var(--color-bg-light);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--radius-sm);
  transition: all var(--anim-duration-fast) var(--anim-easing-smooth);
}

.documents-city-btn:hover {
  color: var(--color-black);
  border-color: var(--color-gray-400);
}

.documents-city-btn.is-active {
  color: var(--color-white);
  background-color: var(--color-black);
  border-color: var(--color-black);
}

.documents-city-btn__count {
  font-size: var(--text-tiny);
  opacity: var(--opacity-subtle);
}

.documents-complex-chip {
  padding: var(--space-8) var(--space-16);
  font-size: var(--text-body-sm);
  color: var(--color-gray-600);
  background-color: transparent;
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--radius-sm);
  transition: all var(--anim-duration-fast) var(--anim-easing-smooth);
}

.documents-complex-chip:hover {
  color: var(--color-black);
  border-color: var(--color-black);
}

.documents-complex-chip.is-active {
  color: var(--color-black);
  background-color: var(--color-bg-alt);
  border-color: var(--color-black);
  font-weight: var(--font-weight-medium);
}

/* Баннер выбранного ЖК */
.complex-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-24) var(--space-32);
  margin-bottom: var(--space-32);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--radius-md);
  background-color: var(--color-bg-alt);
}

.complex-banner__badge {
  font-size: var(--text-micro);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-widest);
  color: var(--color-gray-500);
  margin-bottom: var(--space-4);
}

.complex-banner__title {
  font-size: var(--text-h5);
  font-weight: var(--font-weight-regular);
  color: var(--color-black);
  margin-bottom: var(--space-4);
}

.complex-banner__address {
  display: inline-flex;
  align-items: center;
  gap: var(--space-6);
  font-size: var(--text-body-sm);
  color: var(--color-gray-600);
}

.complex-banner__stat {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.complex-banner__stat-number {
  font-size: var(--text-h3);
  font-weight: var(--font-weight-light);
  line-height: var(--line-height-none);
  color: var(--color-black);
}

.complex-banner__stat-label {
  font-size: var(--text-caption);
  color: var(--color-gray-500);
  margin-top: var(--space-4);
}

/* Список документов (Editorial List) */
.documents-list {
  display: flex;
  flex-direction: column;
  border-top: var(--border-width) solid var(--color-border);
}

.document-item {
  display: flex;
  align-items: center;
  gap: var(--space-24);
  padding: var(--space-24) var(--space-16);
  border-bottom: var(--border-width) solid var(--color-border);
  background-color: transparent;
  transition: background-color var(--anim-duration-fast) var(--anim-easing-smooth);
}

.document-item:hover {
  background-color: var(--color-bg-alt);
}

.document-item__icon-wrapper {
  flex: 0 0 var(--space-48);
  height: var(--space-48);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  background-color: var(--color-bg-light);
  color: var(--color-gray-600);
  transition: all var(--anim-duration-fast) var(--anim-easing-smooth);
}

.document-item:hover .document-item__icon-wrapper {
  background-color: var(--color-black);
  color: var(--color-white);
}

.document-item__main {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.document-item__title {
  font-size: var(--text-body-lg);
  font-weight: var(--font-weight-regular);
  color: var(--color-black);
  line-height: var(--line-height-heading);
}

.document-item__meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-8);
  font-size: var(--text-small);
  color: var(--color-gray-500);
}

.document-item__category {
  color: var(--color-gray-700);
}

.document-item__dot {
  color: var(--color-gray-300);
}

.document-item__badge {
  font-family: var(--font-family-mono);
  font-size: var(--text-tiny);
  letter-spacing: var(--letter-spacing-tight);
  padding: var(--space-2) var(--space-6);
  background-color: var(--color-bg-light);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--radius-xs);
  color: var(--color-gray-600);
}

.document-item__actions {
  display: flex;
  align-items: center;
  gap: var(--space-12);
  flex-shrink: 0;
}

.document-action-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-6);
  padding: var(--space-8) var(--space-16);
  font-size: var(--text-small);
  font-weight: var(--font-weight-regular);
  color: var(--color-gray-700);
  background-color: var(--color-bg-light);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--radius-sm);
  transition: all var(--anim-duration-fast) var(--anim-easing-smooth);
}

.document-action-btn:hover {
  color: var(--color-black);
  background-color: var(--color-white);
  border-color: var(--color-black);
  transform: translateY(calc(var(--space-2) * -1));
}

.document-action-btn--download {
  color: var(--color-white);
  background-color: var(--color-black);
  border-color: var(--color-black);
}

.document-action-btn--download:hover {
  background-color: var(--color-gray-900);
  border-color: var(--color-gray-900);
  color: var(--color-white);
}

/* Пустое состояние (Empty state) */
.documents-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: var(--space-100) var(--space-20);
  border-top: var(--border-width) solid var(--color-border);
}

.documents-empty__icon {
  color: var(--color-gray-300);
  margin-bottom: var(--space-20);
}

.documents-empty__title {
  font-size: var(--text-h5);
  font-weight: var(--font-weight-regular);
  color: var(--color-black);
  margin-bottom: var(--space-8);
}

.documents-empty__text {
  font-size: var(--text-body);
  color: var(--color-gray-500);
  margin-bottom: var(--space-24);
  max-width: var(--menu-width);
}

.documents-empty__reset {
  display: inline-flex;
  padding: var(--space-10) var(--space-24);
  font-size: var(--text-body-sm);
  color: var(--color-black);
  background-color: var(--color-bg-light);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--radius-pill);
  transition: all var(--anim-duration-fast) var(--anim-easing-smooth);
}

.documents-empty__reset:hover {
  background-color: var(--color-black);
  color: var(--color-white);
  border-color: var(--color-black);
}

/* Адаптивность для мобильных и планшетов (согласно Матрице устройств) */
@media (max-width: 1024px) {
  .documents-page__header {
    flex-direction: column;
    align-items: stretch;
  }

  .documents-search {
    flex: auto;
    width: 100%;
  }

  .documents-tabs {
    flex-direction: column;
    gap: var(--space-8);
  }

  .documents-tab {
    width: 100%;
    justify-content: space-between;
  }

  .documents-cities-bar,
  .documents-complexes-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-12);
  }

  .documents-control-label {
    min-width: auto;
  }

  .complex-banner {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-16);
  }

  .complex-banner__stat {
    align-items: flex-start;
  }

  .document-item {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-16);
  }

  .document-item__icon-wrapper {
    display: none;
  }

  .document-item__actions {
    width: 100%;
  }

  .document-action-btn {
    flex: 1;
    justify-content: center;
  }
}
</style>
