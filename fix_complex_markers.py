import re

with open('app/pages/map.vue', 'r') as f:
    text = f.read()

# 1. Add let complexMarkers = []
if 'let complexMarkers = []' not in text:
    text = text.replace('const markers = []', 'const markers = []\nlet complexMarkers = []')

# 2. Add marker removal in returnToPlanet
remove_logic = """
  // Убираем точки ЖК
  complexMarkers.forEach(m => m.marker.remove())
  complexMarkers = []
"""
if '// Убираем точки ЖК' not in text:
    text = text.replace('activeCity.value = null', 'activeCity.value = null\n' + remove_logic)

# 3. Add marker creation in diveTo's setTimeout
creation_logic = """
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
if '// Показываем точки ЖК' not in text:
    target = "map.setPaintProperty(`${city.id}-border`, 'line-opacity', 1)"
    text = text.replace(target, target + '\n' + creation_logic)

# 4. Add CSS
css = """
:deep(.complex-marker) {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s ease;
}

:deep(.complex-marker:hover) {
  transform: scale(1.5);
  background: rgba(0, 0, 0, 1);
}
"""
if '.complex-marker' not in text:
    text = text.replace('</style>', css + '\n</style>')

with open('app/pages/map.vue', 'w') as f:
    f.write(text)
print("Done")
