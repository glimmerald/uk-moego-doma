<template>
  <div class="map-page">
    
    <!-- Информационная панель (Стекло) -->
    <div class="map-sidebar glass-effect">
      <Transition name="fade" mode="out-in">
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
              class="sidebar-city-btn"
              @click="diveTo(city.id)"
            >
              {{ city.name }}
              <span class="city-badge">{{ city.complexes.length }}</span>
            </button>
          </div>
        </div>

        <!-- Состояние 2: Город -->
        <div v-else class="sidebar-content sidebar-content--city" key="city">
          <button class="sidebar-back-btn" @click="returnToPlanet()">
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
                :class="{ 'is-active': activeComplexId === complex.id }"
                @mouseenter="hoverComplex(complex.id)"
                @mouseleave="unhoverComplex()"
                @click="toggleComplex(complex.id)"
              >
                <div class="complex-list-item__header">
                  <img v-if="complex.image" :src="complex.image" class="complex-list-item__thumb" />
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
          <img v-if="hoveredComplex.image" :src="hoveredComplex.image" class="complex-card__image" />
          <div class="complex-card__info">
            <h3 class="complex-card__title">{{ hoveredComplex.name }}</h3>
            <p class="complex-card__address">{{ hoveredComplex.address }}</p>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Тултип -->
    <Transition name="fade">
      <div 
        v-if="hoveredCity"
        class="map-tooltip glass-effect"
        :style="{ top: tooltipY + 'px', left: tooltipX + 'px' }"
      >
        <div class="map-tooltip__title">{{ hoveredCity.name }}</div>
        <div class="map-tooltip__subtitle">Количество объектов: {{ hoveredCity.complexes.length }}</div>
        <div class="map-tooltip__complexes">
          <div v-for="(complex, i) in hoveredCity.complexes" :key="i" class="map-tooltip__complex">
            {{ complex.name }}
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

const mapContainer = ref(null)
let map = null
const isDived = ref(false)
const activeCity = ref(null)
const activeComplexId = ref(null)

const hoveredCity = ref(null)
const hoveredComplex = ref(null)
const tooltipX = ref(0)
const tooltipY = ref(0)

let complexMarkers = []
let markers = []

// Данные городов с реальными координатами [lng, lat]
import cities from '~/data/cities.json'

// Функция активации ЖК (по ховеру)
const hoverComplex = (complexId) => {
  activeComplexId.value = complexId
  complexMarkers.forEach(m => {
    if (m.marker) {
      if (m.complex.id === complexId) {
        m.marker.getElement().classList.add('is-active')
      } else {
        m.marker.getElement().classList.remove('is-active')
      }
    }
  })
}

// Деактивация ЖК
const unhoverComplex = () => {
  activeComplexId.value = null
  complexMarkers.forEach(m => {
    if (m.marker) m.marker.getElement().classList.remove('is-active')
  })
}

// Клик теперь может, например, центрировать карту на ЖК
const toggleComplex = (complexId) => {
  const item = complexMarkers.find(m => m.complex.id === complexId)
  if (item && map) {
    map.flyTo({
      center: item.complex.coordinates,
      zoom: 14,
      pitch: 45,
      duration: 2000,
      essential: true
    })
  }
}

// Функция возврата на общую планету
const returnToPlanet = () => {
  if (!map) return
  isDived.value = false
  activeCity.value = null
  activeComplexId.value = null

  // Убираем точки ЖК
  complexMarkers.forEach(m => m.marker.remove())
  complexMarkers = []


  // Возвращаем камеру на Россию
  map.flyTo({
    center: [42, 48],
    zoom: 5.2,
    pitch: 20, // Возвращаем легкий наклон, как было при входе
    bearing: 0,
    padding: { right: 450 },
    duration: 3000,
    essential: true,
    easing: (t) => t * (2 - t)
  })

  // Через 1 секунду после начала обратного полета
  setTimeout(() => {
    // Прячем контур активного города
    cities.forEach(c => {
      if (map.getLayer(`${c.id}-fill`)) map.setPaintProperty(`${c.id}-fill`, 'fill-opacity', 0)
      if (map.getLayer(`${c.id}-border`)) map.setPaintProperty(`${c.id}-border`, 'line-opacity', 0)
    })
    
    // Возвращаем глобусные точки
    if (map.getLayer('city-dot')) map.setPaintProperty('city-dot', 'circle-opacity', 1)
    
    // Возвращаем HTML-хитбоксы
    document.querySelectorAll('.city-marker-hitbox').forEach(el => {
      el.style.pointerEvents = 'auto'
      el.style.opacity = '1'
    })
  }, 1000)
}

// Функция нырка в город
const diveTo = (cityId) => {
  const city = cities.find(c => c.id === cityId)
  if (!city || !map) return
  
  isDived.value = true
  activeCity.value = city

  // 1. Полет камеры
  map.flyTo({
    center: city.coordinates,
    zoom: 10.54, // Увеличили еще на 15% (было 10.34)
    pitch: 0, // Смотрим перпендикулярно сверху вниз
    bearing: 0,
    padding: { right: 450, top: 200 }, // top: 200 смещает центр города ниже, чтобы он помещался в кадре
    duration: 3000,
    essential: true,
    easing: (t) => t * (2 - t)
  })

  // 2. Подгружаем слой Краснодара (если его еще нет)
  if (!map.getSource(`${city.id}-data`)) {
    map.addSource(`${city.id}-data`, {
      type: 'geojson',
      data:  `/${city.id}.geojson`
    })
    
    map.addLayer({
      id: `${city.id}-fill`,
      type: 'fill',
      source: `${city.id}-data`,
      paint: {
        'fill-color': 'rgba(0, 0, 0, 0.04)', // Город чуть темнее страны, чтобы выделялся
        'fill-opacity': 0, // Изначально прозрачный
        'fill-opacity-transition': { duration: 1500 } // Плавное появление
      }
    })
    
    map.addLayer({
      id: `${city.id}-border`,
      type: 'line',
      source: `${city.id}-data`,
      paint: {
        'line-color': 'rgba(0, 0, 0, 0.3)', // Тонкая графитовая граница
        'line-width': 1.5,
        'line-opacity': 0,
        'line-opacity-transition': { duration: 1500 }
      }
    })
  }

  // 3. Через 1 секунду после начала полета начинаем смену декораций
  setTimeout(() => {
    // ВАЖНО: Мы больше НЕ скрываем Россию. Она остается фоном, 
    // поэтому скачков цвета больше не будет!
    
    // Растворяем глобусные точки
    if (map.getLayer('city-dot')) map.setPaintProperty('city-dot', 'circle-opacity', 0)
    
    // Прячем HTML-хитбоксы с надписями
    document.querySelectorAll('.city-marker-hitbox').forEach(el => {
      el.style.pointerEvents = 'none'
      el.style.opacity = '0'
      el.style.transition = 'opacity var(--anim-duration-slowest) var(--anim-easing-ease)'
    })

    // Показываем контур Краснодара поверх России
    map.setPaintProperty(`${city.id}-fill`, 'fill-opacity', 1)
    map.setPaintProperty(`${city.id}-border`, 'line-opacity', 1)

  }, 1000)

  // Показываем точки ЖК сразу, чтобы они не появлялись слишком поздно
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
    
    wrapper.addEventListener('click', () => {
      toggleComplex(complex.id)
    })

    const marker = new mapboxgl.Marker({ 
      element: wrapper,
      pitchAlignment: 'map'
    })
      .setLngLat(complex.coordinates)
      .addTo(map)
      
    complexMarkers.push({ marker, complex })
  })
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
    zoom: 5.2,
    center: [42, 48], // Смещаем левее, чтобы Sidebar справа не закрывал города 
    pitch: 0,
    
    // ЖЕСТКАЯ БЛОКИРОВКА ВСЕХ ВЗАИМОДЕЙСТВИЙ С КАРТОЙ
    interactive: false
  })

  // Фикс рассинхронизации размеров холста
  window.addEventListener('resize', () => {
    if (map) map.resize()
  })

  map.on('style.load', () => {
    map.setFog({
      'color': '#ffffff', 
      'high-color': '#ffffff', 
      'space-color': '#ffffff', 
      'star-intensity': 0 
    })
  })

  map.on('load', () => {
    map.addSource('countries', {
      type: 'geojson',
      data: '/countries.geojson'
    })

    // Только граница России (Оранжевая)
    map.addLayer({
      id: 'russia-border',
      type: 'line',
      source: 'countries',
      filter: ['==', 'admin', 'Russia'],
      paint: {
        'line-color': 'rgba(0, 0, 0, 0.3)', // Тонкая графитовая граница
        'line-width': 1.5
      }
    })

    // Только заливка России
    map.addLayer({
      id: 'russia-fill',
      type: 'fill',
      source: 'countries',
      filter: ['==', 'admin', 'Russia'],
      paint: {
        'fill-color': '#eaeaea',
        'fill-opacity': 1
      }
    })

    // Создаем GeoJSON с городами для WebGL
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

    // Анимация пульса в WebGL
    let pulseFrame = 0
    const animatePulse = () => {
      pulseFrame = (pulseFrame + 1) % 240
      const progress = pulseFrame / 240
      const radius = 5 + progress * 12.5 // Увеличиваем радиус (в 2 раза меньше)
      
      // Если мы внутри города, пульс не показываем
      const baseOpacity = isDived.value ? 0 : 0.8
      const opacity = baseOpacity * (1 - progress) // Затухание

      if (map.getLayer('city-pulse')) {
        map.setPaintProperty('city-pulse', 'circle-radius', radius)
        map.setPaintProperty('city-pulse', 'circle-opacity', opacity)
      }
      requestAnimationFrame(animatePulse)
    }
    animatePulse()

    // Добавляем маркеры городов (ТОЛЬКО ДЛЯ ХОВЕРА И КЛИКА, БЕЗ ТЕКСТА)
    cities.forEach(city => {
      const el = document.createElement('div')
      el.className = 'city-marker-hitbox'

      el.addEventListener('click', () => {
        diveTo(city.id)
      })

      el.addEventListener('mouseenter', (e) => {
        hoveredCity.value = city
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

    // Динамический масштаб и позиционирование маркеров
    const updateMapState = () => {
      const z = map.getZoom()
      
      // На зуме 4 масштаб 100%, на зуме 1.5 масштаб 40%
      const scale = Math.max(0.4, Math.min(1, (z - 1) / 3))
      document.getElementById('map').style.setProperty('--marker-scale', scale)
      
      // Плавно сводим искусственные координаты к реальным при приближении от зума 5 к зуму 9
      const coordFactor = Math.max(0, Math.min(1, (z - 5) / 4))
      
      const newFeatures = cities.map((c, i) => {
        const start = c.globeCoordinates || c.coordinates
        const end = c.coordinates
        const currentLng = start[0] + (end[0] - start[0]) * coordFactor
        const currentLat = start[1] + (end[1] - start[1]) * coordFactor
        const currentCoords = [currentLng, currentLat]
        
        // Обновляем HTML маркеры
        if (markers[i] && markers[i].marker) {
          markers[i].marker.setLngLat(currentCoords)
        }
        
        return {
          type: 'Feature',
          geometry: { type: 'Point', coordinates: currentCoords },
          properties: { id: c.id, name: c.name }
        }
      })
      
      // Обновляем WebGL слой
      const source = map.getSource('cities-data')
      if (source) {
        source.setData({
          type: 'FeatureCollection',
          features: newFeatures
        })
      }
    }
    
    map.on('zoom', updateMapState)
    updateMapState() // Вычисляем координаты под стартовый зум

    // Анимация входа
    setTimeout(() => {
      map.flyTo({
        center: [42, 48],
        zoom: 5.2,
        pitch: 20,
        bearing: 0,
        duration: 3000,
        essential: true,
        easing: (t) => t * (2 - t)
      })
    }, 500)
  })
})


const updateComplexTooltipPosition = (event) => {
  tooltipX.value = event.clientX + 15
  tooltipY.value = event.clientY + 15
}

const updateTooltipPosition = (event) => {
  tooltipX.value = event.clientX + 15
  tooltipY.value = event.clientY + 15
}

onUnmounted(() => {
  markers.forEach(m => m.marker.remove())
  complexMarkers.forEach(m => m.marker.remove())
  if (map) map.remove()
  window.removeEventListener('mousemove', updateTooltipPosition)
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
  position: relative;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: var(--space-30);
  height: var(--space-30);
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
  color: var(--color-gray-800);
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
  width: var(--space-560);
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
  max-height: calc(var(--vh-100) - var(--space-160) - var(--space-96)); /* Вычитаем паддинги (48 * 2) */
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
  padding: var(--space-24) var(--space-32);
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

.city-badge {
  background: var(--color-black);
  color: var(--color-white);
  font-size: var(--text-small);
  font-size: var(--text-body);
  padding: var(--space-8) var(--space-16);
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
}

:deep(.complex-marker) {
  width: 100%;
  height: 100%;
  border-radius: var(--radius-round);
  background: var(--color-black);
  border: var(--border-width-thick, var(--space-2)) solid var(--color-white);
  box-shadow: inset 0 0 0 0 rgba(255, 244, 204, 0), var(--shadow-sm);
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
  box-shadow: inset 0 0 0 2px var(--color-glow-base), var(--shadow-firefly-hover);
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
  padding: var(--space-16);
  cursor: pointer;
  transition: border-color var(--anim-duration-fast) var(--anim-easing-ease), box-shadow var(--anim-duration-fast) var(--anim-easing-ease);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  flex-shrink: 0;
}

.complex-list-item:hover {
  border-color: var(--color-gray-300);
}

.complex-list-item.is-active {
  border-color: var(--color-black);
  box-shadow: var(--shadow-md);
}

.complex-list-item__header {
  display: flex;
  gap: var(--space-16);
  align-items: center;
}

.complex-list-item__thumb {
  width: var(--space-60);
  height: var(--space-60);
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
  box-shadow: inset 0 0 0 2px var(--color-glow-base), var(--shadow-firefly-hover);
}

:deep(.complex-marker-wrapper.is-hovered) {
  z-index: calc(var(--z-top) + 1);
}

:deep(.complex-marker-wrapper.is-active .complex-marker) {
  scale: 1.15;
  background: var(--color-glow-base);
  border-color: var(--color-glow-base);
  box-shadow: inset 0 0 0 2px var(--color-glow-base), var(--shadow-firefly-active);
}

:deep(.complex-marker-wrapper.is-active) {
  z-index: calc(var(--z-top) + 2);
}
</style>
