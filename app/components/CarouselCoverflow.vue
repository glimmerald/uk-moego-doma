<template>
  <div 
    class="carousel-container" 
    :style="{ perspective: 'var(--perspective-slider)' }"
    @pointerdown="onPointerDown"
    @pointermove="onPointerMove"
    @pointerup="onPointerUp"
    @pointerleave="onPointerUp"
    @mouseenter="stopAutoplay"
    @mouseleave="startAutoplay"
  >
    <div class="carousel-wrapper">
      <div 
        v-for="(slide, index) in slides" 
        :key="index"
        class="carousel-slide"
        :style="getSlideStyle(index)"
        @click="setActive(index)"
      >
        <img :src="slide" alt="ЖК Фото" loading="lazy" draggable="false" />
        <div class="carousel-slide__overlay"></div>
      </div>
    </div>
    
    <button class="carousel-nav carousel-nav--prev" @click="prev">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
        <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
    <button class="carousel-nav carousel-nav--next" @click="next">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
        <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  slides: {
    type: Array,
    required: true
  }
})

const activeIndex = ref(0)
const total = props.slides.length
let autoplayTimer = null

const setActive = (index) => {
  activeIndex.value = index
}

const next = () => {
  activeIndex.value = (activeIndex.value + 1) % total
}

const prev = () => {
  activeIndex.value = (activeIndex.value - 1 + total) % total
}

// Autoplay logic
const startAutoplay = () => {
  if (autoplayTimer) clearInterval(autoplayTimer)
  autoplayTimer = setInterval(next, 3000)
}

const stopAutoplay = () => {
  if (autoplayTimer) {
    clearInterval(autoplayTimer)
    autoplayTimer = null
  }
}

// Drag / Swipe logic
const isDragging = ref(false)
const startX = ref(0)
const diffX = ref(0)

const onPointerDown = (e) => {
  isDragging.value = true
  startX.value = e.clientX || e.touches?.[0]?.clientX
  stopAutoplay()
}

const onPointerMove = (e) => {
  if (!isDragging.value) return
  const currentX = e.clientX || e.touches?.[0]?.clientX
  diffX.value = currentX - startX.value
}

const onPointerUp = () => {
  if (!isDragging.value) return
  
  if (diffX.value > 50) {
    prev() // Swipe right -> prev
  } else if (diffX.value < -50) {
    next() // Swipe left -> next
  }
  
  isDragging.value = false
  diffX.value = 0
  startAutoplay()
}

onMounted(() => {
  startAutoplay()
})

onUnmounted(() => {
  stopAutoplay()
})

const getSlideStyle = (index) => {
  let diff = index - activeIndex.value
  
  if (diff > total / 2) diff -= total
  if (diff < -total / 2) diff += total

  const absDiff = Math.abs(diff)
  
  let translateX = 0
  let translateZ = 0
  let rotateY = 0
  let opacity = 1
  let zIndex = total - absDiff
  let brightness = 1

  // Если мы сейчас тянем (drag), можно добавлять небольшое смещение для интерактивности
  const dragOffset = isDragging.value ? (diffX.value / window.innerWidth) * 100 : 0

  if (diff === 0) {
    translateX = dragOffset * 0.5 // Немного тянем активный слайд
    translateZ = 0
    rotateY = dragOffset * -0.2 // Легкий наклон при свайпе
    brightness = 1
  } else if (absDiff === 1) {
    translateX = diff * 60 + dragOffset * 0.3
    translateZ = -300
    rotateY = diff * -40
    brightness = 0.6
  } else if (absDiff === 2) {
    translateX = diff * 45 + dragOffset * 0.2
    translateZ = -600
    rotateY = diff * -50
    brightness = 0.3
  } else {
    opacity = 0
    translateZ = -1000
    translateX = 0
  }

  // Убираем плавность анимации (transition) во время драга, чтобы слайд "прилипал" к пальцу/мышке
  const transition = isDragging.value ? 'none' : 'transform 0.8s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.8s ease'

  return {
    transform: `translateX(${translateX}%) translateZ(${translateZ}px) rotateY(${rotateY}deg)`,
    zIndex,
    opacity,
    transition,
    '--slide-brightness': brightness
  }
}
</script>

<style scoped>
.carousel-container {
  position: relative;
  width: 100%;
  height: var(--slider-height);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: visible;
  touch-action: pan-y; /* Позволяет скроллить страницу вверх-вниз, но перехватывает свайпы влево-вправо */
  user-select: none; /* Запрет выделения текста при драге */
}

.carousel-wrapper {
  position: relative;
  width: 50%;
  max-width: var(--slider-max-width);
  height: 100%;
  transform-style: preserve-3d;
  display: flex;
  align-items: center;
  justify-content: center;
}

.carousel-slide {
  position: absolute;
  width: 100%;
  height: 100%;
  cursor: grab;
  border-radius: var(--space-16);
  overflow: hidden;
  box-shadow: 0 var(--space-20) var(--space-50) var(--color-overlay);
}

.carousel-slide:active {
  cursor: grabbing;
}

.carousel-slide img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  pointer-events: none; /* Чтобы браузер не пытался перетаскивать саму картинку (ghost image) */
}

.carousel-slide__overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: var(--color-black);
  opacity: calc(1 - var(--slide-brightness));
  transition: opacity 0.8s ease;
  pointer-events: none;
}

.carousel-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: var(--space-48);
  height: var(--space-48);
  border-radius: 50%;
  background: var(--color-white-80);
  backdrop-filter: blur(var(--space-4));
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-dark);
  z-index: 100;
  transition: background 0.3s ease;
  cursor: pointer;
  border: none;
}

.carousel-nav:hover {
  background: var(--color-white);
}

.carousel-nav--prev {
  left: var(--space-20);
}

.carousel-nav--next {
  right: var(--space-20);
}

@media (max-width: 1024px) {
  .carousel-wrapper {
    width: 60%;
    height: 80%;
  }
}

@media (max-width: 768px) {
  .carousel-wrapper {
    width: 75%;
    height: 70%;
  }
  .carousel-nav {
    display: none;
  }
}
</style>
