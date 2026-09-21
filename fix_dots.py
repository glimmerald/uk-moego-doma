import re

with open('app/pages/map.vue', 'r') as f:
    text = f.read()

# Remove glass-effect from complex-marker
if "el.className = 'complex-marker glass-effect'" in text:
    text = text.replace("el.className = 'complex-marker glass-effect'", "el.className = 'complex-marker'")

# Hide city-dot when dived
if "map.setPaintProperty(`${city.id}-fill`, 'fill-opacity', 1)" in text:
    if "map.setPaintProperty('city-dot', 'circle-opacity', 0)" not in text:
        text = text.replace(
            "map.setPaintProperty(`${city.id}-fill`, 'fill-opacity', 1)",
            "map.setPaintProperty('city-dot', 'circle-opacity', 0)\n    map.setPaintProperty(`${city.id}-fill`, 'fill-opacity', 1)"
        )

# Show city-dot when returning
if "isDived.value = false" in text:
    if "map.setPaintProperty('city-dot', 'circle-opacity', 1)" not in text:
        text = text.replace(
            "isDived.value = false",
            "isDived.value = false\n  if (map.getLayer('city-dot')) map.setPaintProperty('city-dot', 'circle-opacity', 1)"
        )

# Make complex-marker highly visible
new_css = """
:deep(.complex-marker) {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #111111;
  border: 2px solid #ffffff;
  box-shadow: 0 4px 10px rgba(0,0,0,0.3);
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 10;
}
:deep(.complex-marker:hover) {
  transform: scale(1.4);
  background: #e65100;
  border-color: #ffffff;
  box-shadow: 0 6px 14px rgba(230, 81, 0, 0.4);
}
"""

text = re.sub(r':deep\(\.complex-marker\).*?:deep\(\.complex-marker:hover\).*?\}', new_css.strip(), text, flags=re.DOTALL)

with open('app/pages/map.vue', 'w') as f:
    f.write(text)
print("Fixed!")
