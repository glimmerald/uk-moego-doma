import re

with open('app/pages/map.vue', 'r') as f:
    text = f.read()

# 1. Add refs for hoveredComplex
if 'const hoveredComplex = ref(null)' not in text:
    text = text.replace('const hoveredCity = ref(null)', 'const hoveredCity = ref(null)\nconst hoveredComplex = ref(null)')

# 2. Add updateComplexTooltipPosition
update_func = """
const updateComplexTooltipPosition = (event) => {
  tooltipX.value = event.clientX + 15
  tooltipY.value = event.clientY + 15
}
"""
if 'updateComplexTooltipPosition' not in text:
    text = text.replace('const updateTooltipPosition = (event) => {', update_func + '\nconst updateTooltipPosition = (event) => {')

# 3. Modify marker creation logic in diveTo to add events
old_creation_logic = """
    // Показываем точки ЖК
    city.complexes.forEach(complex => {
      if (!complex.coordinates) return
      
      const el = document.createElement('div')
      el.className = 'complex-marker glass-effect'
      
      const marker = new mapboxgl.Marker({ element: el })
        .setLngLat(complex.coordinates)
        .addTo(map)
        
      complexMarkers.push({ marker, complex })
    })
"""
new_creation_logic = """
    // Показываем точки ЖК
    city.complexes.forEach(complex => {
      if (!complex.coordinates) return
      
      const el = document.createElement('div')
      el.className = 'complex-marker glass-effect'
      
      el.addEventListener('mouseenter', (e) => {
        hoveredComplex.value = complex
        updateComplexTooltipPosition(e)
        window.addEventListener('mousemove', updateComplexTooltipPosition)
      })

      el.addEventListener('mouseleave', () => {
        hoveredComplex.value = null
        window.removeEventListener('mousemove', updateComplexTooltipPosition)
      })

      const marker = new mapboxgl.Marker({ element: el })
        .setLngLat(complex.coordinates)
        .addTo(map)
        
      complexMarkers.push({ marker, complex })
    })
"""
text = text.replace(old_creation_logic.strip(), new_creation_logic.strip())

# 4. Add template for hoveredComplex
tooltip_template = """
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
            <div class="complex-card__status">{{ hoveredComplex.status }}</div>
          </div>
        </div>
      </div>
    </Transition>
"""
if 'hoveredComplex && isDived' not in text:
    text = text.replace('<!-- Тултип -->', tooltip_template + '\n    <!-- Тултип -->')

# 5. Add CSS for complex card
css = """
.complex-card {
  display: flex;
  flex-direction: column;
  width: 200px;
}
.complex-card__image {
  width: 100%;
  height: 120px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 12px;
}
.complex-card__title {
  font-size: 15px;
  font-weight: 500;
  margin-bottom: 4px;
  color: #000;
}
.complex-card__address {
  font-size: 12px;
  color: #666;
  margin-bottom: 8px;
}
.complex-card__status {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #e65100;
  font-weight: 600;
}
"""
if '.complex-card' not in text:
    text = text.replace('</style>', css + '\n</style>')

with open('app/pages/map.vue', 'w') as f:
    f.write(text)
print("Done!")
