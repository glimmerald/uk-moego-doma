<template>
  <div class="intro-loader" ref="loaderRef" v-show="isVisible">
    <svg 
      class="intro-svg" 
      width="100%" 
      height="100%"
    >
      <defs>
        <!-- Векторная маска -->
        <mask id="arch-mask">
          <rect width="100%" height="100%" fill="white" />
          <path 
            class="arch-hole" 
            ref="holeRef" 
            :d="pathD" 
            fill="black" 
            style="opacity: 0;"
          />
        </mask>
      </defs>

      <!-- Сплошной фон (темный) -->
      <rect 
        class="intro-bg" 
        width="100%" 
        height="100%" 
        fill="var(--color-dark)" 
        mask="url(#arch-mask)" 
      />
      
      <!-- Рисующийся контур (светлый) -->
      <path 
        class="arch-outline" 
        ref="outlineRef" 
        :d="pathD" 
        fill="none" 
        stroke="var(--color-white)" 
        stroke-width="2" 
        stroke-linecap="round" 
        stroke-linejoin="round" 
        style="opacity: 0;"
      />
    </svg>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import gsap from 'gsap'

const emit = defineEmits(['complete'])

const loaderRef = ref(null)
const outlineRef = ref(null)
const holeRef = ref(null)
const isVisible = ref(true)
const pathD = ref('')

const updatePath = () => {
  if (typeof window === 'undefined') return
  
  const w = window.innerWidth
  const h = window.innerHeight
  
  // Ширина арки: на десктопе до 400px, на мобилках до 60% ширины экрана
  const archWidth = Math.min(w * 0.6, 400)
  
  // Высота арки: 70% высоты экрана (оставляет место сверху и снизу)
  const archHeight = h * 0.7
  
  // Центр экрана
  const cx = w / 2
  
  // Низ арки: 10% выше низа экрана
  const bottomY = h * 0.9
  
  // Верх арки
  const topY = bottomY - archHeight
  
  // Радиус верхнего закругления (половина ширины)
  const r = archWidth / 2
  
  // Точка начала закругления
  const arcStartY = topY + r
  
  const leftX = cx - r
  const rightX = cx + r
  
  // Строим замкнутый путь
  pathD.value = `M ${leftX} ${bottomY} L ${leftX} ${arcStartY} A ${r} ${r} 0 0 1 ${rightX} ${arcStartY} L ${rightX} ${bottomY} Z`
}

onMounted(() => {
  if (typeof window === 'undefined') return

  // 1. Сначала рассчитываем путь под текущий экран
  updatePath()
  
  // Если окно меняет размер во время загрузки, обновим (опционально)
  window.addEventListener('resize', updatePath)

  // Ждем, пока Vue применит pathD к DOM-элементам, затем запускаем GSAP
  setTimeout(() => {
    const tl = gsap.timeline({
      onComplete: () => {
        isVisible.value = false
        window.removeEventListener('resize', updatePath)
        emit('complete')
      }
    })
    
    // Получаем точную длину пути для анимации
    const length = outlineRef.value.getTotalLength()
    
    // Устанавливаем длину штриха, чтобы скрыть линию, и возвращаем прозрачность
    gsap.set(outlineRef.value, { strokeDasharray: length, strokeDashoffset: length, opacity: 1 })

    tl.to(outlineRef.value, {
      strokeDashoffset: 0,
      duration: 1.5,
      ease: "power2.inOut"
    })
    
    tl.to(holeRef.value, {
      opacity: 1,
      duration: 0.5,
      ease: "power1.inOut"
    }, "-=0.2")

    tl.to(outlineRef.value, {
      opacity: 0,
      duration: 0.3
    }, "-=0.3")

    tl.to(loaderRef.value, {
      scale: 50,
      opacity: 0,
      duration: 1.5,
      ease: "expo.in"
    }, "+=0.2")
  }, 50)
})
</script>

<style scoped>
.intro-loader {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  transform-origin: center center;
  pointer-events: auto;
  will-change: transform, opacity;
}

.intro-svg {
  width: 100vw;
  height: 100vh;
  display: block;
}
</style>
