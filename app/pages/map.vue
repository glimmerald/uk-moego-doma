<template>
  <div class="map-page">
    
    <!-- Информационная панель (Стекло) -->
    <div class="map-sidebar glass-effect">
      <Transition 
        @before-leave="onSidebarBeforeLeave"
        @leave="onSidebarLeave"
        @before-enter="onSidebarBeforeEnter"
        @enter="onSidebarEnter"
        :css="false"
        mode="out-in"
      >
        <!-- Состояние 1: Планета -->
        <div v-if="!isDived" class="sidebar-content" key="planet">
          <h1 class="sidebar-title">Наши ЖК</h1>
          <p class="sidebar-desc">
            Подробная информация о жилых комплексах, находящихся под нашим управлением. Выберите город на карте или в списке ниже, чтобы изучить объекты.
          </p>
          <div class="sidebar-cities">
            <button 
              v-for="city in cities" 
              :key="city.id" 
              type="button"
              class="sidebar-city-btn"
              :aria-label="'Выбрать город ' + city.name + ', объектов: ' + city.complexes.length"
              @mouseenter="prewarmCity(city)"
              @click="diveTo(city.id)"
            >
              {{ city.name }}
              <span class="city-badge">{{ city.complexes.length }}</span>
            </button>
          </div>
        </div>

        <!-- Состояние 2: Город -->
        <div v-else class="sidebar-content sidebar-content--city" key="city">
          <button type="button" class="sidebar-back-btn" aria-label="Вернуться к списку городов" @click="returnToPlanet()">
            &larr; Вернуться к списку городов
          </button>
          <h1 class="sidebar-title">{{ activeCity?.name }}</h1>
          <div class="complex-directory">
            <div class="complex-directory__header">
              <div class="stat-val">{{ activeCity?.complexes.length }}</div>
              <div class="stat-label">Жилых комплексов</div>
            </div>
            
            <div class="sidebar-complex-list">
              <div 
                v-for="complex in activeCity?.complexes" 
                :key="complex.id"
                class="complex-list-item"
                :data-id="complex.id"
                :class="{ 
                  'is-active': activeComplexId === complex.id,
                  'is-hovered': hoveredComplexId === complex.id
                }"
                role="button"
                tabindex="0"
                :aria-expanded="activeComplexId === complex.id"
                :aria-label="complex.name + ', ' + complex.address"
                @mouseenter="hoverComplex(complex.id)"
                @mouseleave="unhoverComplex()"
                @click="toggleComplex(complex.id)"
                @keydown.enter.prevent="toggleComplex(complex.id)"
                @keydown.space.prevent="toggleComplex(complex.id)"
              >
                <div class="complex-list-item__header">
                  <img 
                    v-if="complex.image" 
                    :src="complex.image" 
                    :alt="complex.name"
                    class="complex-list-item__thumb" 
                    loading="lazy" 
                    decoding="async" 
                  />
                  <div class="complex-list-item__info">
                    <h3 class="complex-list-item__title">{{ complex.name }}</h3>
                    <p class="complex-list-item__address">{{ complex.address }}</p>
                  </div>
                </div>
                <div class="complex-list-item__body">
                  <div class="complex-list-item__body-content">
                    <p class="complex-list-item__desc">{{ complex.description || 'Рыбная информация об этом ЖК. Здесь будет располагаться подробное описание инфраструктуры, преимуществ и особенностей жилого комплекса.' }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </div>

    <div class="map-container" id="map" ref="mapContainer"></div>

    
    <!-- Тултип конкретного ЖК -->
    <Transition name="fade">
      <div 
        v-if="hoveredComplex && isDived" 
        class="map-tooltip glass-effect"
        :style="{ left: tooltipX + 'px', top: tooltipY + 'px' }"
      >
        <div class="complex-card">
          <img 
            v-if="hoveredComplex.image" 
            :src="hoveredComplex.image" 
            :alt="hoveredComplex.name"
            class="complex-card__image" 
            loading="lazy" 
            decoding="async" 
          />
          <div class="complex-card__info">
            <h3 class="complex-card__title">{{ hoveredComplex.name }}</h3>
            <p class="complex-card__address">{{ hoveredComplex.address }}</p>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Тултип города -->
    <Transition name="fade">
      <div 
        v-if="hoveredCity"
        class="map-tooltip glass-effect"
        :style="{ top: tooltipY + 'px', left: tooltipX + 'px' }"
      >
        <div class="map-tooltip__header">{{ hoveredCity.name }}</div>
        <div class="map-tooltip__count">Количество объектов: {{ hoveredCity.complexes.length }}</div>
        <ul class="map-tooltip__list">
          <li v-for="(complex, i) in hoveredCity.complexes" :key="i">
            {{ complex.name }}
          </li>
        </ul>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from '#app'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import gsap from 'gsap'

// --- GSAP Hooks for Sidebar Smooth Height Transition ---
const onSidebarBeforeLeave = (el) => {
  if (typeof window !== 'undefined' && window.innerWidth <= 768) return
  const parent = el.parentElement
  if (!parent) return
  // Freeze parent height to prevent snapping to 0 when element unmounts (Desktop only)
  parent.style.height = `${parent.offsetHeight}px`
  parent.style.overflow = 'hidden'
}

const onSidebarLeave = (el, done) => {
  gsap.to(el, {
    opacity: 0,
    y: -8,
    duration: 0.2,
    ease: 'power2.in',
    onComplete: done
  })
}

const onSidebarBeforeEnter = (el) => {
  el.style.opacity = 0
  el.style.transform = 'translateY(8px)'
}

const onSidebarEnter = (el, done) => {
  const isMobile = typeof window !== 'undefined' && window.innerWidth <= 768
  const parent = el.parentElement
  if (!parent || isMobile) {
    // На мобильных устройствах избегаем layout-пересчетов высоты во время полета камеры WebGL
    gsap.to(el, {
      opacity: 1,
      y: 0,
      duration: 0.25,
      ease: 'power2.out',
      onComplete: done
    })
    return
  }
  
  // 1. Remember the frozen height
  const startHeight = parent.offsetHeight
  
  // 2. Remove height temporarily so it expands to fit the new content
  parent.style.height = 'auto'
  
  // 3. Measure the natural height with the new content
  const targetHeight = parent.offsetHeight
  
  // 4. Reset to frozen height for the start of the animation
  parent.style.height = `${startHeight}px`
  
  // 5. Animate parent height
  gsap.to(parent, {
    height: targetHeight,
    duration: 0.35,
    ease: 'power2.out',
    onComplete: () => {
      parent.style.height = '' // Clear explicit height after animation
      parent.style.overflow = ''
    }
  })
  
  // 6. Animate content in
  gsap.to(el, {
    opacity: 1,
    y: 0,
    duration: 0.35,
    ease: 'power2.out',
    onComplete: done
  })
}
// -----------------------------------------------------

const mapContainer = ref(null)
let map = null
let pulseAnimationId = null
let pulseFrame = 0

// Управление циклом пульсации WebGL точек (останавливается во время полетов и в городе)
const startPulse = () => {
  if (pulseAnimationId || isDived.value || !map) return
  const loop = () => {
    if (!map || isDived.value) {
      pulseAnimationId = null
      return
    }
    pulseFrame = (pulseFrame + 1) % 240
    const progress = pulseFrame / 240
    const radius = 5 + progress * 12.5
    const opacity = 0.8 * (1 - progress)

    if (map.getLayer('city-pulse')) {
      map.setPaintProperty('city-pulse', 'circle-radius', radius)
      map.setPaintProperty('city-pulse', 'circle-opacity', opacity)
    }
    pulseAnimationId = requestAnimationFrame(loop)
  }
  pulseAnimationId = requestAnimationFrame(loop)
}

const stopPulse = () => {
  if (pulseAnimationId) {
    cancelAnimationFrame(pulseAnimationId)
    pulseAnimationId = null
  }
}

const isDived = ref(false)
const activeCity = ref(null)
const activeComplexId = ref(null)
const hoveredComplexId = ref(null)

const hoveredCity = ref(null)
const hoveredComplex = ref(null)
const tooltipX = ref(0)
const tooltipY = ref(0)

let complexMarkers = []
let markers = []

const route = useRoute()
const router = useRouter()

// Данные городов с реальными координатами [lng, lat]
import cities from '~/data/cities.json'

// Предварительный прогрев сетевых ресурсов для города при наведении курсора
const prewarmedCities = new Set()
const prewarmCity = (city) => {
  if (!city || prewarmedCities.has(city.id)) return
  prewarmedCities.add(city.id)

  if (city.complexes && Array.isArray(city.complexes)) {
    city.complexes.forEach(c => {
      if (c.image) {
        const img = new Image()
        img.decoding = 'async'
        img.src = c.image
      }
    })
  }
}

watch(() => route.hash, (newHash) => {
  if (newHash) {
    const cityId = newHash.replace('#', '')
    if (cityId !== activeCity.value?.id) {
      diveTo(cityId)
    }
  } else if (isDived.value) {
    returnToPlanet()
  }
})

// Синхронизация визуальных классов маркеров на карте с состоянием активности и ховера
const updateMarkerClasses = () => {
  complexMarkers.forEach(m => {
    if (!m.marker) return
    const el = m.marker.getElement()
    if (m.complex.id === activeComplexId.value) {
      el.classList.add('is-active')
      el.classList.remove('is-hovered')
    } else if (m.complex.id === hoveredComplexId.value) {
      el.classList.remove('is-active')
      el.classList.add('is-hovered')
    } else {
      el.classList.remove('is-active')
      el.classList.remove('is-hovered')
    }
  })
}

// Функция активации ховера ЖК
const hoverComplex = (complexId) => {
  hoveredComplexId.value = complexId
  updateMarkerClasses()
}

// Деактивация ховера ЖК
const unhoverComplex = () => {
  hoveredComplexId.value = null
  updateMarkerClasses()
}

// Клик активирует карточку, разворачивает описание и центрирует камеру с учетом паддинга
const toggleComplex = (complexId) => {
  // Если карточка уже активна — закрываем ее и возвращаемся к масштабу города
  if (activeComplexId.value === complexId) {
    activeComplexId.value = null
    hoveredComplex.value = null
    updateMarkerClasses()
    if (activeCity.value && map) {
      map.flyTo({
        center: getCityCenter(activeCity.value),
        zoom: getCityZoom(activeCity.value),
        pitch: 0,
        fov: 36.87,
        padding: getCityPadding(),
        duration: 1500,
        essential: true
      })
    }
    return
  }

  // Если нажали на другой ЖК — раскрываем новую карточку и переносимся к ее точке
  activeComplexId.value = complexId
  hoveredComplex.value = null
  updateMarkerClasses()

  const complex = activeCity.value?.complexes.find(c => c.id === complexId)
  if (complex && map) {
    map.flyTo({
      center: complex.coordinates,
      zoom: 15.3,
      pitch: 48,
      fov: 54,
      padding: getCityPadding(),
      duration: 2000,
      essential: true
    })
  }

  scrollCardIntoView(complexId, 'nearest')
}

// Плавный скролл списка карточек к нужному ЖК без скролла всего окна/страницы браузера
const scrollCardIntoView = (complexId, align = 'center') => {
  nextTick(() => {
    const listEl = document.querySelector('.sidebar-complex-list')
    const cardEl = document.querySelector(`.complex-list-item[data-id="${complexId}"]`)
    if (!listEl || !cardEl) return

    const listRect = listEl.getBoundingClientRect()
    const cardRect = cardEl.getBoundingClientRect()

    if (align === 'center') {
      const targetOffset = (cardRect.top - listRect.top) + listEl.scrollTop - (listRect.height / 2) + (cardRect.height / 2)
      listEl.scrollTo({ top: Math.max(0, targetOffset), behavior: 'smooth' })
    } else {
      if (cardRect.top < listRect.top) {
        listEl.scrollTo({ top: listEl.scrollTop + (cardRect.top - listRect.top) - 16, behavior: 'smooth' })
      } else if (cardRect.bottom > listRect.bottom) {
        listEl.scrollTo({ top: listEl.scrollTop + (cardRect.bottom - listRect.bottom) + 16, behavior: 'smooth' })
      }
    }
  })
}

// Выбор ЖК по клику на точку на карте:
// закрывает ранее открытые карточки других ЖК, раскрывает карточку выбранного ЖК и переносит камеру к нему
const selectComplexFromMap = (complexId) => {
  activeComplexId.value = complexId
  hoveredComplex.value = null
  updateMarkerClasses()

  const complex = activeCity.value?.complexes.find(c => c.id === complexId)
  if (complex && map) {
    map.flyTo({
      center: complex.coordinates,
      zoom: 15.3,
      pitch: 48,
      fov: 54,
      padding: getCityPadding(),
      duration: 2000,
      essential: true
    })
  }

  scrollCardIntoView(complexId, 'center')
}

const getPlanetPadding = () => {
  if (typeof window === 'undefined') return { right: 0 }
  if (window.innerWidth > 768) {
    const sidebarWidth = Math.min(Math.max(320, window.innerWidth * 0.10 + 220), 480)
    return { right: Math.round(sidebarWidth + 40) }
  }
  return { bottom: Math.round(window.innerHeight * 0.52) }
}

const getCityPadding = () => {
  if (typeof window === 'undefined') return { right: 0, top: 0 }
  if (window.innerWidth > 768) {
    const sidebarWidth = Math.min(Math.max(320, window.innerWidth * 0.10 + 220), 480)
    const topOffset = Math.min(Math.round(window.innerHeight * 0.15), 180)
    return { right: Math.round(sidebarWidth + 40), top: topOffset }
  }
  return { bottom: Math.round(window.innerHeight * 0.52), top: 60 }
}

const getCityCenter = (city) => {
  if (!city) return [38.9753, 45.0355]
  if (typeof window !== 'undefined' && window.innerWidth <= 768) {
    if (city.id === 'krasnodar') {
      return [38.962, 45.061]
    }
    if (city.id === 'yablonovsky') {
      return [38.947, 44.988]
    }
    if (city.id === 'guryevsk') {
      return [20.619, 54.776]
    }
  }
  return city.coordinates
}

const getCityZoom = (city) => {
  if (typeof window === 'undefined') return 10.54
  const isMobile = window.innerWidth <= 768
  if (isMobile) {
    if (city?.id === 'krasnodar') {
      const w = window.innerWidth
      if (w <= 400) return 9.17
      if (w <= 480) return 9.25
      return 9.4
    }
    if (city?.id === 'yablonovsky') {
      return 11.0
    }
    if (city?.id === 'guryevsk') {
      return 11.0
    }
    return 10.0
  }
  return 10.54
}

const getPlanetCenter = () => {
  if (typeof window === 'undefined') return [33.5, 49.5]
  const w = window.innerWidth
  if (w >= 1600) return [36, 49.5]
  if (w >= 1200) return [33.5, 49.5]
  if (w > 768) return [31.5, 49.8]
  return [31, 50]
}

const getPlanetZoom = () => {
  if (typeof window === 'undefined') return 4.5
  const w = window.innerWidth
  if (w >= 1920) return 4.9
  if (w >= 1440) return 4.5
  if (w >= 1200) return 4.2
  if (w >= 960) return 3.85
  if (w > 768) return 3.7
  if (w > 480) return 3.6
  return 3.4
}

const getPlanetPitch = () => {
  if (typeof window === 'undefined') return 20
  return window.innerWidth > 768 ? 20 : 35
}

let diveTimer = null
let diveArrivalHandler = null
let returnToPlanetTimer = null
let initialFlyTimer = null

const cleanDiveArrival = () => {
  if (diveTimer) {
    clearTimeout(diveTimer)
    diveTimer = null
  }
  if (returnToPlanetTimer) {
    clearTimeout(returnToPlanetTimer)
    returnToPlanetTimer = null
  }
  if (diveArrivalHandler && map) {
    map.off('moveend', diveArrivalHandler)
    diveArrivalHandler = null
  }
}

// Функция возврата на общую планету
const returnToPlanet = () => {
  if (!map) return
  cleanDiveArrival()
  isDived.value = false
  activeCity.value = null
  activeComplexId.value = null
  hoveredComplexId.value = null
  hoveredComplex.value = null
  
  if (route.hash) {
    router.replace({ hash: '' })
  }

  // Немедленно убираем точки ЖК при начале обратного полета
  complexMarkers.forEach(m => m.marker.remove())
  complexMarkers = []

  // Прячем контуры всех городов
  cities.forEach(c => {
    if (map.getLayer(`${c.id}-fill`)) map.setPaintProperty(`${c.id}-fill`, 'fill-opacity', 0)
    if (map.getLayer(`${c.id}-border`)) map.setPaintProperty(`${c.id}-border`, 'line-opacity', 0)
  })

  // Возвращаем камеру на Россию по баллистической траектории
  map.flyTo({
    center: getPlanetCenter(),
    zoom: getPlanetZoom(),
    pitch: getPlanetPitch(),
    bearing: 0,
    fov: 36.87,
    padding: getPlanetPadding(),
    curve: 1.42,
    speed: 1.1,
    essential: true
  })

  // Через 1 секунду после начала обратного полета
  returnToPlanetTimer = setTimeout(() => {
    if (!map || isDived.value) return
    
    // Возвращаем глобусные точки и подписи
    if (map.getLayer('city-dot')) map.setPaintProperty('city-dot', 'circle-opacity', 1)
    if (map.getLayer('city-labels')) map.setPaintProperty('city-labels', 'text-opacity', 1)
    
    // Возвращаем HTML-хитбоксы
    document.querySelectorAll('.city-marker-hitbox').forEach(el => {
      el.style.pointerEvents = 'auto'
      el.style.opacity = '1'
    })

    // Возобновляем пульс на планете
    startPulse()
  }, 1000)
}

// Функция нырка в город
const diveTo = (cityId) => {
  if (activeCity.value?.id === cityId && isDived.value) return
  
  const city = cities.find(c => c.id === cityId)
  if (!city || !map) return
  
  cleanDiveArrival()
  stopPulse()

  // Если мы уже были в другом городе, нужно убрать его декорации и маркеры
  if (activeCity.value) {
    const prevId = activeCity.value.id
    if (map.getLayer(`${prevId}-fill`)) map.setPaintProperty(`${prevId}-fill`, 'fill-opacity', 0)
    if (map.getLayer(`${prevId}-border`)) map.setPaintProperty(`${prevId}-border`, 'line-opacity', 0)
    
    complexMarkers.forEach(m => m.marker.remove())
    complexMarkers = []
  }

  isDived.value = true
  activeCity.value = city
  activeComplexId.value = null
  hoveredComplexId.value = null
  hoveredComplex.value = null
  
  if (route.hash !== `#${cityId}`) {
    router.replace({ hash: `#${cityId}` })
  }

  // Сразу прячем глобусные элементы (точки, подписи, хитбоксы), чтобы они не летали по карте во время полета
  if (map.getLayer('city-dot')) map.setPaintProperty('city-dot', 'circle-opacity', 0)
  if (map.getLayer('city-pulse')) map.setPaintProperty('city-pulse', 'circle-opacity', 0)
  if (map.getLayer('city-labels')) map.setPaintProperty('city-labels', 'text-opacity', 0)
  document.querySelectorAll('.city-marker-hitbox').forEach(el => {
    el.style.pointerEvents = 'none'
    el.style.opacity = '0'
  })

  // 1. Полет камеры: естественная баллистическая кривая Van Wijk (без загрузки тайлов всей страны)
  map.flyTo({
    center: getCityCenter(city),
    zoom: getCityZoom(city),
    pitch: 0,
    bearing: 0,
    fov: 36.87,
    padding: getCityPadding(),
    curve: 1.42,
    speed: 1.1,
    essential: true
  })

  // 2. Обработчик прибытия камеры: появление контура и маркеров строго после приземления (исключает статтер)
  let arrived = false
  diveArrivalHandler = () => {
    if (arrived || !isDived.value || activeCity.value?.id !== city.id) return
    arrived = true
    cleanDiveArrival()

    // Плавно проявляем контур города
    if (map.getLayer(`${city.id}-fill`)) map.setPaintProperty(`${city.id}-fill`, 'fill-opacity', 1)
    if (map.getLayer(`${city.id}-border`)) map.setPaintProperty(`${city.id}-border`, 'line-opacity', 1)

    // Показываем точки ЖК ТОЛЬКО когда камера уже приземлилась в городе,
    // чтобы они не летали и не вызывали статтер во время движения камеры
    complexMarkers.forEach(m => m.marker.remove())
    complexMarkers = []

    city.complexes.forEach(complex => {
      if (!complex.coordinates) return
      
      const wrapper = document.createElement('div')
      wrapper.className = 'complex-marker-wrapper fade-in-marker'
      
      const el = document.createElement('div')
      el.className = 'complex-marker'
      
      wrapper.appendChild(el)
      
      wrapper.addEventListener('mouseenter', (e) => {
        hoveredComplex.value = complex
        updateComplexTooltipPosition(e)
        window.addEventListener('mousemove', updateComplexTooltipPosition)
        hoverComplex(complex.id)
      })

      wrapper.addEventListener('mouseleave', () => {
        hoveredComplex.value = null
        window.removeEventListener('mousemove', updateComplexTooltipPosition)
        unhoverComplex()
      })
      
      wrapper.setAttribute('role', 'button')
      wrapper.setAttribute('tabindex', '0')
      wrapper.setAttribute('aria-label', complex.name)

      wrapper.addEventListener('click', (e) => {
        e.stopPropagation()
        selectComplexFromMap(complex.id)
      })

      wrapper.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault()
          e.stopPropagation()
          selectComplexFromMap(complex.id)
        }
      })

      const marker = new mapboxgl.Marker({ 
        element: wrapper,
        anchor: 'center',
        pitchAlignment: 'map'
      })
        .setLngLat(complex.coordinates)
        .addTo(map)
        
      complexMarkers.push({ marker, complex })
    })

    updateMarkerClasses()
  }

  // Привязываем к нативному событию завершения полета
  map.once('moveend', diveArrivalHandler)

  // Страховочный таймер на случай непредвиденного прерывания события moveend
  diveTimer = setTimeout(diveArrivalHandler, 2600)
}

onMounted(() => {
  // Ваш личный ключ Mapbox
  mapboxgl.accessToken = 'pk.eyJ1Ijoiamsta3Jhc25vZGFyIiwiYSI6ImNtdThhdzYwbzBxMWEyeXM3ZDNnNGJoOTkifQ.kqIYZO0xU7inIoXFKFjpWQ'

  map = new mapboxgl.Map({
    container: 'map',
    style: {
      version: 8,
      glyphs: "mapbox://fonts/mapbox/{fontstack}/{range}.pbf",
      sources: {},
      layers: [
        {
          id: 'background',
          type: 'background',
          paint: {
            'background-color': '#f4f4f4'
          }
        }
      ]
    },
    projection: 'globe',
    minZoom: 1.5,
    zoom: getPlanetZoom(),
    center: getPlanetCenter(), 
    pitch: 0,
    
    // ЖЕСТКАЯ БЛОКИРОВКА ВСЕХ ВЗАИМОДЕЙСТВИЙ С КАРТОЙ
    interactive: false,
    maxTileCacheSize: 100
  })

  // В dev-режиме: клик по карте выводит координаты в консоль браузера для быстрой калибровки cities.json
  if (import.meta.dev) {
    map.on('click', (e) => {
      console.log(`[Geo Calibration] [${e.lngLat.lng.toFixed(6)}, ${e.lngLat.lat.toFixed(6)}]`)
    })
  }

  // Фикс рассинхронизации холста и авто-калибровка камеры при повороте устройства/ресайзе
  window.addEventListener('resize', handleResize)

  map.on('style.load', () => {
    map.setFog({
      'color': '#ffffff', 
      'high-color': '#ffffff', 
      'space-color': '#ffffff', 
      'star-intensity': 0 
    })
  })

  map.on('load', () => {
    // Источник: GeoJSON только с регионами РФ
    map.addSource('russia-regions-data', {
      type: 'geojson',
      data: '/russia.geojson'
    })

    // Идеальная заливка России, собранная из самих регионов (гарантирует 100% совпадение границ)
    map.addLayer({
      id: 'russia-fill',
      type: 'fill',
      source: 'russia-regions-data',
      paint: {
        'fill-color': '#eaeaea',
        'fill-opacity': 1
      }
    })

    // Подключаем стандартный векторный слой Mapbox для инфраструктуры (вода, дороги, здания)
    map.addSource('mapbox-streets-v8', {
      type: 'vector',
      url: 'mapbox://mapbox.mapbox-streets-v8'
    })

    // ОЗЕРА И ШИРОКИЕ РЕКИ (полигоны) - фильтруем ОКЕАНЫ, чтобы не было конфликта с береговой линией!
    map.addLayer({
      id: 'water-lakes',
      type: 'fill',
      source: 'mapbox-streets-v8',
      'source-layer': 'water',
      filter: ['!=', 'class', 'ocean'], // Исключаем океаны
      paint: {
        'fill-color': '#ffffff', // Вода будет белой, создавая нежный контраст с серой землей
        'fill-opacity': 0.7
      }
    })

    // РЕКИ И КАНАЛЫ (линии)
    map.addLayer({
      id: 'water-rivers',
      type: 'line',
      source: 'mapbox-streets-v8',
      'source-layer': 'waterway',
      paint: {
        'line-color': '#ffffff',
        'line-width': 1,
        'line-opacity': 0.7
      }
    })

    // ДОРОГИ
    map.addLayer({
      id: 'roads',
      type: 'line',
      source: 'mapbox-streets-v8',
      'source-layer': 'road',
      paint: {
        'line-color': '#ffffff',
        'line-width': [
          'interpolate',
          ['linear'],
          ['zoom'],
          10, 0.5,
          15, 2
        ],
        'line-opacity': [
          'interpolate',
          ['linear'],
          ['zoom'],
          8, 0,
          11, 0.5,
          15, 1
        ]
      }
    })

    // ФУНДАМЕНТЫ ЗДАНИЙ (2D-подложка контуров кварталов на земле)
    map.addLayer({
      id: '2d-buildings',
      source: 'mapbox-streets-v8',
      'source-layer': 'building',
      filter: ['!=', ['get', 'underground'], 'true'],
      type: 'fill',
      minzoom: 11,
      paint: {
        'fill-color': '#e0e0e0',
        'fill-opacity': 0.6
      }
    })

    // ЗДАНИЯ (3D)
    map.addLayer({
      id: '3d-buildings',
      source: 'mapbox-streets-v8',
      'source-layer': 'building',
      filter: ['!=', ['get', 'underground'], 'true'],
      type: 'fill-extrusion',
      minzoom: 11,
      paint: {
        'fill-extrusion-color': '#f2f2f2', // Чуть светлее земли (#eaeaea), чтобы здания слегка выделялись
        'fill-extrusion-height': [
          'interpolate',
          ['linear'],
          ['zoom'],
          11, 0,
          13, ['coalesce', ['get', 'height'], 15]
        ],
        'fill-extrusion-base': [
          'interpolate',
          ['linear'],
          ['zoom'],
          11, 0,
          13, ['coalesce', ['get', 'min_height'], 0]
        ],
        'fill-extrusion-opacity': 0.85
      }
    })

    // Единые границы регионов и страны
    map.addLayer({
      id: 'russia-regions',
      type: 'line',
      source: 'russia-regions-data',
      paint: {
        'line-color': 'rgba(0, 0, 0, 0.08)', // Более неяркий и деликатный цвет
        'line-width': 1.5, // Сделали потолще по просьбе
        'line-dasharray': [3, 3], // Чуть более разряженный пунктир для толстой линии
        'line-opacity': [
          'interpolate',
          ['linear'],
          ['zoom'],
          6, 1,    // До 6-го зума (вид всей страны) границы полностью видны
          9, 0     // К 9-му зуму (подлет к городу) границы плавно растворяются
        ]
      }
    })

    // ПРЕДЗАГРУЗКА КОНТУРОВ ВСЕХ ГОРОДОВ
    // Регистрируем GeoJSON и слои сразу с нулевой прозрачностью,
    // чтобы при клике на город не было сетевых запросов и перекомпиляции WebGL-шейдеров
    cities.forEach(c => {
      map.addSource(`${c.id}-data`, {
        type: 'geojson',
        data: `/${c.id}.geojson`
      })

      map.addLayer({
        id: `${c.id}-fill`,
        type: 'fill',
        source: `${c.id}-data`,
        paint: {
          'fill-color': 'rgba(0, 0, 0, 0.04)',
          'fill-opacity': 0,
          'fill-opacity-transition': { duration: 1000 }
        }
      })

      map.addLayer({
        id: `${c.id}-border`,
        type: 'line',
        source: `${c.id}-data`,
        paint: {
          'line-color': 'rgba(0, 0, 0, 0.3)',
          'line-width': 1.5,
          'line-opacity': 0,
          'line-opacity-transition': { duration: 1000 }
        }
      })
    })

    const citiesGeoJSON = {
      type: 'FeatureCollection',
      features: cities.map(c => ({
        type: 'Feature',
        geometry: { type: 'Point', coordinates: c.globeCoordinates || c.coordinates },
        properties: { id: c.id, name: c.name }
      }))
    }

    map.addSource('cities-data', {
      type: 'geojson',
      data: citiesGeoJSON
    })

    // Слой ПУЛЬСА (WebGL)
    map.addLayer({
      id: 'city-pulse',
      type: 'circle',
      source: 'cities-data',
      paint: {
        'circle-color': '#111111',
        'circle-radius': 5,
        'circle-opacity': 0.5,
        'circle-pitch-alignment': 'map' // Прибито к земле
      }
    })

    // Слой ТОЧКИ (WebGL)
    map.addLayer({
      id: 'city-dot',
      type: 'circle',
      source: 'cities-data',
      paint: {
        'circle-color': '#111111',
        'circle-radius': 5,
        'circle-pitch-alignment': 'map', // Прибито к земле
        'circle-opacity-transition': { duration: 1500 } // Добавили плавность
      }
    })

    // Слой ПОДПИСЕЙ (WebGL) - нативный Mapbox для избежания багов CSS позиционирования
    map.addLayer({
      id: 'city-labels',
      type: 'symbol',
      source: 'cities-data',
      layout: {
        'text-field': ['get', 'name'],
        'text-size': [
          'interpolate',
          ['linear'],
          ['zoom'],
          5, 14,    /* На общем плане (zoom 5) - обычный шрифт 14px */
          10.5, 32  /* При приближении города (zoom 10.5) - крупный акцентный шрифт 32px */
        ],
        'text-offset': [
          'match',
          ['get', 'id'],
          'krasnodar', ['literal', [0, -1.2]], // Сверху для Краснодара
          'yablonovsky', ['literal', [0, 1.2]], // Снизу для Яблоновского
          ['literal', [0, 1.2]] // По умолчанию снизу
        ],
        'text-anchor': [
          'match',
          ['get', 'id'],
          'krasnodar', 'bottom',
          'yablonovsky', 'top',
          'top'
        ],
        'text-allow-overlap': true // Разрешаем перекрытие, чтобы всегда было видно, так как мы вручную развели их
      },
      paint: {
        'text-color': '#111111',
        'text-halo-color': 'rgba(255,255,255,0.8)',
        'text-halo-width': 2,
        'text-opacity-transition': { duration: 1500 }
      }
    })

    // Запуск пульсации на общем виде
    startPulse()

    // Добавляем маркеры городов (ТОЛЬКО ДЛЯ ХОВЕРА И КЛИКА, БЕЗ ТЕКСТА)
    cities.forEach(city => {
      const el = document.createElement('div')
      el.className = 'city-marker-hitbox'

      el.addEventListener('click', () => {
        diveTo(city.id)
      })

      el.addEventListener('mouseenter', (e) => {
        hoveredCity.value = city
        prewarmCity(city)
        updateTooltipPosition(e)
        window.addEventListener('mousemove', updateTooltipPosition)
        // Подсвечиваем WebGL точку
        map.setPaintProperty('city-dot', 'circle-color', [
          'match', ['get', 'id'], city.id, '#111111', '#555555'
        ])
        map.setPaintProperty('city-dot', 'circle-radius', [
          'match', ['get', 'id'], city.id, 7, 5
        ])
      })

      el.addEventListener('mouseleave', () => {
        hoveredCity.value = null
        window.removeEventListener('mousemove', updateTooltipPosition)
        // Возвращаем цвет
        map.setPaintProperty('city-dot', 'circle-color', '#111111')
        map.setPaintProperty('city-dot', 'circle-radius', 5)
      })

      const marker = new mapboxgl.Marker({ 
        element: el,
        anchor: 'center',
        pitchAlignment: 'map'
      })
        .setLngLat(city.globeCoordinates || city.coordinates)
        .addTo(map)
        
      markers.push({ marker, city })
    })

    // Анимация входа или загрузка по хэшу
    initialFlyTimer = setTimeout(() => {
      if (!map) return
      let foundCity = false
      if (route.hash) {
        const cityId = route.hash.replace('#', '')
        if (cities.find(c => c.id === cityId)) {
          foundCity = true
          diveTo(cityId)
        }
      }
      
      if (!foundCity) {
        startPulse()
        map.flyTo({
          center: getPlanetCenter(),
          zoom: getPlanetZoom(),
          pitch: getPlanetPitch(),
          bearing: 0,
          fov: 36.87,
          padding: getPlanetPadding(),
          curve: 1.42,
          speed: 1.2,
          essential: true
        })
      }
    }, 500)
  })
})


let resizeTimer = null
const handleResize = () => {
  if (!map) return
  map.resize()
  clearTimeout(resizeTimer)
  resizeTimer = setTimeout(() => {
    if (!map) return
    if (!isDived.value) {
      map.easeTo({
        center: getPlanetCenter(),
        zoom: getPlanetZoom(),
        pitch: getPlanetPitch(),
        padding: getPlanetPadding(),
        duration: 300
      })
    } else if (activeCity.value) {
      const targetCoords = activeComplexId.value
        ? (complexMarkers.find(m => m.complex.id === activeComplexId.value)?.complex.coordinates || getCityCenter(activeCity.value))
        : getCityCenter(activeCity.value)
      map.easeTo({
        center: targetCoords,
        zoom: activeComplexId.value ? 15.3 : getCityZoom(activeCity.value),
        padding: getCityPadding(),
        duration: 300
      })
    }
  }, 200)
}

const updateComplexTooltipPosition = (event) => {
  tooltipX.value = event.clientX + 15
  tooltipY.value = event.clientY + 15
}

const updateTooltipPosition = (event) => {
  tooltipX.value = event.clientX + 15
  tooltipY.value = event.clientY + 15
}

onUnmounted(() => {
  stopPulse()
  cleanDiveArrival()
  if (initialFlyTimer) clearTimeout(initialFlyTimer)
  if (returnToPlanetTimer) clearTimeout(returnToPlanetTimer)
  if (resizeTimer) clearTimeout(resizeTimer)
  window.removeEventListener('resize', handleResize)
  markers.forEach(m => m.marker.remove())
  complexMarkers.forEach(m => m.marker.remove())
  if (map) map.remove()
  window.removeEventListener('mousemove', updateTooltipPosition)
  window.removeEventListener('mousemove', updateComplexTooltipPosition)
  map = null
})
</script>

<style scoped>
.map-page {
  width: 100%;
  height: var(--vh-100);
  position: relative;
  padding-top: var(--space-0); 
  background-color: var(--color-white);
}

.map-container {
  width: 100%;
  height: 100%;
}

/* Принудительно отключаем курсор-руку на самом глобусе */
:deep(.mapboxgl-canvas-container) {
  cursor: default !important;
}

/* Стили HTML-маркера (теперь только хитбокс для ховера и текст) */
:deep(.city-marker-hitbox) {
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: var(--space-30);
  height: var(--space-30);
}

:deep(.city-marker-hitbox)::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: var(--space-48);
  height: var(--space-48);
  transform: translate(-50%, -50%);
}


/* Плавающий Тултип */
.map-tooltip {
  position: fixed;
  z-index: var(--z-overlay);
  border: var(--border-width) solid var(--color-header-border);
  padding: var(--space-32);
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-card);
  pointer-events: none;
  transform: translateY(0);
}

.map-tooltip__header {
  font-size: var(--text-h5);
  font-weight: var(--font-weight-medium);
  color: var(--color-black);
  margin-bottom: var(--space-8);
}

.map-tooltip__count {
  font-size: var(--text-body-sm);
  color: var(--color-gray-400);
  margin-bottom: var(--space-20);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-widest);
}

.map-tooltip__list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: var(--space-12);
  padding: var(--space-0);
  margin: var(--space-0);
}

.map-tooltip__list li {
  font-size: var(--text-body);
  color: var(--color-gray-700);
  position: relative;
  padding-left: var(--space-16);
}

.map-tooltip__list li::before {
  content: '';
  position: absolute;
  left: var(--space-0);
  top: var(--space-8);
  width: var(--space-6);
  height: var(--space-6);
  border-radius: var(--radius-round);
  background-color: var(--color-gray-200);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--anim-duration-fast) var(--anim-easing-ease), transform var(--anim-duration-fast) var(--anim-easing-ease);
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(var(--space-6));
}
/* --- ИНФОРМАЦИОННАЯ ПАНЕЛЬ (SIDEBAR) --- */
.map-sidebar {
  position: absolute;
  top: var(--space-120);
  right: var(--space-40);
  width: var(--map-sidebar-width);
  max-height: calc(var(--vh-100) - var(--space-160));
  z-index: var(--z-overlay);
  border-radius: var(--radius-xl);
  padding: var(--space-48);
  display: flex;
  flex-direction: column;
  overflow: hidden; /* Убираем глобальный скролл */
  border: var(--border-width) solid var(--color-white-50);
  box-shadow: var(--shadow-sm);
}

.sidebar-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  max-height: calc(var(--vh-100) - var(--space-160) - var(--space-48) * 2); /* Вычитаем паддинги (48 * 2) */
}

.sidebar-title {
  font-size: var(--text-h2);
  font-weight: var(--font-weight-light);
  margin-bottom: var(--space-20);
  color: var(--color-black);
  letter-spacing: var(--letter-spacing-tight);
  flex-shrink: 0;
}

.sidebar-desc {
  font-size: var(--text-body-lg);
  line-height: var(--line-height-relaxed);
  color: var(--color-gray-700);
  margin-bottom: var(--space-40);
  font-weight: var(--font-weight-light);
  flex-shrink: 0;
}

.sidebar-cities {
  display: flex;
  flex-direction: column;
  gap: var(--space-16);
  overflow-y: auto;
  padding-right: var(--space-8);
  /* Без margin-right, чтобы не обрезать скроллбар */
  flex: 1;
}

.sidebar-cities::-webkit-scrollbar {
  width: var(--space-4);
}
.sidebar-cities::-webkit-scrollbar-track {
  background: transparent;
}
.sidebar-cities::-webkit-scrollbar-thumb {
  background: var(--color-gray-300);
  border-radius: var(--radius-pill);
}

.sidebar-city-btn {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: var(--sidebar-city-btn-padding);
  background: var(--color-white-50);
  border: var(--border-width) solid var(--color-white-80);
  border-radius: var(--radius-md);
  font-size: var(--text-subtitle);
  color: var(--color-black);
  font-weight: var(--font-weight-regular);
  transition: all var(--anim-duration-fast) ease;
  text-align: left;
}

.sidebar-city-btn:hover {
  background: var(--color-accordion-bg);
  box-shadow: var(--shadow-sm);
}

.sidebar-city-btn:focus-visible {
  outline: var(--border-width) solid var(--color-black);
  outline-offset: var(--space-2);
}

.city-badge {
  background: var(--color-black);
  color: var(--color-white);
  font-size: var(--text-small);
  padding: var(--space-8) var(--space-8);
  min-width: var(--badge-min-width);
  border-radius: var(--radius-pill);
  font-weight: var(--font-weight-medium);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: var(--line-height-none);
}

.sidebar-back-btn {
  align-self: flex-start;
  margin-bottom: var(--space-32);
  background: none;
  border: none;
  font-size: var(--text-body);
  color: var(--color-gray-500);
  cursor: pointer;
  padding: var(--space-0);
  transition: color var(--anim-duration-fast) var(--anim-easing-ease);
  flex-shrink: 0;
}

.sidebar-back-btn:hover {
  color: var(--color-black);
}

.sidebar-back-btn:focus-visible {
  outline: var(--border-width) solid var(--color-black);
  outline-offset: var(--space-2);
}

.complex-directory {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0; /* Важно для внутреннего скролла */
}

.complex-directory__header {
  display: flex;
  align-items: baseline;
  gap: var(--space-8);
  padding-bottom: var(--space-24);
  border-bottom: var(--border-width) solid var(--color-border);
  flex-shrink: 0;
}

.complex-directory__header .stat-val {
  font-size: var(--text-h4);
  font-weight: var(--font-weight-regular);
  color: var(--color-black);
}

.complex-directory__header .stat-label {
  font-size: var(--text-caption);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-widest);
  color: var(--color-gray-600);
}

:deep(.complex-marker-wrapper) {
  display: flex;
  justify-content: center;
  align-items: center;
  width: var(--space-16);
  height: var(--space-16);
  cursor: pointer;
  z-index: var(--z-top);
  pointer-events: auto;
}

:deep(.complex-marker-wrapper:focus-visible) {
  outline: var(--border-width) solid var(--color-black);
  outline-offset: var(--space-2);
  border-radius: var(--radius-round);
}

:deep(.complex-marker-wrapper)::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: var(--space-48);
  height: var(--space-48);
  transform: translate(-50%, -50%);
}

:deep(.complex-marker) {
  width: 100%;
  height: 100%;
  border-radius: var(--radius-round);
  background: var(--color-black);
  border: var(--border-width-thick) solid var(--color-white);
  box-shadow: inset 0 0 0 0 var(--color-glow-transparent), var(--shadow-sm);
  scale: 1;
  transition: 
    scale var(--anim-duration-medium) var(--anim-easing-smooth), 
    box-shadow var(--anim-duration-medium) var(--anim-easing-smooth), 
    background var(--anim-duration-medium) var(--anim-easing-smooth), 
    border-color var(--anim-duration-medium) var(--anim-easing-smooth);
  box-sizing: border-box;
}

:deep(.fade-in-marker) {
  animation: fadeInMarker var(--anim-duration-slower) ease-out forwards;
}

@keyframes fadeInMarker {
  from { opacity: 0; }
  to { opacity: 1; }
}

:deep(.complex-marker-wrapper:hover .complex-marker) {
  scale: 1.15;
  background: var(--color-glow-dim);
  border-color: var(--color-glow-base);
  box-shadow: inset 0 0 0 var(--space-2) var(--color-glow-base), var(--shadow-firefly-hover);
}

:deep(.complex-marker-wrapper:hover) {
  z-index: calc(var(--z-top) + 1);
}


.complex-card {
  display: flex;
  flex-direction: column;
  width: var(--space-400);
}
.complex-card__image {
  width: 100%;
  height: var(--space-200);
  object-fit: cover;
  border-radius: var(--space-4);
  margin-bottom: var(--space-16);
}
.complex-card__title {
  font-size: var(--text-h5);
  font-weight: var(--font-weight-medium);
  margin-bottom: var(--space-8);
  color: var(--color-black);
}
.complex-card__address {
  font-size: var(--text-body);
  color: var(--color-gray-600);
  margin-bottom: var(--space-8);
}

/* --- СПИСОК ЖК В ГОРОДЕ --- */
.sidebar-content--city {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.sidebar-complex-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-12);
  overflow-y: auto;
  
  /* Плавное растворение списка внизу (дорогой fade-эффект) */
  -webkit-mask-image: linear-gradient(to bottom, black 0%, black calc(100% - var(--space-64)), transparent 100%);
  mask-image: linear-gradient(to bottom, black 0%, black calc(100% - var(--space-64)), transparent 100%);
  
  /* Делаем огромные отступы для тени (т.к. у нее 50px blur) и компенсируем margin-ом.
     Так как родитель не имеет overflow: hidden, а самый верхний .map-sidebar имеет 48px padding,
     этот трюк идеально помещает тень в безопасную зону, не сдвигая сами карточки. */
  padding-left: var(--space-48);
  margin-left: calc(var(--space-48) * -1);
  padding-right: var(--space-48);
  margin-right: calc(var(--space-48) * -1);
  
  /* Вертикальные отступы */
  padding-top: var(--space-24); /* Увеличен для визуального выравнивания (компенсация line-height заголовка и тени карточки) */
  padding-bottom: var(--space-32);
  
  flex: 1;
}

.sidebar-complex-list::-webkit-scrollbar {
  width: var(--space-4);
}
.sidebar-complex-list::-webkit-scrollbar-track {
  background: transparent;
  margin-top: var(--space-24);
  margin-bottom: var(--space-16);
}
.sidebar-complex-list::-webkit-scrollbar-thumb {
  background: var(--color-gray-300);
  border-radius: var(--radius-pill);
}

.complex-list-item {
  background: var(--color-white);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--complex-item-padding);
  cursor: pointer;
  transition: border-color var(--anim-duration-fast) var(--anim-easing-ease), box-shadow var(--anim-duration-fast) var(--anim-easing-ease);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  flex-shrink: 0;
}

.complex-list-item:hover,
.complex-list-item.is-hovered {
  border-color: var(--color-gray-300);
}

.complex-list-item:focus-visible {
  outline: var(--border-width) solid var(--color-black);
  outline-offset: var(--space-2);
}

.complex-list-item.is-active {
  border-color: var(--color-black);
  box-shadow: var(--shadow-md);
}

.complex-list-item.is-active:hover {
  border-color: var(--color-black);
}

.complex-list-item__header {
  display: flex;
  gap: var(--space-16);
  align-items: center;
}

.complex-list-item__thumb {
  width: var(--complex-thumb-size);
  height: var(--complex-thumb-size);
  border-radius: var(--radius-sm);
  object-fit: cover;
  flex-shrink: 0;
}

.complex-list-item__info {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.complex-list-item__title {
  font-size: var(--text-body);
  font-weight: var(--font-weight-medium);
  color: var(--color-black);
}

.complex-list-item__address {
  font-size: var(--text-caption);
  color: var(--color-gray-500);
}

.complex-list-item__body {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows var(--anim-duration-medium) var(--anim-easing-smooth);
}

.complex-list-item.is-active .complex-list-item__body {
  grid-template-rows: 1fr;
}

.complex-list-item__body-content {
  overflow: hidden;
  font-size: var(--text-body-sm);
  color: var(--color-gray-700);
  line-height: var(--line-height-relaxed);
}

.complex-list-item__desc {
  padding-top: var(--space-16);
  margin: var(--space-0);
}

/* Маркеры на карте (активные состояния) */
:deep(.complex-marker-wrapper.is-hovered .complex-marker) {
  scale: 1.15;
  background: var(--color-glow-dim);
  border-color: var(--color-glow-base);
  box-shadow: inset 0 0 0 var(--space-2) var(--color-glow-base), var(--shadow-firefly-hover);
}

:deep(.complex-marker-wrapper.is-hovered) {
  z-index: calc(var(--z-top) + 1);
}

:deep(.complex-marker-wrapper.is-active .complex-marker),
:deep(.complex-marker-wrapper.is-active:hover .complex-marker) {
  scale: 1.15;
  background: var(--color-glow-base);
  border-color: var(--color-glow-base);
  box-shadow: inset 0 0 0 var(--space-2) var(--color-glow-base), var(--shadow-firefly-active);
}

:deep(.complex-marker-wrapper.is-active) {
  z-index: calc(var(--z-top) + 2);
}

@media (max-width: 768px) {
  .map-page {
    display: block; /* revert flex */
  }

  .map-container {
    position: absolute;
    top: var(--space-0);
    left: var(--space-0);
    width: 100%;
    height: 100%;
    flex-shrink: unset;
  }

  .map-sidebar {
    position: absolute;
    top: auto;
    bottom: var(--map-sheet-inset);
    left: var(--map-sheet-inset);
    right: var(--map-sheet-inset);
    max-width: var(--map-sheet-max-width);
    margin: var(--space-0) auto;
    width: auto;
    max-height: var(--map-sheet-max-height);
    border-radius: var(--radius-xl);
    padding: var(--map-sheet-padding);
    z-index: var(--z-overlay);
    border: var(--border-width) solid var(--color-white-50);
  }

  .sidebar-content {
    max-height: none;
    height: 100%;
  }

  .map-tooltip {
    display: none;
  }

  .sidebar-complex-list {
    padding-left: var(--map-sheet-padding);
    margin-left: calc(var(--map-sheet-padding) * -1);
    padding-right: var(--map-sheet-padding);
    margin-right: calc(var(--map-sheet-padding) * -1);
    padding-top: var(--map-sheet-padding);
    padding-bottom: var(--map-sheet-padding);
    -webkit-mask-image: linear-gradient(to bottom, black 0%, black calc(100% - var(--space-32)), transparent 100%);
    mask-image: linear-gradient(to bottom, black 0%, black calc(100% - var(--space-32)), transparent 100%);
  }
}
</style>
