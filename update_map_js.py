import re

with open('app/pages/map.vue', 'r') as f:
    text = f.read()

# 1. Update refs
text = text.replace('let isDived = false', 'const isDived = ref(false)\nconst activeCity = ref(null)')

# 2. Update isDived usage
text = text.replace('isDived = false', 'isDived.value = false\n  activeCity.value = null')
text = text.replace('isDived = true', 'isDived.value = true\n  activeCity.value = city')
text = text.replace('const baseOpacity = isDived ? 0 : 0.8', 'const baseOpacity = isDived.value ? 0 : 0.8')

# 3. Add click listener to city hitbox
click_code = """      el.addEventListener('click', () => {
        diveTo(city.id)
      })

      el.addEventListener('mouseenter'"""
text = text.replace("el.addEventListener('mouseenter'", click_code)

# 4. Update Initial Zoom and Center (and remove test-controls CSS)
text = text.replace("zoom: 2.5,", "zoom: 4.2,")
text = text.replace("center: [0, 20],", "center: [30, 48], // Смещаем левее, чтобы Sidebar справа не закрывал города")
# Also the returnToPlanet coords
text = text.replace("center: [60, 55],", "center: [30, 48],")

# 5. Remove test-controls CSS
test_css = """.test-controls {
  position: absolute;
  top: 100px;
  left: 20px;
  z-index: 1000;
}

.test-controls button {
  background-color: #111111;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
}

.test-controls button:hover {
  background-color: #555555;
}"""
text = text.replace(test_css, "")

with open('app/pages/map.vue', 'w') as f:
    f.write(text)
