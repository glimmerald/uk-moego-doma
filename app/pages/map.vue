<template>
  <div class="map-page">
    <AppHeader />
    
    <!-- Временная кнопка для теста -->
    <div class="test-controls">
      <button @click="diveTo('krd')">Нырок в Краснодар</button>
      <button @click="returnToPlanet()" style="margin-left: 10px; background-color: #555;">Назад к планете</button>
    </div>

    <div class="map-container" id="map" ref="mapContainer"></div>

    <!-- Тултип -->
    <Transition name="fade">
      <div 
        v-if="hoveredCity"
        class="map-tooltip"
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
import AppHeader from '~/components/AppHeader.vue'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

const mapContainer = ref(null)
let map = null
let isDived = false

const hoveredCity = ref(null)
const tooltipX = ref(0)
const tooltipY = ref(0)

// Данные городов с реальными координатами [lng, lat]
const cities = [
  {
    id: 'kld',
    name: 'Калининград',
    coordinates: [20.4522, 54.7104],
    complexes: [{ name: 'ЖК Калининградский' }]
  },
  {
    id: 'krd',
    name: 'Краснодар',
    coordinates: [38.9753, 45.0355],
    complexes: [
      { name: 'ЖК Престиж' }, 
      { name: 'ЖК Марсель' }, 
      { name: 'ЖК Аврора' }, 
      { name: 'ЖК Фреш' }
    ]
  },
  {
    id: 'adg',
    name: 'Республика Адыгея',
    coordinates: [39.1833, 44.6098], // Майкоп
    complexes: [{ name: 'ЖК Спортивный парк' }]
  }
]

// Функция возврата на общую планету
const returnToPlanet = () => {
  if (!map) return
  isDived = false

  // Возвращаем камеру на Россию
  map.flyTo({
    center: [60, 55],
    zoom: 2.5,
    pitch: 20, // Возвращаем легкий наклон, как было при входе
    bearing: 0,
    duration: 3000,
    essential: true,
    easing: (t) => t * (2 - t)
  })

  // Через 1 секунду после начала обратного полета
  setTimeout(() => {
    // Прячем контур Краснодара
    if (map.getLayer('krasnodar-fill')) map.setPaintProperty('krasnodar-fill', 'fill-opacity', 0)
    if (map.getLayer('krasnodar-border')) map.setPaintProperty('krasnodar-border', 'line-opacity', 0)
    
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
  
  isDived = true

  // 1. Полет камеры
  map.flyTo({
    center: city.coordinates,
    zoom: 11, // Зум до уровня города
    pitch: 0, // Смотрим перпендикулярно сверху вниз
    bearing: 0,
    duration: 3000,
    essential: true,
    easing: (t) => t * (2 - t)
  })

  // 2. Подгружаем слой Краснодара (если его еще нет)
  if (!map.getSource('krasnodar-data')) {
    map.addSource('krasnodar-data', {
      type: 'geojson',
      data: '/krasnodar.geojson'
    })
    
    map.addLayer({
      id: 'krasnodar-fill',
      type: 'fill',
      source: 'krasnodar-data',
      paint: {
        'fill-color': '#dcdcdc', // Город чуть темнее страны, чтобы выделялся
        'fill-opacity': 0, // Изначально прозрачный
        'fill-opacity-transition': { duration: 1500 } // Плавное появление
      }
    })
    
    map.addLayer({
      id: 'krasnodar-border',
      type: 'line',
      source: 'krasnodar-data',
      paint: {
        'line-color': '#e65100', // Оранжевая граница
        'line-width': 2,
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
      el.style.transition = 'opacity 1s ease'
    })

    // Показываем контур Краснодара поверх России
    map.setPaintProperty('krasnodar-fill', 'fill-opacity', 1)
    map.setPaintProperty('krasnodar-border', 'line-opacity', 1)
  }, 1000)
}

onMounted(() => {
  // Ваш личный ключ Mapbox
  mapboxgl.accessToken = 'pk.eyJ1Ijoiamsta3Jhc25vZGFyIiwiYSI6ImNtdThhdzYwbzBxMWEyeXM3ZDNnNGJoOTkifQ.kqIYZO0xU7inIoXFKFjpWQ'

  map = new mapboxgl.Map({
    container: 'map',
    style: {
      version: 8,
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
    zoom: 1.5,
    center: [0, 20], 
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
        'line-color': '#e65100', // ЯРКАЯ ОРАНЖЕВАЯ ЛИНИЯ
        'line-width': 2
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
        geometry: { type: 'Point', coordinates: c.coordinates },
        properties: { id: c.id }
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
        'circle-color': '#e65100',
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
        'circle-color': '#e65100',
        'circle-radius': 5,
        'circle-pitch-alignment': 'map', // Прибито к земле
        'circle-opacity-transition': { duration: 1500 } // Добавили плавность
      }
    })

    // Анимация пульса в WebGL
    let pulseFrame = 0
    const animatePulse = () => {
      pulseFrame = (pulseFrame + 1) % 120
      const progress = pulseFrame / 120
      const radius = 5 + progress * 25 // Увеличиваем радиус
      
      // Если мы внутри города, пульс не показываем
      const baseOpacity = isDived ? 0 : 0.8
      const opacity = baseOpacity * (1 - progress) // Затухание

      if (map.getLayer('city-pulse')) {
        map.setPaintProperty('city-pulse', 'circle-radius', radius)
        map.setPaintProperty('city-pulse', 'circle-opacity', opacity)
      }
      requestAnimationFrame(animatePulse)
    }
    animatePulse()

    // Добавляем маркеры городов (ТОЛЬКО ДЛЯ ТЕКСТА И ХОВЕРА)
    cities.forEach(city => {
      const el = document.createElement('div')
      el.className = 'city-marker-hitbox'
      
      const label = document.createElement('div')
      label.className = 'city-marker__label'
      label.innerText = city.name

      el.appendChild(label)

      el.addEventListener('mouseenter', (e) => {
        hoveredCity.value = city
        updateTooltipPosition(e)
        window.addEventListener('mousemove', updateTooltipPosition)
        // Подсвечиваем WebGL точку
        map.setPaintProperty('city-dot', 'circle-color', [
          'match', ['get', 'id'], city.id, '#ff6d00', '#e65100'
        ])
        map.setPaintProperty('city-dot', 'circle-radius', [
          'match', ['get', 'id'], city.id, 7, 5
        ])
      })

      el.addEventListener('mouseleave', () => {
        hoveredCity.value = null
        window.removeEventListener('mousemove', updateTooltipPosition)
        // Возвращаем цвет
        map.setPaintProperty('city-dot', 'circle-color', '#e65100')
        map.setPaintProperty('city-dot', 'circle-radius', 5)
      })

      const marker = new mapboxgl.Marker({ 
        element: el,
        anchor: 'center'
      })
        .setLngLat(city.coordinates)
        .addTo(map)
        
      markers.push({ marker, el })
    })

    // Динамический масштаб маркеров от зума
    const updateMarkerScale = () => {
      const z = map.getZoom()
      // На зуме 4 масштаб 100%, на зуме 1.5 масштаб 40%
      const scale = Math.max(0.4, Math.min(1, (z - 1) / 3))
      document.getElementById('map').style.setProperty('--marker-scale', scale)
    }
    map.on('zoom', updateMarkerScale)
    updateMarkerScale() // Инициализация

    // Анимация входа
    setTimeout(() => {
      map.flyTo({
        center: [60, 55],
        zoom: 2.5,
        pitch: 20,
        bearing: 0,
        duration: 3000,
        essential: true,
        easing: (t) => t * (2 - t)
      })
    }, 500)
  })
})

const updateTooltipPosition = (event) => {
  tooltipX.value = event.clientX + 15
  tooltipY.value = event.clientY + 15
}

onUnmounted(() => {
  markers.forEach(m => m.marker.remove())
  if (map) map.remove()
  window.removeEventListener('mousemove', updateTooltipPosition)
})
</script>

<style scoped>
.map-page {
  width: 100%;
  height: 100vh;
  position: relative;
  padding-top: 0; 
  background-color: #fff;
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
  width: 30px;
  height: 30px;
}

:deep(.city-marker__label) {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%) scale(var(--marker-scale, 1));
  transform-origin: top center;
  margin-top: 4px;
  font-size: 13px;
  font-weight: 500;
  color: #555;
  white-space: nowrap;
  pointer-events: none;
  transition: color 0.3s ease, font-weight 0.3s ease;
}

:deep(.city-marker-hitbox:hover .city-marker__label) {
  color: #e65100;
  font-weight: 600;
}

/* Плавающий Тултип */
.map-tooltip {
  position: fixed;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(0, 0, 0, 0.05);
  padding: 16px 20px;
  border-radius: 8px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  pointer-events: none;
  transform: translateY(0);
}

.map-tooltip__header {
  font-size: 16px;
  font-weight: 500;
  color: #000;
  margin-bottom: 4px;
}

.map-tooltip__count {
  font-size: 12px;
  color: #888;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.map-tooltip__list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 0;
  margin: 0;
}

.map-tooltip__list li {
  font-size: 13px;
  color: #444;
  position: relative;
  padding-left: 12px;
}

.map-tooltip__list li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 6px;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background-color: #ccc;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(5px);
}
.test-controls {
  position: absolute;
  top: 100px;
  right: 40px;
  z-index: 100;
}

.test-controls button {
  background-color: #e65100;
  color: white;
  border: none;
  padding: 12px 24px;
  font-family: inherit;
  font-size: 14px;
  font-weight: 500;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.test-controls button:hover {
  background-color: #ff6d00;
}
</style>
