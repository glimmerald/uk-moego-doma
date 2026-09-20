import re

with open('app/pages/map.vue', 'r') as f:
    text = f.read()

# Replace hardcoded krasnodar with dynamic city.id in diveTo
text = text.replace("'krasnodar-data'", "`${city.id}-data`")
text = text.replace("'/krasnodar.geojson'", " `/${city.id}.geojson`")
text = text.replace("'krasnodar-fill'", "`${city.id}-fill`")
text = text.replace("'krasnodar-border'", "`${city.id}-border`")

# Also in the setPaintProperty inside setTimeout inside diveTo
#   map.setPaintProperty(`${city.id}-fill`, 'fill-opacity', 1)
#   map.setPaintProperty(`${city.id}-border`, 'line-opacity', 1)

# Now in returnToPlanet:
old_return = """    // Прячем контур Краснодара
    if (map.getLayer('krasnodar-fill')) map.setPaintProperty('krasnodar-fill', 'fill-opacity', 0)
    if (map.getLayer('krasnodar-border')) map.setPaintProperty('krasnodar-border', 'line-opacity', 0)"""

new_return = """    // Прячем контур активного города
    if (activeCity.value) {
      const cityId = activeCity.value.id
      if (map.getLayer(`${cityId}-fill`)) map.setPaintProperty(`${cityId}-fill`, 'fill-opacity', 0)
      if (map.getLayer(`${cityId}-border`)) map.setPaintProperty(`${cityId}-border`, 'line-opacity', 0)
    }"""
text = text.replace(old_return, new_return)

with open('app/pages/map.vue', 'w') as f:
    f.write(text)
