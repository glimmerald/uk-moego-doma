<template>
  <div class="page-index">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero__video-wrapper">
        <video class="hero__video" src="/main_video.mp4" autoplay loop muted playsinline></video>
        <!-- Overlay to make text and header more readable -->
        <div class="hero__overlay"></div>
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

    <!-- Третья секция (Имиджевая)
    <section class="section-image" id="about">
      <div class="image-section__container">
        <div class="image-section__header">
          <h2 class="image-section__title">Философия комфорта</h2>
          <p class="image-section__text">
            Наш подход основан на абсолютном внимании к деталям. Мы верим, что качество жизни
            определяется мелочами, поэтому каждая зона в наших домах продумана до сантиметра.
          </p>
        </div>

        <div class="image-section__slider-wrapper">
          <CarouselCoverflow :slides="sliderImages" />
        </div>
      </div>
    </section>
    -->

    <!-- Четвертая секция (Преимущества - Аккордеон) -->
    <section class="section-advantages" id="advantages">
      <div class="advantages__container">
        <div class="advantages__header">
          <h2 class="advantages__section-title">В цифрах</h2>
          <div class="advantages__controls">
            <button class="slider-btn" @click="scrollAccordion(-1)">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
                  stroke-linejoin="round" />
              </svg>
            </button>
            <button class="slider-btn" @click="scrollAccordion(1)">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
                  stroke-linejoin="round" />
              </svg>
            </button>
          </div>
        </div>

        <div class="accordion-wrapper">
          <div class="accordion" ref="accordionRef" @pointerleave="deactivateItem">
            <div class="accordion__item" :class="{ 'is-active': activeAccordionIndex === index }"
              v-for="(adv, index) in advantagesList" :key="index" @pointermove="activateItem(index, $event)">
              <div class="accordion__bg">
                <img :src="adv.image" alt="" loading="lazy" />
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
          <!-- Колонка 1, Строка 1: Изображение -->
          <div class="news__image-container">
            <div v-for="(news, index) in newsList" :key="'img-' + index" class="news__image"
              :class="{ 'is-active': activeNewsIndex === index }">
              <img :src="news.image" alt="Новость" loading="lazy">
            </div>
          </div>

          <!-- Колонка 2, Строка 1: Список новостей -->
          <div class="news__list">
            <div class="news-list__item" v-for="(news, index) in newsList" :key="'item-' + index"
              :class="{ 'is-active': activeNewsIndex === index }" @mouseenter="onNewsHover(index)">
              <div class="news-list__date">{{ news.date }}</div>
              <h3 class="news-list__title">{{ news.title }}</h3>
            </div>
          </div>

          <!-- Колонка 1, Строка 2: Текст новости и кнопка -->
          <div class="news__content">
            <div v-for="(news, index) in newsList" :key="'text-' + index" class="news__excerpt"
              :class="{ 'is-active': activeNewsIndex === index }">
              <p>{{ news.excerpt }}</p>
              <NuxtLink to="#" class="btn-arrow">
                <span class="btn-arrow__text">Читать целиком</span>
                <span class="btn-arrow__icon">
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
            <NuxtLink to="#" class="news-list__view-all">Смотреть все новости (15)</NuxtLink>
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
              <img :src="press.image" alt="" class="press__image"
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
              <NuxtLink :to="press.link" class="press__link glass-effect">
                <span>Читать статью</span>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
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

        <div class="debt__tabs">
          <button
            class="debt__tab"
            v-for="city in debtRegistry"
            :key="city.id"
            :class="{ 'is-active': activeCityId === city.id }"
            @click="activeCityId = city.id"
          >
            {{ city.name }}
          </button>
        </div>

        <div class="debt__list" v-if="activeCity">
          
          <!-- Выпадающий список ЖК -->
          <div class="debt__complex-dropdown">
            <div class="debt__dropdown-header" @click="isComplexDropdownOpen = !isComplexDropdownOpen">
              <span class="debt__dropdown-title">
                {{ activeComplex ? activeComplex.name : 'Выберите жилой комплекс...' }}
              </span>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" class="debt__dropdown-icon" :class="{ 'is-rotated': isComplexDropdownOpen }">
                <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
            </div>
            
            <Transition name="fade">
              <div class="debt__dropdown-options" v-if="isComplexDropdownOpen">
                <div class="debt__dropdown-option" 
                     v-for="complex in activeCity.complexes" :key="complex.id"
                     @click="selectComplex(complex)">
                  <span class="debt__option-name">{{ complex.name }}</span>
                  <span class="debt__option-address" v-if="complex.address">{{ complex.address }}</span>
                </div>
              </div>
            </Transition>
          </div>

          <Transition name="fade">
            <div class="debt__complex-content" v-if="activeComplex">
              <div class="debt__building-list">
                            <div class="debt__building" v-for="building in activeComplex.buildings" :key="building.id"
                              :class="{ 'is-open': building.isOpen }">
                              <div class="debt__building-header" @click="toggleBuilding(building)">
                                <h4 class="debt__building-name">{{ building.name }}</h4>
                                <div class="debt__building-icon">
                                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                                    <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="icon-plus" />
                                  </svg>
                                </div>
                              </div>

                              <!-- Тело аккордеона Корпуса -->
                              <div class="debt__building-body-wrapper">
                                <div class="debt__building-body">
                                  <div class="debt__building-body-content">

                                    <!-- Поиск внутри конкретного корпуса -->
                                    <div class="debt__search-wrapper">
                                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
                                        class="debt__search-icon">
                                        <path
                                          d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z"
                                          stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
                                          stroke-linejoin="round" />
                                      </svg>
                                      <input type="number" inputmode="numeric" v-model="building.searchQuery"
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
import { ref } from 'vue'

const accordionRef = ref(null)
const activeAccordionIndex = ref(null)
let scrollLock = false

const activateItem = (index, event) => {
  if (scrollLock) return
  if (activeAccordionIndex.value === index) return

  activeAccordionIndex.value = index

  if (!accordionRef.value) return

  const el = event.currentTarget
  const rect = el.getBoundingClientRect()
  const containerRect = accordionRef.value.getBoundingClientRect()

  const elLeft = rect.left - containerRect.left
  const expandedWidth = 640
  const paddingRight = 40

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
  activeAccordionIndex.value = null
}

const scrollAccordion = (direction) => {
  if (accordionRef.value) {
    const scrollAmount = 350;
    accordionRef.value.scrollBy({ left: direction * scrollAmount, behavior: 'smooth' });
  }
}

const sliderImages = [
  '/optimized/Фасад/DSC05127.webp',
  '/optimized/Фасад/DSC04986.webp',
  '/optimized/Фасад/DSC05052.webp',
  '/optimized/Фасад/DSC04826.webp',
  '/optimized/Фасад/DSC04824.webp',
  '/optimized/Фасад/DSC04402.webp'
]

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
const onNewsHover = (index) => {
  activeNewsIndex.value = index
}

const newsList = [
  {
    date: '14 / 09',
    title: 'Старт продаж в новом клубном доме на набережной',
    excerpt: 'Уникальные видовые квартиры с террасами и собственным выходом к воде. Узнайте первыми о специальных условиях на старте.',
    image: '/optimized/Фасад/DSC05045.webp'
  },
  {
    date: '28 / 08',
    title: 'Завершение монолитных работ в ЖК «Авангард»',
    excerpt: 'Мы идем с опережением графика на 2 месяца. Строители приступили к остеклению фасадов и монтажу инженерных систем.',
    image: '/optimized/Фасад/DSC04984.webp'
  },
  {
    date: '12 / 08',
    title: 'Новые стандарты благоустройства внутренних дворов',
    excerpt: 'Ландшафтный дизайн от мировых бюро, всесезонные растения и зонирование для всех возрастов.',
    image: '/optimized/Фасад/DSC05455.webp'
  },
  {
    date: '03 / 08',
    title: 'Наш проект получил премию Urban Awards 2024',
    excerpt: 'Жюри высоко оценило архитектурный облик и концепцию инфраструктуры нашего флагманского проекта.',
    image: '/optimized/Фасад/DSC04993.webp'
  },
  {
    date: '18 / 07',
    title: 'Открытие премиального фитнес-клуба для резидентов',
    excerpt: 'Бассейн 25 метров, SPA-зона и новейшее оборудование. Доступ только для жителей комплекса по индивидуальной ключ-карте.',
    image: '/optimized/Фасад/DSC05046.webp'
  }
]

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

import { onMounted, onUnmounted, computed, nextTick } from 'vue'
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

import { watch } from 'vue'
watch(activeCityId, () => {
  activeComplexId.value = null
  isComplexDropdownOpen.value = false
})


const toggleCity = (city) => {
  city.isOpen = !city.isOpen
}

const toggleComplex = (complex) => {
  complex.isOpen = !complex.isOpen
}

const toggleBuilding = (building) => {
  building.isOpen = !building.isOpen
}

const getFilteredDebtors = (building) => {
  if (!building.searchQuery) return building.debtors
  return building.debtors.filter(d => d.apt.includes(building.searchQuery))
}

// Эффект "фонарика" (spotlight reveal) при наведении на блок
const onPressMouseMove = (e) => {
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


onMounted(() => {
  nextTick(() => {
    // 1. Hero Animation
    const heroTl = gsap.timeline();
    heroTl.fromTo('.hero__title-line', 
      { y: 50, opacity: 0 }, 
      { y: 0, opacity: 1, duration: 1, stagger: 0.2, ease: 'power3.out' }
    ).fromTo('.hero__subtitle', 
      { y: 20, opacity: 0 }, 
      { y: 0, opacity: 0.9, duration: 1, ease: 'power2.out' }, 
      "-=0.5"
    );

    // 2. Dispatch Section Parallax
    ScrollTrigger.matchMedia({
      "(min-width: 1025px)": function() {
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
          });
        });
      }
    });

    // 3. Press Section Parallax (О нас пишут)
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

    // 4. Reveal items (News, Press, Dispatch photos)
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
})

onUnmounted(() => {
  ScrollTrigger.getAll().forEach(t => t.kill());
})
</script>

<style scoped>
.page-index {
  /* No special styles for the page wrapper yet */
}

.hero {
  position: relative;
  width: 100%;
  height: var(--vh-70);
  min-height: var(--accordion-height-mobile);
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
  background-color: var(--color-white);
}

.hero__video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero__overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom,
      var(--color-overlay) 0%,
      var(--color-header-border) var(--percent-40),
      var(--color-overlay) 100%);
  z-index: var(--z-above);
}

.hero__content {
  position: relative;
  z-index: var(--z-top);
  text-align: center;
  padding: 0 var(--space-40);
  margin-top: var(--space-80);
  /* offset for header */
}

.hero__title {
  font-size: var(--text-hero);
  font-weight: var(--font-weight-light);
  line-height: var(--line-height-hero);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
  margin-bottom: var(--space-32);
  display: flex;
  flex-direction: column;
}

.hero__title-line {
  display: block;
}

.hero__subtitle {
  font-size: var(--text-body-lg);
  font-weight: var(--font-weight-light);
  letter-spacing: var(--letter-spacing-widest);
  opacity: 0.9;
  max-width: var(--max-width-text);
  margin: 0 auto;
}

.hero__scroll-indicator {
  position: absolute;
  bottom: var(--space-40);
  left: var(--percent-50);
  transform: translateX(var(--translate-half-neg));
  z-index: var(--z-top);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-16);
  opacity: 0.8;
}

.hero__scroll-text {
  font-size: var(--text-micro);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-uppercase);
}

.hero__scroll-line {
  width: var(--border-width);
  height: var(--space-60);
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
  .hero__title {
    font-size: var(--space-60);
  }
}

@media (max-width: 768px) {
  .hero__title {
    font-size: var(--space-40);
  }

  .hero__subtitle {
    font-size: var(--text-body-sm);
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
  gap: var(--space-80);
}

.projects__title {
  font-size: var(--text-h1);
  font-weight: var(--font-weight-light);
  line-height: var(--line-height-hero);
  margin-bottom: var(--space-40);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
}

.projects__description {
  font-size: var(--text-body-lg);
  font-weight: var(--font-weight-light);
  line-height: var(--line-height-loose);
  color: var(--color-text);
  max-width: var(--max-width-text);
  margin-top: var(--space-16);
  /* Небольшое выравнивание относительно заголовка */
}

/* Стили для кнопки-ссылки */
.btn-arrow {
  display: inline-flex;
  align-items: center;
  gap: var(--space-16);
  font-size: var(--text-caption);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-widest);
  color: var(--color-text);
  transition: opacity var(--anim-duration-fast) ease;
}

.btn-arrow:hover {
  opacity: 0.7;
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

.btn-arrow:hover .btn-arrow__icon {
  transform: translateX(var(--space-8));
  background-color: var(--color-text);
  color: var(--color-bg);
}

/* Адаптив */
@media (max-width: 1024px) {
  .projects__container {
    grid-template-columns: 1fr;
    gap: var(--space-48);
  }

  .projects__title {
    font-size: var(--text-h3);
  }
}

@media (max-width: 768px) {
  .section-projects {
    padding: var(--space-80) 0;
  }

  .projects__title {
    font-size: var(--space-40);
  }

  .projects__description {
    font-size: var(--text-body-sm);
  }
}

/* Секция Имиджевая */
.section-image {
  padding: var(--space-140) 0;
  background-color: var(--color-bg-alt);
}

.image-section__container {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: 0 var(--space-40);
}

.image-section__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: var(--space-64);
  gap: var(--space-40);
}

.image-section__title {
  font-size: var(--text-h2);
  font-weight: var(--font-weight-light);
  line-height: var(--line-height-hero);
  text-transform: uppercase;
  flex: 1;
}

.image-section__text {
  flex: 1;
  font-size: var(--text-body);
  line-height: var(--line-height-loose);
  color: var(--color-text);
  max-width: var(--max-width-text);
}

.image-section__slider-wrapper {
  width: 100%;
  margin-top: var(--space-40);
}

@media (max-width: 1024px) {
  .image-section__header {
    flex-direction: column;
    align-items: flex-start;
  }

  .image-section__title {
    font-size: var(--space-40);
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
  /* Убираем правый паддинг, чтобы слайдер уходил в край экрана */
  padding-left: var(--space-40);
}

.advantages__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
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

.slider-btn:hover {
  background-color: var(--color-text);
  color: var(--color-bg);
}

.accordion-wrapper {
  position: relative;
  width: 100%;
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
  padding-right: var(--space-40);
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
  opacity: 0.15;
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
  transform: translateY(-var(--space-10));
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
  .accordion__item {
    width: var(--accordion-item-width-tablet);
  }

  .accordion__item.is-active {
    width: 100%;
  }

  .accordion__text-wrapper {
    width: var(--accordion-item-width);
  }
}

@media (max-width: 768px) {
  .accordion {
    height: var(--accordion-height-mobile);
  }

  .accordion__item {
    width: var(--accordion-item-width-mobile);
  }

  .accordion__item.is-active {
    width: var(--vw-85);
  }

  .accordion__number {
    font-size: var(--space-60);
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

.dispatch__right {
  width: var(--press-item-2-width);
  display: flex;
  flex-direction: column;
  padding: var(--space-140) var(--space-40) var(--space-140) 0;
  gap: var(--space-120);
}

.dispatch__photo {
  width: 100%;
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

/* Асимметрия: сдвигаем четные фотки чуть влево для журнального вида */
.dispatch__photo--offset {
  width: var(--dispatch-photo-offset-width);
  margin-left: var(--dispatch-photo-offset-margin);
  aspect-ratio: var(--aspect-ratio-3-4);
}

.dispatch__photo img {
  width: var(--percent-100, 100%);
  height: var(--percent-100, 100%);
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

  .dispatch__huge-text {
    font-size: var(--space-120);
  }

  .dispatch__right {
    width: 100%;
    padding: 0 var(--space-40) var(--space-100) var(--space-40);
    gap: var(--space-60);
  }

  .dispatch__photo--offset {
    width: var(--dispatch-photo-offset-mobile-width);
    margin-left: var(--dispatch-photo-offset-mobile-margin);
  }
}

@media (max-width: 768px) {
  .dispatch__huge-text {
    font-size: var(--text-hero);
  }

  .dispatch__title {
    font-size: var(--text-h5);
  }

  .dispatch__description {
    font-size: var(--text-body-sm);
  }
}

/* Секция Новости (Editorial List) */
.section-news {
  padding: var(--space-140) 0;
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
  margin-bottom: var(--space-40);
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
  height: var(--space-160);
  padding-top: var(--space-40);
  /* Отступ от картинки до текста */
}

.news__excerpt {
  position: absolute;
  top: var(--space-40);
  /* Совпадает с padding-top */
  left: 0;
  width: 100%;
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--anim-duration-normal) ease, transform var(--anim-duration-normal) ease;
  transform: translateY(var(--space-10));
}

.news__excerpt.is-active {
  opacity: 1;
  pointer-events: auto;
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
  align-items: center;
  padding: var(--space-48) 0;
  border-top: var(--border-width) solid var(--color-border);
  border-bottom: var(--border-width) solid var(--color-border);
  margin-top: -var(--border-width);
  /* Схлопываем двойные границы */
  cursor: pointer;
  transition: border-color var(--anim-duration-normal) ease;
  z-index: var(--z-base);
}

.news-list__item:first-child {
  margin-top: 0;
}

.news-list__date {
  font-size: var(--text-h5);
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
  transition: transform var(--anim-duration-normal) var(--anim-easing-smooth), color var(--anim-duration-normal) ease;
}

.news-list__item:hover,
.news-list__item.is-active {
  border-color: var(--color-text);
  z-index: var(--z-above);
  /* Чтобы активные границы были поверх соседних */
}

.news-list__item:hover .news-list__date,
.news-list__item.is-active .news-list__date {
  color: var(--color-text);
}

.news-list__item:hover .news-list__title,
.news-list__item.is-active .news-list__title {
  transform: translateX(var(--space-16));
}

.news-list__footer {
  display: flex;
  align-items: center;
  /* Центрируем по вертикали */
  justify-content: flex-start;
  height: var(--space-160);
  /* Высота равна левому блоку */
  border-bottom: var(--border-width) solid var(--color-border);
  /* Нижняя граница, о которой просили */
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
  opacity: 0.6;
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
}

.press__item:nth-child(3) {
  width: var(--press-item-3-width);
  align-self: flex-start;
  margin-left: var(--dispatch-photo-offset-margin);
}

.press__item:nth-child(4) {
  width: var(--press-item-4-width);
  align-self: flex-end;
  margin-right: var(--press-item-4-margin);
}

.press__item:nth-child(5) {
  width: var(--press-item-5-width);
  align-self: center;
}

/* Огромная фоновая кавычка (как в первой идее) */
.press__item::before {
  z-index: 1;
  content: '“';
  position: absolute;
  top: -var(--space-80);
  left: -var(--space-60);
  font-size: var(--press-quote-bg-size);
  line-height: var(--line-height-none);
  font-family: var(--font-family-serif);
  /* Классическая кавычка с засечками */
  color: var(--color-border);
  opacity: 0.5;
  z-index: 0;
  pointer-events: none;
  transition: opacity var(--anim-duration-medium) ease;
}

.press__quote {
  position: relative;
  z-index: var(--z-base);
  font-size: calc(var(--text-h4) / 1.75);
  font-weight: var(--font-weight-light);
  line-height: var(--line-height-base);
  margin-bottom: var(--space-40);
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
  transform: translateY(var(--translate-full));
  opacity: 0;
  transition: transform var(--anim-duration-slower) var(--anim-easing-smooth), opacity var(--anim-duration-slower) ease;
}

/* Когда родитель получает .is-revealed, слова поднимаются */
.press__item.is-revealed .press__word {
  transform: translateY(0);
  opacity: 1;
}

.press__footer {
  position: relative;
  z-index: var(--z-base);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: var(--space-24);
  border-top: var(--border-width) solid var(--color-border);
}

.press__source {
  font-size: var(--text-subtitle);
  font-weight: var(--font-weight-regular);
  font-family: var(--font-family-serif);
  letter-spacing: var(--letter-spacing-wide);
  padding: var(--space-16) var(--space-24);
}

.press__link {
  display: flex;
  align-items: center;
  gap: var(--space-12);
  font-size: var(--text-body-sm);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-widest);
  color: var(--color-text);

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
  z-index: 0;
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
  opacity: 0.95;
}

/* Приглушаем фоновую кавычку при наведении, но оставляем легкий силуэт */
.press__item:hover::before {
  opacity: 0.15;
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
  gap: var(--space-40);
  margin-bottom: var(--space-60);
  border-bottom: var(--border-width) solid var(--color-debt-border);
}

.debt__tab {
  font-size: var(--text-h5);
  font-weight: var(--font-weight-regular);
  color: var(--color-gray-400);
  padding-bottom: var(--space-16);
  position: relative;
  transition: color var(--anim-duration-fast) ease;
}

.debt__tab:hover,
.debt__tab.is-active {
  color: var(--color-black);
}

.debt__tab.is-active::after {
  content: '';
  position: absolute;
  bottom: calc(var(--border-width) * -1);
  left: 0;
  width: 100%;
  height: calc(var(--border-width) * 2);
  background-color: var(--color-black);
}

.debt__list {
  display: flex;
  flex-direction: column;
}


.debt__complex-dropdown {
  position: relative;
  margin-bottom: var(--space-40);
  z-index: 10;
}

.debt__dropdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-24) 0;
  border-bottom: var(--border-width) solid var(--color-black);
  cursor: pointer;
  transition: opacity var(--anim-duration-fast) ease;
}

.debt__dropdown-header:hover {
  opacity: 0.7;
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

.debt__dropdown-option:hover {
  background-color: var(--color-debt-hover);
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

  .news__image-container {
    height: var(--news-image-height-mobile);
  }

  .news-list__date {
    font-size: var(--text-subtitle);
    width: var(--space-100);
  }

  .news-list__title {
    font-size: var(--text-body-lg);
  }

  .press__item:nth-child(n) {
    width: 100%;
    margin-left: 0;
    margin-right: 0;
    align-self: flex-start;
  }

  .press__quote {
    position: relative;
    z-index: 1;
    font-size: var(--text-subtitle);
  }

  .press__list {
    gap: var(--space-80);
  }

  .press__item::before {
    z-index: 1;
    font-size: var(--space-140);
    top: -var(--space-40);
    left: -var(--space-20);
  }

  /* Debt section mobile */
  .debt__header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-16);
  }

  .debt__icon {
    position: absolute;
    right: 0;
    top: var(--space-40);
  }

  .debt__complex {
    position: relative;
  }

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
