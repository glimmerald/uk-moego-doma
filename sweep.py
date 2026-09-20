import re

with open('app/pages/map.vue', 'r') as f:
    text = f.read()

# Replace hex codes
text = text.replace('#e65100', '#111111')
text = text.replace('#ff6d00', '#555555')
# Replace rgba(230, 81, 0, 0.2)
text = text.replace('rgba(230, 81, 0, 0.2)', 'rgba(0, 0, 0, 0.1)')
text = text.replace('rgba(230, 81, 0, 0.4)', 'rgba(0, 0, 0, 0.2)')
text = text.replace('rgba(230, 81, 0, 0.5)', 'rgba(0, 0, 0, 0.2)')
text = text.replace('rgba(230, 81, 0, 0.1)', 'rgba(17, 17, 17, 0.1)')

# Specific color fixes
text = text.replace("'line-color': '#111111', // ЯРКАЯ ОРАНЖЕВАЯ ЛИНИЯ", "'line-color': 'rgba(0, 0, 0, 0.2)', // Тонкая графитовая линия")

with open('app/pages/map.vue', 'w') as f:
    f.write(text)
