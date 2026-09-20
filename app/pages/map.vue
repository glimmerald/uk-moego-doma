<template>
  <div class="map-page">
    <AppHeader />
    
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
        <div v-else class="sidebar-content" key="city">
          <button class="sidebar-back-btn" @click="returnToPlanet()">
            &larr; Вернуться к списку городов
          </button>
          <h1 class="sidebar-title">{{ activeCity?.name }}</h1>
          <div class="sidebar-stats">
            <div class="stat-box">
              <div class="stat-val">{{ activeCity?.complexes.length }}</div>
              <div class="stat-label">Жилых комплексов</div>
            </div>
          </div>
          <p class="sidebar-desc" style="margin-top: 20px;">
            Нажмите на маркер на карте, чтобы посмотреть информацию о конкретном жилом комплексе.
          </p>
        </div>
      </Transition>
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
const isDived = ref(false)
const activeCity = ref(null)

const hoveredCity = ref(null)
const tooltipX = ref(0)
const tooltipY = ref(0)

// Данные городов с реальными координатами [lng, lat]
import cities from '~/data/cities.json'

// Функция возврата на общую планету
const returnToPlanet = () => {
  if (!map) return
  isDived.value = false
  activeCity.value = null

  // Возвращаем камеру на Россию
  map.flyTo({
    center: [50, 48],
    zoom: 4.2,
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
    zoom: 11, // Зум до уровня города
    pitch: 0, // Смотрим перпендикулярно сверху вниз
    bearing: 0,
    padding: { right: 450 },
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
      el.style.transition = 'opacity 1s ease'
    })

    // Показываем контур Краснодара поверх России
    map.setPaintProperty(`${city.id}-fill`, 'fill-opacity', 1)
    map.setPaintProperty(`${city.id}-border`, 'line-opacity', 1)
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
    zoom: 4.2,
    center: [50, 48], // Смещаем левее, чтобы Sidebar справа не закрывал города 
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

    // Анимация пульса в WebGL
    let pulseFrame = 0
    const animatePulse = () => {
      pulseFrame = (pulseFrame + 1) % 120
      const progress = pulseFrame / 120
      const radius = 5 + progress * 25 // Увеличиваем радиус
      
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

    // Добавляем маркеры городов (ТОЛЬКО ДЛЯ ТЕКСТА И ХОВЕРА)
    cities.forEach(city => {
      const el = document.createElement('div')
      el.className = 'city-marker-hitbox'
      
      const label = document.createElement('div')
      label.className = 'city-marker__label'
      label.innerText = city.name

      el.appendChild(label)

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
        center: [50, 48],
        zoom: 4.2,
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
  color: #111111;
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
/* --- ИНФОРМАЦИОННАЯ ПАНЕЛЬ (SIDEBAR) --- */
.map-sidebar {
  position: absolute;
  top: 120px;
  right: 40px;
  width: 400px;
  max-height: calc(100vh - 160px);
  z-index: 1000;
  border-radius: 24px;
  padding: 32px;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05);
}

.sidebar-title {
  font-size: 32px;
  font-weight: 300;
  margin-bottom: 16px;
  color: #111;
  letter-spacing: -0.02em;
}

.sidebar-desc {
  font-size: 15px;
  line-height: 1.5;
  color: #555;
  margin-bottom: 32px;
  font-weight: 300;
}

.sidebar-cities {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.sidebar-city-btn {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  font-size: 16px;
  color: #111;
  font-weight: 400;
  transition: all 0.3s ease;
  text-align: left;
}

.sidebar-city-btn:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: translateX(-4px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.05);
}

.city-badge {
  background: #111;
  color: #fff;
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 20px;
  font-weight: 500;
}

.sidebar-back-btn {
  display: inline-flex;
  align-items: center;
  color: #555;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 24px;
  transition: color 0.3s ease;
  padding: 0;
  background: transparent;
  cursor: pointer;
  border: none;
}

.sidebar-back-btn:hover {
  color: #111;
}

.sidebar-stats {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
}

.stat-box {
  background: rgba(255, 255, 255, 0.5);
  padding: 16px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.6);
  flex: 1;
}

.stat-val {
  font-size: 32px;
  font-weight: 300;
  color: #111;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
</style>
