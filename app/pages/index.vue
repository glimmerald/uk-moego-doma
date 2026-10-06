<template>
  <div class="page-index">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero__video-wrapper">
        <video
          ref="ambientVideoRef"
          class="hero__video-ambient"
          src="/main_video.mp4"
          autoplay
          loop
          muted
          playsinline
          aria-hidden="true"
        ></video>
        <div class="hero__video-inner">
          <video
            ref="mainVideoRef"
            class="hero__video"
            src="/main_video.mp4"
            autoplay
            loop
            muted
            playsinline
          ></video>
        </div>
      </div>


      <div class="hero__scroll-indicator">
        <span class="hero__scroll-text">Листайте вниз</span>
        <div class="hero__scroll-line"></div>
      </div>
    </section>

    <!-- Секция Наши ЖК -->
    <section class="section-projects" id="projects">
      <div class="projects__container">
        <div class="projects__left">
          <h2 class="projects__title">Наши ЖК</h2>
          <NuxtLink to="/map" class="btn-arrow">
            <span class="btn-arrow__text">На карту</span>
            <span class="btn-arrow__icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="1.5"
                  stroke-linecap="round" stroke-linejoin="round" />
              </svg>
            </span>
          </NuxtLink>
        </div>

        <div class="projects__right">
          <p class="projects__description">
            Мы не просто обслуживаем здания — мы создаём комфортную и безопасную среду для жизни. В каждом жилом
            комплексе наша команда реализует продуманный подход: современные стандарты эксплуатации, премиальный уровень
            сервиса и внимание к каждой детали — от инженерных систем до благоустройства территории
          </p>
        </div>
      </div>
    </section>

    <!-- Третья секция (Преимущества - Аккордеон) -->
    <section class="section-advantages" id="advantages">
      <div class="advantages__container">
        <div class="advantages__header">
          <h2 class="advantages__section-title">В цифрах</h2>
          <div class="advantages__controls">
            <button class="slider-btn" type="button" aria-label="Предыдущий слайд" @click="scrollAccordion(-1)">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
                  stroke-linejoin="round" />
              </svg>
            </button>
            <button class="slider-btn" type="button" aria-label="Следующий слайд" @click="scrollAccordion(1)">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
                  stroke-linejoin="round" />
              </svg>
            </button>
          </div>
        </div>

        <div class="accordion-wrapper">
          <div class="accordion" ref="accordionRef" @pointerleave="deactivateItem" @scroll="handleAccordionScroll" @touchstart="onTouchStart" @touchend="onTouchEnd" @touchcancel="onTouchEnd">
            <div class="accordion__item" :class="{ 'is-active': activeAccordionIndex === index }"
              v-for="(adv, index) in advantagesList" :key="index"
              tabindex="0"
              role="region"
              :aria-label="adv.title"
              @pointermove="activateItem(index, $event)"
              @focus="activateItem(index, $event)"
              @keydown.enter="activateItem(index, $event)"
              @keydown.space.prevent="activateItem(index, $event)">
              <div class="accordion__bg">
                <img :src="adv.image" alt="" aria-hidden="true" loading="lazy" />
                <div class="accordion__bg-overlay"></div>
              </div>

              <div class="accordion__content">
                <div class="accordion__number">{{ adv.number }}</div>
                <div class="accordion__text-wrapper">
                  <h3 class="accordion__title">{{ adv.title }}</h3>
                  <p class="accordion__description">{{ adv.text }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Пятая секция (Диспетчерская - Sticky Split-Screen) -->
    <section class="section-dispatch" id="dispatch">
      <div class="dispatch__container">
        <!-- Левая залипающая часть -->
        <div class="dispatch__left">
          <div class="dispatch__content">
            <div class="dispatch__huge-text">24/7</div>
            <h2 class="dispatch__title">На страже комфорта</h2>
            <p class="dispatch__description">
              Наша аварийно-диспетчерская служба работает круглосуточно.
              Инженеры, сантехники и электрики всегда дежурят на объекте, чтобы решить любую задачу в течение 15 минут.
              Ваше спокойствие под надежной защитой без выходных и праздников.
            </p>
            <a :href="contactsData.dispatch.link" class="dispatch__phone">
              {{ contactsData.dispatch.phone }}
            </a>
          </div>
        </div>

        <!-- Правая прокручиваемая часть с фото -->
        <div class="dispatch__right">
          <div class="dispatch__photo">
            <img :src="'/optimized/Фасад/DSC04411.webp'" alt="Служба заботы" loading="lazy">
          </div>
          <div class="dispatch__photo dispatch__photo--offset">
            <img :src="'/optimized/Фасад/DSC04615.webp'" alt="Инженер" loading="lazy">
          </div>
          <div class="dispatch__photo">
            <img :src="'/optimized/Фасад/DSC04613.webp'" alt="Техническое обслуживание" loading="lazy">
          </div>
          <div class="dispatch__photo dispatch__photo--offset">
            <img :src="'/optimized/Фасад/DSC04603.webp'" alt="Консьерж" loading="lazy">
          </div>
        </div>
      </div>
    </section>

    <!-- Шестая секция (Новости - Editorial List) -->
    <section class="section-news" id="news">
      <div class="news__container">
        <!-- Заголовок на всю ширину (или только слева), чтобы выровнять контент -->
        <div class="news__header">
          <h2 class="news__visual-title">Новости</h2>
        </div>

        <div class="news__grid">
          <!-- Колонка 1, Строка 1: Изображение (Только Десктоп) -->
          <div class="news__image-container">
            <div v-for="(news, index) in newsList" :key="'img-' + index" class="news__image"
              :class="{ 'is-active': activeNewsIndex === index }">
              <img :src="news.image" :alt="news.title" loading="lazy">
            </div>
          </div>

          <!-- Колонка 2, Строка 1: Список новостей (Десктоп) / Аккордеон (Мобилка) -->
          <div class="news__list">
            <div class="news-list__item" v-for="(news, index) in newsList" :key="'item-' + index"
              :class="{ 'is-active': activeNewsIndex === index }" 
              tabindex="0"
              role="button"
              :aria-expanded="activeNewsIndex === index"
              @click="onNewsClick(index)"
              @keydown.enter.prevent="onNewsClick(index)"
              @keydown.space.prevent="onNewsClick(index)">
              
              <div class="news-list__header">
                <div class="news-list__date">{{ news.date }}</div>
                <h3 class="news-list__title">{{ news.title }}</h3>
              </div>
              
              <!-- Контент аккордеона (Только Мобилка) -->
              <div class="news-list__mobile-body">
                <div class="news-list__mobile-inner">
                  <div class="news-list__mobile-image">
                    <img :src="news.image" :alt="news.title" loading="lazy">
                  </div>
                  <div class="news-list__mobile-excerpt">
                    <p>{{ news.excerpt }}</p>
                    <NuxtLink :to="`/news/${news.slug}`" class="btn-arrow" :aria-label="'Читать новость целиком: ' + news.title">
                      <span class="btn-arrow__text">Читать целиком</span>
                      <span class="btn-arrow__icon" aria-hidden="true">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                          <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                        </svg>
                      </span>
                    </NuxtLink>
                  </div>
                </div>
              </div>

            </div>
          </div>

          <!-- Колонка 1, Строка 2: Текст новости и кнопка (Только Десктоп) -->
          <div class="news__content">
            <div v-for="(news, index) in newsList" :key="'text-' + index" class="news__excerpt"
              :class="{ 'is-active': activeNewsIndex === index }">
              <p>{{ news.excerpt }}</p>
              <NuxtLink :to="`/news/${news.slug}`" class="btn-arrow" :aria-label="'Читать новость целиком: ' + news.title">
                <span class="btn-arrow__text">Читать целиком</span>
                <span class="btn-arrow__icon" aria-hidden="true">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="1.5"
                      stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </span>
              </NuxtLink>
            </div>
          </div>

          <!-- Колонка 2, Строка 2: Кнопка "Все новости" -->
          <div class="news-list__footer">
            <NuxtLink to="/news" class="news-list__view-all" aria-label="Смотреть все новости компании">Смотреть все новости ({{ totalNewsCount }})</NuxtLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Седьмая секция (Мы в СМИ - Асимметричная верстка) -->
    <section class="section-press" id="press" ref="pressSection">
      <div class="press__container">
        <h2 class="press__section-title">О нас пишут</h2>

        <div class="press__list">
          <div class="press__item" v-for="(press, index) in pressList" :key="index"
            @mouseenter="onPressMouseMove($event)" @mousemove="onPressMouseMove($event)"
            >
            <!-- Фотография-подложка, проявляемая "фонариком" -->
            <div class="press__image-reveal">
              <img :src="press.image" alt="" aria-hidden="true" class="press__image" loading="lazy" decoding="async"
                :style="press.imagePosition ? { objectPosition: press.imagePosition } : {}" />
            </div>

            <!-- Построчное/пословное проявление цитаты -->
            <div class="press__quote">
              <span v-for="(word, wIndex) in press.quote.split(' ')" :key="wIndex" class="press__word-mask">
                <span class="press__word" :style="{ transitionDelay: `calc(${wIndex} * var(--anim-word-step))` }">{{ word }}&nbsp;</span>
              </span>
            </div>

            <div class="press__footer">
              <div class="press__source glass-effect">{{ press.source }}</div>
              <NuxtLink :to="press.link" class="press__link glass-effect" :aria-label="'Читать статью в источнике: ' + press.source">
                <span>Читать статью</span>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="1.5"
                    stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Восьмая секция (Реестр задолженностей) -->
    <section class="section-debt" id="debt">
      <div class="debt__container">
        <h2 class="debt__section-title">Реестр открытых начислений</h2>
        <p class="debt__section-subtitle">
          Мы ценим прозрачность. Ниже представлена финансовая информация по объектам управления.
        </p>

        <div class="debt__tabs" role="tablist" aria-label="Города">
          <button
            class="debt__tab"
            v-for="city in debtRegistry"
            :key="city.id"
            type="button"
            role="tab"
            :aria-selected="activeCityId === city.id"
            :class="{ 'is-active': activeCityId === city.id }"
            @click="activeCityId = city.id"
          >
            {{ city.name }}
          </button>
        </div>

        <div class="debt__list" v-if="activeCity">
          
          <!-- Выпадающий список ЖК -->
          <div class="debt__complex-dropdown" :class="{ 'is-open': isComplexDropdownOpen }">
            <button
              type="button"
              class="debt__dropdown-header"
              :aria-expanded="isComplexDropdownOpen"
              aria-haspopup="listbox"
              aria-controls="debt-complex-options"
              @click="isComplexDropdownOpen = !isComplexDropdownOpen"
              @keydown.enter.prevent="isComplexDropdownOpen = !isComplexDropdownOpen"
              @keydown.space.prevent="isComplexDropdownOpen = !isComplexDropdownOpen"
              @keydown.escape="isComplexDropdownOpen = false"
            >
              <span class="debt__dropdown-title">
                {{ activeComplex ? activeComplex.name : 'Выберите жилой комплекс...' }}
              </span>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" class="debt__dropdown-icon" :class="{ 'is-rotated': isComplexDropdownOpen }" aria-hidden="true">
                <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
            </button>
            
            <Transition name="fade">
              <div class="debt__dropdown-options" id="debt-complex-options" role="listbox" aria-label="Жилые комплексы" v-if="isComplexDropdownOpen">
                <button
                  type="button"
                  class="debt__dropdown-option" 
                  v-for="complex in activeCity.complexes" :key="complex.id"
                  role="option"
                  :aria-selected="activeComplex && activeComplex.id === complex.id"
                  @click="selectComplex(complex)"
                  @keydown.enter.prevent="selectComplex(complex)"
                  @keydown.space.prevent="selectComplex(complex)">
                  <span class="debt__option-name">{{ complex.name }}</span>
                  <span class="debt__option-address" v-if="complex.address">{{ complex.address }}</span>
                </button>
              </div>
            </Transition>
          </div>

          <Transition 
            @enter="onComplexEnter" 
            @leave="onComplexLeave" 
            :css="false"
            mode="out-in"
          >
            <div class="debt__complex-content" v-if="activeComplex" :key="activeComplex.id">
              <div class="debt__building-list">
                <div class="debt__building" v-for="building in activeComplex.buildings" :key="building.id"
                  :class="{ 'is-open': building.isOpen }">
                  <button
                    type="button"
                    class="debt__building-header"
                    :aria-expanded="building.isOpen"
                    @click="toggleBuilding(building)"
                    @keydown.enter.prevent="toggleBuilding(building)"
                    @keydown.space.prevent="toggleBuilding(building)"
                  >
                    <h4 class="debt__building-name">{{ building.name }}</h4>
                    <div class="debt__building-icon" aria-hidden="true">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                        <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="icon-plus" />
                      </svg>
                    </div>
                  </button>

                  <!-- Тело аккордеона Корпуса -->
                  <div class="debt__building-body-wrapper">
                    <div class="debt__building-body">
                      <div class="debt__building-body-content">

                        <!-- Поиск внутри конкретного корпуса -->
                        <div class="debt__search-wrapper">
                          <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
                            class="debt__search-icon" aria-hidden="true">
                            <path
                              d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z"
                              stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
                              stroke-linejoin="round" />
                          </svg>
                          <input type="number" inputmode="numeric" v-model="building.searchQuery"
                            aria-label="Поиск по номеру квартиры"
                            placeholder="Поиск по номеру квартиры..." class="debt__search-input" />
                        </div>

                                    <!-- Банковский реестр (Таблица) -->
                                    <div class="debt__table">
                                      <div class="debt__table-header">
                                        <div class="debt__col debt__col--apt">Квартира</div>
                                        <div class="debt__col debt__col--period">Срок задолженности</div>
                                        <div class="debt__col debt__col--amount">Сумма к оплате</div>
                                      </div>

                                      <TransitionGroup name="debt-list" tag="div" class="debt__table-body">
                                        <div class="debt__table-row" v-for="debtor in getFilteredDebtors(building)"
                                          :key="debtor.apt">
                                          <div class="debt__col debt__col--apt">
                                            <span class="font-mono">№ {{ debtor.apt }}</span>
                                          </div>
                                          <div class="debt__col debt__col--period">{{ debtor.period }}</div>
                                          <div class="debt__col debt__col--amount">
                                            <span class="font-mono">{{ debtor.amount }}</span>
                                          </div>
                                        </div>
                                      </TransitionGroup>

                                      <Transition name="fade">
                                        <div class="debt__empty" v-if="getFilteredDebtors(building).length === 0">
                                          По запросу «{{ building.searchQuery }}» ничего не найдено.
                                        </div>
                                      </Transition>
                                    </div>

                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>

            </div>
          </Transition>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import contactsData from '@/assets/data/contacts.json'

// Hero Video Elements (Main & Ambient Backlight)
const mainVideoRef = ref(null)
const ambientVideoRef = ref(null)

const accordionRef = ref(null)
const activeAccordionIndex = ref(0)
let scrollLock = false

const activateItem = (index, event) => {
  if (scrollLock) return
  if (activeAccordionIndex.value === index) return

  activeAccordionIndex.value = index

  if (!accordionRef.value || !event) return

  const el = event.currentTarget
  if (!el || typeof el.getBoundingClientRect !== 'function') return
  const rect = el.getBoundingClientRect()
  const containerRect = accordionRef.value.getBoundingClientRect()

  if (window.innerWidth <= 1024) {
    // На мобилке просто крутим карточку в центр, scroll-snap поможет
    el.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' })
    return
  }

    const elLeft = rect.left - containerRect.left
    const cs = window.getComputedStyle(accordionRef.value)
    const expandedWidth = parseFloat(cs.getPropertyValue('--accordion-item-active-width')) || rect.width
    const paddingRight = parseFloat(cs.getPropertyValue('--space-40')) || 0

  let delta = 0

  // Если обрезано слева
  if (elLeft < 0) {
    delta = elLeft
  }
  // Если обрезано справа
  else if (elLeft + expandedWidth + paddingRight > containerRect.width) {
    delta = (elLeft + expandedWidth + paddingRight) - containerRect.width
  }

  if (delta !== 0) {
    scrollLock = true
    accordionRef.value.scrollBy({ left: delta, behavior: 'smooth' })

    // Блокируем смену активного элемента во время скролла, чтобы избежать багов (дребезга)
    setTimeout(() => {
      scrollLock = false
    }, 500)
  }
}

const deactivateItem = () => {
  if (scrollLock) return
  if (window.innerWidth <= 1024) return // На мобилке не снимаем активный класс при отпускании пальца
  activeAccordionIndex.value = null
}

let scrollTimeout = null
let isDragging = false
let hasScrolled = false

const onTouchStart = () => {
  if (window.innerWidth > 1024) return
  isDragging = true
  hasScrolled = false
}

const onTouchEnd = () => {
  if (window.innerWidth > 1024) return
  isDragging = false
  handleAccordionScroll()
}

const handleAccordionScroll = () => {
  if (window.innerWidth > 1024 || scrollLock) return

  if (scrollTimeout) {
    clearTimeout(scrollTimeout)
  }

  scrollTimeout = setTimeout(() => {
    if (isDragging) return // Не раскрываем, пока палец на экране
    if (!accordionRef.value) return

    const container = accordionRef.value
    const children = Array.from(container.children)
    const windowCenter = window.innerWidth / 2

    let bestIndex = 0
    let minDiff = Infinity

    children.forEach((child, index) => {
      const rect = child.getBoundingClientRect()
      // Центр карточки относительно окна
      const childCenter = rect.left + rect.width / 2
      const diff = Math.abs(windowCenter - childCenter)
      
      if (diff < minDiff) {
        minDiff = diff
        bestIndex = index
      }
    })

    activeAccordionIndex.value = bestIndex
    targetAccordionIndex = null // Сбрасываем таргет
  }, 150)
}

let targetAccordionIndex = null

const scrollAccordion = (direction) => {
  if (accordionRef.value) {
    if (window.innerWidth <= 1024) {
      let currentIndex = targetAccordionIndex !== null ? targetAccordionIndex : (activeAccordionIndex.value !== null ? activeAccordionIndex.value : 0)
      
      const children = Array.from(accordionRef.value.children)
      let newIndex = currentIndex + direction
      if (newIndex < 0) newIndex = 0
      if (newIndex >= children.length) newIndex = children.length - 1
      
      if (newIndex === currentIndex) return

      targetAccordionIndex = newIndex

      // Сначала плавно доезжаем до нужной карточки (ширина не меняется, нет рывков)
      children[newIndex].scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' })
      
      // Всю остальную магию (раскрытие после остановки) берет на себя handleAccordionScroll!
      // Мы убрали scrollLock, так что можно спамить кликами сколько угодно!
    } else {
      if (scrollLock) return
      scrollLock = true
      const scrollAmount = 350
      accordionRef.value.scrollBy({ left: direction * scrollAmount, behavior: 'smooth' })
      
      setTimeout(() => {
        scrollLock = false
        handleAccordionScroll()
      }, 500)
    }
  }
}

const advantagesList = [
  {
    number: '> 15',
    title: 'Жилых комплексов',
    text: 'В портфеле нашей управляющей компании более 15 объектов премиум и бизнес-класса в разных городах.',
    image: '/optimized/Фасад/DSC04808.webp'
  },
  {
    number: '24/7',
    title: 'Служба заботы',
    text: 'Круглосуточная диспетчерская служба и консьерж-сервис, готовые решить любой вопрос за считанные минуты.',
    image: '/optimized/Фасад/DSC05913.webp'
  },
  {
    number: '50к+',
    title: 'Счастливых жителей',
    text: 'Мы создаем комьюнити, где каждый житель чувствует себя в безопасности и максимальном комфорте.',
    image: '/optimized/Фасад/DSC04833.webp'
  },
  {
    number: '10 лет',
    title: 'Безупречной работы',
    text: 'С 2014 года мы задаем новые стандарты управления недвижимостью на российском рынке.',
    image: '/optimized/Фасад/DSC04416.webp'
  },
  {
    number: '№ 1',
    title: 'Рейтинг доверия',
    text: 'Первое место по результатам независимых опросов среди резидентов элитных домов в 2023 году.',
    image: '/optimized/Фасад/DSC04416.webp'
  },
  {
    number: '15 мин',
    title: 'Скорость реакции',
    text: 'Среднее время прибытия мастера по заявке. Мы ценим ваше время и действуем на опережение.',
    image: '/optimized/Фасад/DSC04414.webp'
  },
  {
    number: '100%',
    title: 'Прозрачность',
    text: 'Полная детализация расходов и доступ к финансовой отчетности вашего дома через мобильное приложение.',
    image: '/optimized/Фасад/DSC04788.webp'
  },
  {
    number: '4',
    title: 'Региона',
    text: 'Мы успешно масштабируем наш премиальный сервис: Москва, Краснодар, Адыгея, Калининград.',
    image: '/optimized/Фасад/DSC04827.webp'
  }
]

const activeNewsIndex = ref(0)
const onNewsClick = (index) => {
  if (typeof window !== 'undefined' && window.innerWidth <= 1024) {
    // На мобильных устройствах работает как аккордеон (открыть/закрыть)
    activeNewsIndex.value = activeNewsIndex.value === index ? null : index
  } else {
    // На десктопе клик фиксирует новость и никогда не прячет картинку
    activeNewsIndex.value = index
  }
}
const handleNewsResize = () => {
  if (typeof window !== 'undefined' && window.innerWidth > 1024 && activeNewsIndex.value === null) {
    activeNewsIndex.value = 0
  }
}

import { getAllNews } from '~/data/news'

const allNewsData = getAllNews()
const totalNewsCount = allNewsData.length
const newsList = allNewsData.slice(0, 5).map(item => ({
  date: item.displayDateShort,
  title: item.title,
  excerpt: item.excerpt,
  image: item.coverImage,
  slug: item.slug
}))

import press1 from '@/assets/images/press/press-1.jpg'
import press2 from '@/assets/images/press/press-2.jpg'
import press3 from '@/assets/images/press/press-3.jpg'
import press4 from '@/assets/images/press/press-4.jpg'
import press5 from '@/assets/images/press/press-5.jpg'
import kazaryanImg from '@/assets/images/press/kazaryan.jpg'

const pressList = [
  {
    quote: '«Есть миф, что женщина не может руководить в ЖКХ. За 10 лет я научилась среди ночи рассказывать, где протекла кровля и как перезапустить тепловой пункт. Я открыта для людей и критики. Когда благодарность сменяет недовольство — это победа.» — Светлана Казарян, директор «УК Моего Дома»',
    source: 'The Blueprint',
    link: 'https://theblueprint.ru/career/special/domiland-interview',
    image: kazaryanImg,
    imagePosition: 'center calc(var(--percent-50) + var(--img-offset-140))'
  },
  {
    quote: 'Идеальный пример того, как смелый архитектурный замысел поддерживается безупречной, невидимой глазу эксплуатацией здания. Инженерные системы функционируют как швейцарские часы, обеспечивая жильцам максимальный уровень безопасности и абсолютную тишину.',
    source: 'РБК Недвижимость',
    link: '#',
    image: press2
  },
  {
    quote: 'Будущее рынка элитного жилья за девелоперами, которые делают ставку не только на метры, но и на комьюнити и круглосуточную заботу. Создание полноценной среды для жизни становится ключевым фактором при выборе недвижимости премиум-класса в современных мегаполисах.',
    source: 'Коммерсантъ',
    link: '#',
    image: press3
  },
  {
    quote: 'Первая УК, которая внедрила консьерж-сервис уровня пятизвездочного отеля в повседневную жизнь жилого комплекса. Теперь резиденты могут смело делегировать любые бытовые вопросы профессионалам, освобождая свое время для по-настоящему важных дел и общения с семьей.',
    source: 'Ведомости',
    link: '#',
    image: press4
  },
  {
    quote: 'Эталонный подход к благоустройству территории: ландшафтный парк поддерживается в идеальном состоянии круглый год. Сложные инженерные решения для полива и бережного ухода за редкими растениями позволяют сохранять эстетику дворового пространства даже в самый холодный зимний период.',
    source: 'Архитектурный вестник',
    link: '#',
    image: press5
  }
]

import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

if (typeof window !== 'undefined') {
  gsap.registerPlugin(ScrollTrigger)
}


import debtorsData from '@/assets/data/debtors.json'

// Наблюдатель для анимации появления (scroll reveal)

// Данные для секции "Реестр задолженностей"
const debtRegistry = ref(debtorsData)
const activeCityId = ref(debtorsData[0]?.id || '')
const activeCity = computed(() => debtRegistry.value.find(c => c.id === activeCityId.value))

const activeComplexId = ref(null)
const isComplexDropdownOpen = ref(false)

const activeComplex = computed(() => {
  if (!activeCity.value) return null
  return activeCity.value.complexes.find(c => c.id === activeComplexId.value)
})

const selectComplex = (complex) => {
  activeComplexId.value = complex.id
  isComplexDropdownOpen.value = false
}

const onComplexEnter = (el, done) => {
  gsap.fromTo(el,
    { height: 0, opacity: 0, overflow: 'hidden' },
    { 
      height: el.scrollHeight, 
      opacity: 1, 
      duration: 0.4, 
      ease: 'power2.out', 
      onComplete: () => {
        el.style.height = 'auto'
        el.style.overflow = 'visible'
        done()
      }
    }
  )
}

const onComplexLeave = (el, done) => {
  gsap.fromTo(el,
    { height: el.scrollHeight, opacity: 1, overflow: 'hidden' },
    { height: 0, opacity: 0, duration: 0.4, ease: 'power2.out', onComplete: done }
  )
}

watch(activeCityId, () => {
  activeComplexId.value = null
  isComplexDropdownOpen.value = false
})


const toggleBuilding = (building) => {
  building.isOpen = !building.isOpen
}

const getFilteredDebtors = (building) => {
  const query = String(building.searchQuery || '').trim().toLowerCase()
  if (!query) return building.debtors
  return building.debtors.filter(d => String(d.apt).includes(query))
}

// Эффект "фонарика" (spotlight reveal) при наведении на блок
const onPressMouseMove = (e) => {
  if (window.innerWidth <= 1024) return;
  
  const item = e.currentTarget
  const imageReveal = item.querySelector('.press__image-reveal')
  if (imageReveal) {
    const rect = imageReveal.getBoundingClientRect()
    const x = Math.round(e.clientX - rect.left)
    const y = Math.round(e.clientY - rect.top)
    const mask = `radial-gradient(circle var(--press-spotlight-size) at ${x}px ${y}px, var(--color-spotlight-center) var(--percent-15), var(--color-spotlight-mid) var(--percent-50), var(--color-spotlight-edge) var(--percent-75), var(--color-spotlight-transparent) 100%)`
    imageReveal.style.webkitMaskImage = mask
    imageReveal.style.maskImage = mask
  }
}


let syncVideos = null
let onMainPlay = null

onMounted(() => {
  // Hero Video Ambient Sync
  if (mainVideoRef.value && ambientVideoRef.value) {
    syncVideos = () => {
      if (mainVideoRef.value && ambientVideoRef.value) {
        if (Math.abs(mainVideoRef.value.currentTime - ambientVideoRef.value.currentTime) > 0.15) {
          ambientVideoRef.value.currentTime = mainVideoRef.value.currentTime
        }
      }
    }
    onMainPlay = () => {
      ambientVideoRef.value?.play()
    }
    mainVideoRef.value.addEventListener('timeupdate', syncVideos)
    mainVideoRef.value.addEventListener('seeking', syncVideos)
    mainVideoRef.value.addEventListener('play', onMainPlay)
  }

  nextTick(() => {
    // 1. Dispatch Section Parallax
    gsap.utils.toArray('.dispatch__photo').forEach(photo => {
      const img = photo.querySelector('img');
      if (!img) return;
      gsap.fromTo(img, 
        { yPercent: -20, scale: 1.4 },
        {
          yPercent: 20,
          scale: 1.4,
          ease: 'none',
          scrollTrigger: {
            trigger: photo,
            start: 'top bottom',
            end: 'bottom top',
            scrub: true
          }
        }
      );
    });

    // 2. Press Section Parallax (О нас пишут) - Только Десктоп
    let mm = gsap.matchMedia();
    mm.add("(min-width: 1025px)", () => {
      gsap.utils.toArray('.press__item').forEach((item, index) => {
        const direction = index % 2 === 0 ? 1 : -1;
        gsap.fromTo(item, 
          { y: 100 * direction },
          {
            y: -100 * direction,
            ease: 'none',
            scrollTrigger: {
              trigger: '.section-press',
              start: 'top bottom',
              end: 'bottom top',
              scrub: true
            }
          }
        );
      });
    });

    // 3. Reveal items (News, Press, Dispatch photos)
    const revealElements = gsap.utils.toArray('.dispatch__photo, .press__item, .news-list__item, .advantages__item');
    revealElements.forEach(el => {
      ScrollTrigger.create({
        trigger: el,
        start: 'top 85%',
        onEnter: () => el.classList.add('is-revealed'),
        once: true
      });
    });
  });

  window.addEventListener('resize', handleNewsResize);
})

onUnmounted(() => {
  if (mainVideoRef.value) {
    if (syncVideos) {
      mainVideoRef.value.removeEventListener('timeupdate', syncVideos);
      mainVideoRef.value.removeEventListener('seeking', syncVideos);
    }
    if (onMainPlay) {
      mainVideoRef.value.removeEventListener('play', onMainPlay);
    }
  }
  window.removeEventListener('resize', handleNewsResize);
  ScrollTrigger.getAll().forEach(t => t.kill());
})
</script>

<style scoped>
.page-index {
  overflow-x: clip;
}

.hero {
  position: relative;
  width: 100%;
  height: var(--vh-70);
  min-height: var(--hero-min-height);
  max-height: var(--hero-max-height);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  color: var(--color-white);
  background-color: var(--color-white);
}

.hero__video-wrapper {
  position: absolute;
  top: var(--header-height);
  left: 0;
  width: 100%;
  height: calc(100% - var(--header-height));
  z-index: var(--z-base);
  background-color: var(--color-black);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.hero__video-ambient {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: blur(var(--hero-ambient-blur)) saturate(var(--hero-ambient-saturate)) brightness(var(--hero-ambient-brightness));
  transform: scale(var(--hero-ambient-scale));
  opacity: var(--hero-ambient-opacity);
  pointer-events: none;
  z-index: var(--z-behind);
}

.hero__video-inner {
  position: relative;
  z-index: var(--z-above);
  height: 100%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.hero__video {
  height: 100%;
  width: auto;
  max-width: 100%;
  aspect-ratio: var(--aspect-ratio-16-9);
  object-fit: contain;
  box-shadow: var(--hero-ambient-shadow);
  pointer-events: auto;
}

.hero__scroll-indicator {
  position: absolute;
  bottom: var(--hero-scroll-bottom);
  left: var(--percent-50);
  transform: translateX(var(--translate-half-neg));
  z-index: var(--z-top);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--hero-scroll-gap);
  opacity: var(--opacity-80);
}

.hero__scroll-text {
  font-size: var(--text-micro);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-uppercase);
  text-shadow: var(--shadow-text-subtle);
}

.hero__scroll-line {
  width: var(--border-width);
  height: var(--hero-scroll-line-height);
  background-color: var(--color-line-semi-transparent);
  position: relative;
  overflow: hidden;
}

.hero__scroll-line::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: var(--percent-50);
  background-color: var(--color-white);
  animation: scroll-down var(--anim-duration-marquee) ease-in-out infinite;
}

@keyframes scroll-down {
  0% {
    transform: translateY(var(--translate-full-neg));
  }

  100% {
    transform: translateY(var(--translate-double));
  }
}

/* Responsive adjustments */
@media (max-width: 1024px) {
  .hero {
    height: calc(100vw * 9 / 16 + var(--header-height));
    min-height: 0;
    max-height: none;
    background-color: var(--color-white);
  }

  .hero__video-wrapper {
    background-color: var(--color-white);
  }

  .hero__video-ambient {
    display: none;
  }

  .hero__video-inner {
    width: 100%;
    height: 100%;
  }

  .hero__video {
    width: 100%;
    height: 100%;
    aspect-ratio: auto;
    object-fit: cover;
    box-shadow: none;
  }
}

.section-projects {
  padding: var(--space-140) 0;
  background-color: var(--color-bg);
  color: var(--color-text);
}

.projects__container {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: 0 var(--space-40);
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--projects-gap);
}

.projects__title {
  font-size: var(--text-h1);
  font-weight: var(--font-weight-light);
  line-height: var(--line-height-hero);
  margin-bottom: var(--space-40);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
  margin-left: var(--offset-optical-title); /* Оптическое выравнивание шрифта (убираем пустой отступ слева от буквы Н) */
}

.projects__description {
  font-size: var(--text-body-lg);
  font-weight: var(--font-weight-light);
  line-height: var(--line-height-loose);
  color: var(--color-text);
  max-width: var(--max-width-text);
  margin-top: calc(var(--space-4) * -1);
}

/* Стили для кнопки-ссылки */
.btn-arrow {
  display: inline-flex;
  align-items: center;
  gap: var(--space-16);
  font-size: var(--text-body-lg);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-widest);
  color: var(--color-text);
  transition: opacity var(--anim-duration-fast) ease;
}

.btn-arrow:hover {
  opacity: var(--opacity-70);
}

.btn-arrow__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: var(--space-48);
  height: var(--space-48);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--radius-round);
  transition: transform var(--anim-duration-fast) ease, background-color var(--anim-duration-fast) ease, color var(--anim-duration-fast) ease;
}

.btn-arrow__icon svg {
  width: var(--percent-50);
  height: var(--percent-50);
}

.btn-arrow:hover .btn-arrow__icon {
  transform: translateX(var(--space-8));
  background-color: var(--color-text);
  color: var(--color-bg);
}

/* Адаптив */
@media (max-width: 1024px) {
  .projects__container {
    display: flex;
    flex-direction: column;
  }

  .projects__left {
    display: contents;
  }

  .projects__title {
    order: 1;
    margin-bottom: 0;
  }

  .projects__right {
    order: 2;
  }

  .projects__description {
    margin-top: 0;
  }

  .projects__left .btn-arrow {
    order: 3;
  }
}

/* Секция Преимущества (Аккордеон) */
.section-advantages {
  padding: var(--space-140) 0;
  background-color: var(--color-bg);
  color: var(--color-text);
}

.advantages__container {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: 0 var(--space-40);
}

.advantages__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex-wrap: wrap;
  gap: var(--space-24);
  margin-bottom: var(--space-64);
}

.advantages__section-title {
  font-size: var(--text-h2);
  font-weight: var(--font-weight-light);
  text-transform: uppercase;
}

.advantages__controls {
  display: flex;
  gap: var(--space-16);
  padding-right: 0; /* controls already inside padded container */
}

.slider-btn {
  width: var(--space-56);
  height: var(--space-56);
  border-radius: var(--radius-round);
  border: var(--border-width) solid var(--color-border);
  background: transparent;
  color: var(--color-text);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color var(--anim-duration-fast) ease, color var(--anim-duration-fast) ease;
}

.slider-btn:focus-visible {
  outline: var(--border-width) solid var(--color-text);
  outline-offset: var(--space-4);
}

@media (hover: hover) {
  .slider-btn:hover {
    background-color: var(--color-text);
    color: var(--color-bg);
  }
}

.accordion-wrapper {
  position: relative;
  margin: 0 calc(var(--space-40) * -1);
  width: auto;
}

.accordion {
  display: flex;
  height: var(--accordion-height);
  gap: var(--space-16);
  width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  padding-bottom: var(--space-24);
  /* Чтобы не обрезалась тень или hover */
  padding-left: var(--space-40);
  padding-right: var(--accordion-padding-right);
  /* Отступ в конце скролла */
  scrollbar-width: none;
  /* Скрываем скроллбар в Firefox */
  -webkit-overflow-scrolling: touch;
  /* Плавный скролл на iOS */
}

.accordion::-webkit-scrollbar {
  display: none;
  /* Скрываем скроллбар в Chrome/Safari */
}

.accordion__item {
  position: relative;
  /* Убираем flex: 1, ставим фиксированную ширину и flex-shrink: 0 */
  flex-shrink: 0;
  width: var(--accordion-item-width);
  border-radius: var(--radius-md);
  overflow: hidden;
  transition: width var(--anim-duration-slow) var(--anim-easing-smooth);
  background-color: var(--color-dark);
  /* Темный фон для карточки */
  cursor: pointer;
}

.accordion__item:focus-visible {
  outline: var(--border-width) solid var(--color-white);
  outline-offset: var(--space-4);
}

.accordion__item.is-active {
  width: var(--accordion-item-active-width);
  /* Раскрытая ширина */
}

.accordion__bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: var(--z-base);
}

.accordion__bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--anim-duration-slow) ease, opacity var(--anim-duration-slow) ease;
  transform: scale(1.1);
  opacity: var(--opacity-15);
}

.accordion__item.is-active .accordion__bg img {
  transform: scale(1);
  opacity: 1;
}

.accordion__bg-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to top, var(--color-overlay-dark) 0%, transparent 100%);
  opacity: 0;
  transition: opacity var(--anim-duration-slow) ease;
}

.accordion__item.is-active .accordion__bg-overlay {
  opacity: 1;
}

.accordion__content {
  position: relative;
  z-index: var(--z-above);
  height: 100%;
  padding: var(--space-40);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  color: var(--color-white);
}

.accordion__number {
  font-size: var(--text-hero);
  font-weight: var(--font-weight-thin);
  line-height: var(--line-height-none);
  transition: transform var(--anim-duration-slow) ease, font-size var(--anim-duration-slow) ease;
}

.accordion__item.is-active .accordion__number {
  transform: translateY(calc(var(--space-10) * -1));
}

.accordion__text-wrapper {
  display: flex;
  flex-direction: column;
  gap: var(--space-16);
  width: var(--accordion-text-width);
  max-width: var(--vw-100);
}

.accordion__title {
  font-size: var(--text-subtitle);
  font-weight: var(--font-weight-regular);
  text-transform: uppercase;
}

.accordion__description {
  font-size: var(--text-body-sm);
  line-height: var(--line-height-relaxed);
  opacity: 0;
  max-height: 0;
  overflow: hidden;
  transition: opacity var(--anim-duration-slow) ease, max-height var(--anim-duration-slow) ease, transform var(--anim-duration-slow) ease;
  transform: translateY(var(--space-20));
  color: var(--color-accordion-bg);
}

.accordion__item.is-active .accordion__description {
  opacity: 1;
  max-height: var(--accordion-desc-max-height);
  transform: translateY(0);
}

@media (max-width: 1024px) {
  .accordion {
    scroll-snap-type: x mandatory;
  }

  .accordion__item {
    scroll-snap-align: center;
    scroll-snap-stop: always; /* Карточки листаются строгими "щелчками" */
    /* Неактивная карточка поменьше, чтобы соседние сильнее выглядывали */
    width: min(calc(100vw - var(--space-40) * 4), var(--accordion-item-width-tablet));
  }

  .accordion__item.is-active {
    /* Активная карточка сбалансирована под мобильные и планшеты */
    width: min(calc(100vw - var(--space-40) * 2), var(--accordion-item-active-width-tablet));
  }

  .accordion__text-wrapper {
    /* Фиксируем ширину текста такой, какой она будет в РАСКРЫТОЙ карточке */
    width: min(calc(100vw - var(--space-40) * 4), calc(var(--accordion-item-active-width-tablet) - var(--space-40) * 2));
    max-width: 100%;
  }
}

/* Секция Аварийно-диспетчерская служба */
.section-dispatch {
  background-color: var(--color-black);
  color: var(--color-white);
  position: relative;
}

.dispatch__container {
  display: flex;
  max-width: var(--container-max-width);
  margin: 0 auto;
}

.dispatch__left {
  width: var(--press-item-2-width);
  padding: 0 var(--space-40);
  height: var(--vh-100);
  position: sticky;
  top: 0;
  align-self: flex-start;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.dispatch__content {
  max-width: var(--max-width-text);
}

.dispatch__huge-text {
  font-size: var(--text-huge);
  font-weight: var(--font-weight-thin);
  line-height: var(--line-height-tight);
  color: var(--color-white);
  margin-bottom: var(--space-24);
  letter-spacing: var(--letter-spacing-tight);
}

.dispatch__title {
  font-size: var(--text-h3);
  font-weight: var(--font-weight-light);
  margin-bottom: var(--space-24);
  text-transform: uppercase;
}

.dispatch__description {
  font-size: var(--text-body-lg);
  line-height: var(--line-height-loose);
  color: var(--color-text-semi-transparent);
}

.dispatch__phone {
  display: inline-flex;
  align-items: center;
  margin-top: var(--space-48);
  font-size: var(--text-h4);
  font-weight: var(--font-weight-light);
  color: var(--color-white);
  text-decoration: none;
  letter-spacing: var(--letter-spacing-widest);
  border-bottom: var(--border-width) solid var(--color-line-semi-transparent);
  padding-bottom: var(--space-8);
  transition: border-color var(--anim-duration-fast) ease, opacity var(--anim-duration-fast) ease;
}

.dispatch__phone:hover {
  border-color: var(--color-white);
  opacity: var(--opacity-90);
}

.dispatch__right {
  width: var(--press-item-2-width);
  display: flex;
  flex-direction: column;
  padding: var(--space-140) var(--space-40) var(--space-140) 0;
  gap: var(--dispatch-gap);
}

.dispatch__photo {
  height: var(--dispatch-photo-max-height);
  width: auto;
  max-width: 100%;
  aspect-ratio: var(--aspect-ratio-4-5);
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-lg);

  /* Исходное состояние для анимации вылета справа */
  opacity: 0;
  transform: translateX(var(--space-120));
  transition: opacity var(--anim-duration-slowest) var(--anim-easing-smooth), transform var(--anim-duration-slowest) var(--anim-easing-smooth);
}

/* Класс добавляется через IntersectionObserver (JS) */
.dispatch__photo.is-revealed {
  opacity: 1;
  transform: translateX(0);
}

/* Асимметрия: сдвигаем четные фотки чуть вправо для журнального вида */
.dispatch__photo--offset {
  height: var(--dispatch-photo-max-height);
  width: auto;
  max-width: 100%;
  aspect-ratio: var(--aspect-ratio-3-4);
  margin-left: var(--dispatch-photo-offset-margin-desktop);
}

.dispatch__photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transform: scale(var(--scale-parallax));
}


@media (max-width: 1024px) {
  .dispatch__container {
    flex-direction: column;
  }

  .dispatch__left {
    width: 100%;
    height: auto;
    position: relative;
    padding: var(--space-100) var(--space-40) var(--space-60);
  }

  .dispatch__right {
    width: 100%;
    padding: 0 var(--space-40) var(--space-100) var(--space-40);
  }

  /* Исправляем залезание фотографий за пределы экрана на мобилках и калибруем высоту на планшетах */
  .dispatch__photo {
    height: auto;
    width: 100%;
    max-height: var(--dispatch-photo-max-height-tablet);
    transform: translateX(calc(var(--space-120) * -1));
  }
  .dispatch__photo--offset {
    height: auto;
    width: var(--percent-85);
    margin-left: var(--percent-15);
    max-height: var(--dispatch-photo-max-height-tablet);
    transform: translateX(var(--space-120));
  }
  /* Восстанавливаем нулевое положение после раскрытия */
  .dispatch__photo.is-revealed {
    transform: translateX(0);
  }
}

/* Секция Новости (Editorial List) */
.section-news {
  padding: var(--space-100) 0;
  background-color: var(--color-bg);
  color: var(--color-text);
}

.news__container {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: 0 var(--space-40);
}

.news__grid {
  display: grid;
  grid-template-columns: var(--news-grid-left-col) 1fr;
  column-gap: var(--space-80);
}

.news__visual-title {
  font-size: var(--text-h2);
  font-weight: var(--font-weight-light);
  text-transform: uppercase;
  margin-bottom: var(--space-32);
}

.news__image-container {
  width: 100%;
  height: 100%;
  /* Растягивается на всю высоту ячейки грида (высоту списка новостей) */
  position: relative;
  overflow: hidden;
  border-radius: var(--radius-md);
  background-color: var(--color-bg-light);
  /* Убираем margin-bottom, чтобы нижний край упирался в текст */
}

.news__image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--anim-duration-slower) ease, transform var(--anim-duration-slower) var(--anim-easing-smooth);
  transform: scale(1.05) translateY(var(--space-20));
}

.news__image.is-active {
  opacity: 1;
  pointer-events: auto;
  transform: scale(1) translateY(0);
}

.news__image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.news__content {
  position: relative;
  display: grid;
  padding-top: var(--space-24);
  /* Отступ от картинки до текста */
}

.news__excerpt {
  grid-area: 1 / 1;
  opacity: 0;
  pointer-events: none;
  visibility: hidden;
  transition: opacity var(--anim-duration-normal) ease, transform var(--anim-duration-normal) ease, visibility var(--anim-duration-normal) ease;
  transform: translateY(var(--space-10));
}

.news__excerpt.is-active {
  opacity: 1;
  pointer-events: auto;
  visibility: visible;
  transform: translateY(0);
  transition-delay: calc(var(--anim-duration-marquee) / 2);
}

.news__excerpt p {
  font-size: var(--text-body);
  line-height: var(--line-height-loose);
  color: var(--color-gray-600);
  margin-bottom: var(--space-24);
}

.news__list {
  display: flex;
  flex-direction: column;
}

.news-list__item {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  justify-content: center;
  padding: var(--space-32) 0;
  border-top: var(--border-width) solid var(--color-border);
  border-bottom: var(--border-width) solid var(--color-border);
  margin-top: calc(var(--border-width) * -1);
  /* Схлопываем двойные границы */
  cursor: pointer;
  transition: border-color var(--anim-duration-normal) ease;
  z-index: var(--z-base);
}

.news-list__header {
  display: flex;
  align-items: center;
  width: 100%;
}

.news-list__mobile-body {
  display: none; /* Скрыто на десктопе */
}

.news-list__mobile-inner {
  overflow: hidden;
  padding-top: 0;
  transition: padding-top var(--anim-duration-slow) ease;
}

.news-list__mobile-image {
  width: 100%;
  height: var(--news-image-height);
  border-radius: var(--radius-md);
  overflow: hidden;
  margin-bottom: var(--space-24);
}

.news-list__mobile-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.news-list__mobile-excerpt p {
  font-size: var(--text-body);
  line-height: var(--line-height-loose);
  color: var(--color-gray-600);
  margin-bottom: var(--space-24);
}

.news-list__item:first-child {
  margin-top: 0;
}

.news-list__date {
  font-size: var(--news-date-font-size);
  font-weight: var(--font-weight-light);
  color: var(--color-gray-300);
  width: var(--space-140);
  flex-shrink: 0;
  transition: color var(--anim-duration-normal) ease;
}

.news-list__title {
  font-size: var(--text-h6);
  font-weight: var(--font-weight-light);
  line-height: var(--line-height-heading);
  color: var(--color-gray-500); /* Делаем неактивный заголовок бледнее */
  transition: transform var(--anim-duration-normal) var(--anim-easing-smooth), color var(--anim-duration-normal) ease;
}

/* Деликатный ховер на десктопе: только мягкое усиление контраста без сдвига */
@media (hover: hover) {
  .news-list__item:hover:not(.is-active) .news-list__title {
    color: var(--color-gray-900);
  }

  .news-list__item:hover:not(.is-active) .news-list__date {
    color: var(--color-gray-500);
  }
}

/* Активное состояние (новость выбрана и открыта слева) */
.news-list__item.is-active {
  border-color: var(--color-text);
  z-index: var(--z-above);
  /* Чтобы активные границы были поверх соседних */
}

.news-list__item.is-active .news-list__date {
  color: var(--color-text);
}

.news-list__item.is-active .news-list__title {
  color: var(--color-text);
  transform: translateX(var(--space-16));
}

/* Доступность с клавиатуры (фокус) */
.news-list__item:focus-visible {
  outline: var(--border-width) solid var(--color-text);
  outline-offset: calc(var(--space-4) * -1);
  z-index: var(--z-above);
}

.news-list__item:focus-visible:not(.is-active) .news-list__title {
  color: var(--color-gray-900);
}

.news-list__item:focus-visible:not(.is-active) .news-list__date {
  color: var(--color-gray-500);
}

.news-list__footer {
  display: flex;
  align-items: center;
  /* Центрируем по вертикали */
  justify-content: flex-start;
  height: 100%;
  /* Высота равна левому блоку */
  padding: var(--space-24) 0;
  border-bottom: var(--border-width) solid var(--color-border);
  /* Нижняя граница, выравнивающаяся с левой колонкой */
}

.news-list__view-all {
  font-size: var(--text-body-lg);
  color: var(--color-text);
  text-decoration: none;
  border-bottom: var(--border-width) solid var(--color-text);
  padding-bottom: var(--space-4);
  transition: opacity var(--anim-duration-fast) ease;
}

.news-list__view-all:hover {
  opacity: var(--opacity-60);
}

/* Секция 7: Мы в СМИ (Парящий ритм) */
.section-press {
  padding: var(--space-160) 0;
  background-color: var(--color-bg);
  color: var(--color-text);
  overflow: hidden;
}

.press__container {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: 0 var(--space-40);
}

.press__section-title {
  font-size: var(--text-h2);
  font-weight: var(--font-weight-light);
  text-transform: uppercase;
  margin-bottom: var(--space-120);
  text-align: center;
}

.press__list {
  display: flex;
  flex-direction: column;
  gap: var(--space-160);
  /* Огромный отступ между цитатами */
}

.press__item {
  position: relative;
  display: flex;
  flex-direction: column;
  isolation: isolate;
  /* Создаем контекст наложения, чтобы фото z-index:-1 не проваливалось под секцию */
}

/* Асимметрия / Парящий ритм */
.press__item:nth-child(1) {
  width: var(--press-item-1-width);
  align-self: flex-start;
  margin-left: 0;
}

.press__item:nth-child(2) {
  width: var(--press-item-2-width);
  align-self: flex-end;
  margin-right: var(--press-item-2-margin);
  margin-top: var(--space-120);
}

.press__item:nth-child(3) {
  width: var(--press-item-3-width);
  align-self: flex-start;
  margin-left: var(--press-item-3-margin);
}

.press__item:nth-child(4) {
  width: var(--press-item-4-width);
  align-self: flex-end;
  margin-right: var(--press-item-4-margin);
}

.press__item:nth-child(5) {
  width: var(--press-item-5-width);
  align-self: center;
  margin-top: var(--space-120);
}

/* Огромная фоновая кавычка (как в первой идее) */
.press__item::before {
  content: '“';
  position: absolute;
  top: calc(var(--space-80) * -1);
  left: calc(var(--space-60) * -1);
  font-size: var(--press-quote-bg-size);
  line-height: var(--line-height-none);
  font-family: var(--font-family-serif);
  /* Классическая кавычка с засечками */
  color: var(--color-border);
  opacity: var(--opacity-50);
  z-index: var(--z-behind);
  pointer-events: none;
  transition: opacity var(--anim-duration-medium) ease;
}

.press__quote {
  position: relative;
  z-index: var(--z-base);
  font-size: var(--press-quote-font-size);
  font-weight: var(--font-weight-light);
  line-height: var(--line-height-base);
  margin-bottom: var(--press-quote-margin-bottom);
}

/* Маска для каждого слова */
.press__word-mask {
  position: relative;
  z-index: var(--z-base);
  display: inline-block;
  overflow: hidden;
  vertical-align: top;
}

/* Само слово прячем снизу */
.press__word {
  display: inline-block;
  transform: translate3d(0, var(--translate-full), 0);
  opacity: 0;
  will-change: transform, opacity;
  backface-visibility: hidden;
  transition: transform var(--anim-duration-fast) ease-out, opacity var(--anim-duration-fast) ease-out;
}

/* Когда родитель получает .is-revealed, слова поднимаются */
.press__item.is-revealed .press__word {
  transform: translate3d(0, 0, 0);
  opacity: 1;
}

.press__footer {
  position: relative;
  z-index: var(--z-base);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--space-16);
  padding-top: var(--space-24);
  border-top: var(--border-width) solid var(--color-border);
}

.press__source {
  font-size: var(--text-subtitle);
  font-weight: var(--font-weight-regular);
  font-family: var(--font-family-serif);
  letter-spacing: var(--letter-spacing-wide);
  padding: var(--space-16) var(--space-24);
  border-radius: var(--radius-xs);
}

.press__link {
  display: flex;
  align-items: center;
  gap: var(--space-12);
  font-size: var(--text-body-sm);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-widest);
  color: var(--color-text);
  border-radius: var(--radius-xs);

  padding: var(--space-16) var(--space-24);
}

.press__link svg {
  transition: transform var(--anim-duration-fast) ease;
}

.press__link:hover svg {
  transform: translateX(var(--space-8));
}

/* Эффект "фонарика" с фото на заднем плане строго вокруг текста цитаты */
.press__image-reveal {
  position: absolute;
  top: calc(var(--space-64) * -1);
  bottom: calc(var(--space-64) * -1);
  left: calc(var(--space-80) * -1);
  right: calc(var(--space-80) * -1);
  z-index: var(--z-behind);
  border-radius: var(--radius-lg);
  opacity: 0;
  overflow: hidden;
  transition: opacity var(--anim-duration-medium) ease;

  /* Начальная маска до первого движения мыши */
  -webkit-mask-image: radial-gradient(circle var(--press-spotlight-size) at var(--percent-50) var(--percent-50), var(--color-spotlight-center) var(--percent-15), var(--color-spotlight-mid) var(--percent-50), var(--color-spotlight-edge) var(--percent-75), var(--color-spotlight-transparent) 100%);
  mask-image: radial-gradient(circle var(--press-spotlight-size) at var(--percent-50) var(--percent-50), var(--color-spotlight-center) var(--percent-15), var(--color-spotlight-mid) var(--percent-50), var(--color-spotlight-edge) var(--percent-75), var(--color-spotlight-transparent) 100%);
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-size: 100% 100%;
  mask-size: 100% 100%;
}

.press__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.press__item:hover .press__image-reveal {
  opacity: var(--opacity-95);
}

/* Приглушаем фоновую кавычку при наведении, но оставляем легкий силуэт */
.press__item:hover::before {
  opacity: var(--opacity-15);
  transition: opacity var(--anim-duration-medium) ease;
}

/* Секция 8: Реестр задолженностей */
.section-debt {
  padding: var(--space-160) 0;
  background-color: var(--color-debt-bg);
  color: var(--color-text);
}

.debt__container {
  max-width: var(--debt-container-max-width);
  margin: 0 auto;
  padding: 0 var(--space-40);
}

.debt__section-title {
  font-size: var(--text-h3);
  font-weight: var(--font-weight-light);
  margin-bottom: var(--space-24);
}

.debt__section-subtitle {
  font-size: var(--text-body-lg);
  color: var(--color-gray-600);
  margin-bottom: var(--space-80);
  max-width: var(--max-width-text);
}

.debt__tabs {
  display: flex;
  gap: var(--debt-tabs-gap);
  margin-bottom: var(--debt-tabs-margin-bottom);
  border-bottom: var(--border-width) solid var(--color-debt-border);
}

.debt__tab {
  font-size: var(--text-h5);
  font-weight: var(--font-weight-regular);
  color: var(--color-gray-400);
  padding-bottom: var(--debt-tab-padding-bottom);
  position: relative;
  transition: color var(--anim-duration-medium) ease;
}

.debt__tab:hover,
.debt__tab.is-active {
  color: var(--color-black);
}

.debt__tab:focus-visible {
  outline: var(--border-width) solid var(--color-black);
  outline-offset: var(--space-4);
}

.debt__tab::after {
  content: '';
  position: absolute;
  bottom: calc(var(--border-width) * -1);
  left: 0;
  width: 100%;
  height: calc(var(--border-width) * 2);
  background-color: var(--color-black);
  opacity: 0;
  transition: opacity var(--anim-duration-medium) ease;
}

.debt__tab.is-active::after {
  opacity: 1;
}

.debt__list {
  display: flex;
  flex-direction: column;
}


.debt__complex-dropdown {
  position: relative;
  margin-bottom: var(--space-40);
  z-index: var(--z-top);
}

.debt__dropdown-header {
  width: 100%;
  text-align: left;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-24) 0;
  border-bottom: var(--border-width) solid var(--color-black);
  cursor: pointer;
  transition: opacity var(--anim-duration-fast) ease;
}

.debt__dropdown-header:hover {
  opacity: var(--opacity-70);
}

.debt__dropdown-header:focus-visible {
  outline: var(--border-width) solid var(--color-black);
  outline-offset: var(--space-4);
}

.debt__dropdown-title {
  font-size: var(--text-h4);
  font-weight: var(--font-weight-light);
  color: var(--color-black);
}

.debt__dropdown-icon {
  color: var(--color-black);
  transition: transform var(--anim-duration-medium) var(--anim-easing-smooth);
}

.debt__dropdown-icon.is-rotated {
  transform: rotate(180deg);
}

.debt__dropdown-options {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background-color: var(--color-white);
  box-shadow: var(--shadow-lg);
  border-radius: 0 0 var(--radius-md) var(--radius-md);
  overflow: hidden;
  max-height: var(--max-height-dropdown);
  overflow-y: auto;
}

.debt__dropdown-option {
  width: 100%;
  text-align: left;
  padding: var(--space-24) var(--space-40);
  cursor: pointer;
  border-bottom: var(--border-width) solid var(--color-debt-border);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  transition: background-color var(--anim-duration-fast) ease;
}

.debt__dropdown-option:last-child {
  border-bottom: none;
}

.debt__dropdown-option:hover,
.debt__dropdown-option:focus-visible {
  background-color: var(--color-debt-hover);
  outline: none;
}

.debt__option-name {
  font-size: var(--text-body-lg);
  font-weight: var(--font-weight-regular);
  color: var(--color-black);
}

.debt__option-address {
  font-size: var(--text-body-sm);
  color: var(--color-gray-400);
}


/* Корпуса (Buildings) */
.debt__building-list {
  display: flex;
  flex-direction: column;
  padding-left: var(--space-24);
  /* Небольшой отступ для вложенности */
}

.debt__building {
  border-bottom: var(--border-width) solid var(--color-debt-border);
}

.debt__building:last-child {
  border-bottom: none;
}

.debt__building-header {
  width: 100%;
  text-align: left;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-24) 0;
  cursor: pointer;
  color: var(--color-gray-600);
  transition: color var(--anim-duration-fast) ease;
}

.debt__building-header:hover {
  color: var(--color-black);
}

.debt__building-header:focus-visible {
  outline: var(--border-width) solid var(--color-black);
  outline-offset: var(--space-4);
}

.debt__building-name {
  font-size: var(--text-body-lg);
  font-weight: var(--font-weight-regular);
}

.debt__building-icon {
  width: var(--space-48);
  height: var(--space-48);
  border-radius: var(--radius-round);
  border: var(--border-width) solid var(--color-debt-border);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-gray-600);
  transition: transform var(--anim-duration-normal) var(--anim-easing-smooth), background-color var(--anim-duration-fast) ease, color var(--anim-duration-fast) ease, border-color var(--anim-duration-fast) ease;
}

.debt__building-header:hover .debt__building-icon {
  background-color: var(--color-debt-hover);
}

.debt__building.is-open .debt__building-icon {
  transform: rotate(45deg);
  background-color: var(--color-black);
  color: var(--color-white);
  border-color: var(--color-black);
}

.debt__building.is-open .debt__building-header {
  color: var(--color-black);
}

.debt__building-body-wrapper {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows var(--anim-duration-normal) var(--anim-easing-smooth);
}

.debt__building.is-open .debt__building-body-wrapper {
  grid-template-rows: 1fr;
}

.debt__building-body {
  overflow: hidden;
}

.debt__building-body-content {
  padding-bottom: var(--space-32);
  padding-top: var(--space-8);
}

.debt__search-wrapper {
  display: flex;
  align-items: center;
  padding: var(--space-16) var(--space-24);
  background-color: var(--color-white);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--radius-sm);
  margin-bottom: var(--space-32);
  gap: var(--space-12);
}

.debt__search-icon {
  color: var(--color-gray-300);
}

.debt__search-input {
  flex: 1;
  border: none;
  outline: none;
  font-family: inherit;
  font-size: var(--text-body-sm);
  background: transparent;
  color: var(--color-text);
  /* Убираем стрелочки у number input */
  -moz-appearance: textfield;
}

.debt__search-input::-webkit-outer-spin-button,
.debt__search-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.debt__search-input::placeholder {
  color: var(--color-gray-200);
}

.debt__table {
  display: flex;
  flex-direction: column;
  container-type: inline-size;
  container-name: debttable;
}

.debt__table-header {
  display: flex;
  padding: var(--space-16) var(--space-24);
  font-size: var(--text-caption);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-widest);
  color: var(--color-gray-300);
  border-bottom: var(--border-width) solid var(--color-debt-border);
}

/* Анимации для списка должников */
.debt__table-body {
  position: relative;
}

.debt-list-move,
.debt-list-enter-active,
.debt-list-leave-active {
  transition: all var(--anim-duration-normal) ease;
}

.debt-list-enter-from,
.debt-list-leave-to {
  opacity: 0;
  transform: translateX(var(--space-20));
}

.debt-list-leave-active {
  position: absolute;
  width: 100%;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--anim-duration-normal) ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.debt__table-row {
  display: flex;
  padding: var(--space-24);
  border-bottom: var(--border-width) solid var(--color-debt-hover);
  background-color: transparent;
  transition: background-color calc(var(--anim-duration-marquee) / 2) ease;
}

.debt__table-row:hover {
  background-color: var(--color-white);
}

.debt__col {
  flex: 1;
}

.debt__col--apt {
  flex: 0 0 var(--debt-col-apt-width);
  color: var(--color-gray-600);
}

.debt__col--period {
  flex: 1;
  color: var(--color-gray-600);
}

.debt__col--amount {
  flex: 0 0 var(--debt-col-amount-width);
  text-align: right;
  font-weight: var(--font-weight-regular);
}

.font-mono {
  font-family: var(--font-family-mono);
  font-size: var(--text-body);
  letter-spacing: var(--letter-spacing-tight);
}

.debt__empty {
  padding: var(--space-40);
  text-align: center;
  color: var(--color-gray-300);
  font-style: italic;
}

@media (max-width: 1024px) {
  .news__grid {
    grid-template-columns: 1fr;
    row-gap: var(--space-40);
  }

  /* Скрываем десктопные колонки с фото и текстом */
  .news__image-container,
  .news__content {
    display: none;
  }

  /* Стили для аккордеона внутри списка */
  .news-list__mobile-body {
    display: grid;
    grid-template-rows: 0fr;
    opacity: 0;
    transition: grid-template-rows var(--anim-duration-slow) ease, opacity var(--anim-duration-slow) ease;
  }

  .news-list__item.is-active .news-list__mobile-body {
    grid-template-rows: 1fr;
    opacity: 1;
  }

  .news-list__item.is-active .news-list__mobile-inner {
    padding-top: var(--space-32);
  }

  /* Стили для заголовка аккордеона (мобилка) */
  .news-list__header {
    flex-direction: column-reverse;
    align-items: flex-start;
    gap: var(--space-16);
  }

  .news-list__date {
    width: 100%;
    text-align: right;
  }

  .news-list__title {
    width: 100%;
  }

  /* Отключаем десктопный ховер-сдвиг заголовка, так как он не нужен на мобилке */
  .news-list__item:hover .news-list__title,
  .news-list__item:focus-visible .news-list__title,
  .news-list__item.is-active .news-list__title {
    transform: none;
  }

  .news-list__footer {
    height: auto;
    padding: var(--space-32) 0;
  }

  /* Press section mobile cards */
  .press__item:nth-child(n) {
    width: 100%;
    margin-left: 0;
    margin-right: 0;
    align-self: stretch;
    margin-top: 0;
  }

  .press__item::before {
    display: none; /* Убираем фоновую гигантскую кавычку на мобилке */
  }

  .press__image-reveal {
    position: relative;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    height: var(--news-image-height);
    opacity: 1 !important; /* Всегда видим на мобилке */
    mask-image: none !important;
    -webkit-mask-image: none !important;
    margin-bottom: var(--space-24);
    border-radius: var(--radius-md);
  }

  .press__image {
    object-position: center center !important; /* Отменяем индивидуальный сдвиг первого фото */
  }

  /* На мобилке кнопки без стекла, просто текст */
  .press__footer .glass-effect {
    background: none !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    border: none !important;
    padding: 0 !important;
  }

  /* Debt section mobile */
  .debt__tabs {
    flex-direction: column;
    align-items: flex-start;
    border-bottom: none;
  }

  .debt__tab {
    width: 100%;
    text-align: left;
    border-bottom: var(--border-width) solid var(--color-debt-border);
  }

  .debt__tab::after {
    bottom: calc(var(--border-width) * -1);
  }
}

@container debttable (max-width: 600px) {
  .debt__table-header {
    display: none;
    /* Прячем заголовки таблицы на мобилках */
  }

  .debt__table-row {
    flex-direction: column;
    gap: var(--space-8);
    padding: var(--space-16);
  }

  .debt__col--apt,
  .debt__col--amount {
    flex: auto;
    text-align: left;
  }
}
</style>
