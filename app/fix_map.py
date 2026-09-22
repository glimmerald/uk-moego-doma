import re

with open("pages/map.vue", "r") as f:
    content = f.read()

replacements = {
    r"height: 100vh;": "height: var(--vh-100);",
    r"transform: translateY\(5px\);": "transform: translateY(var(--space-6));",
    r"calc\(100vh - var\(--space-160\)\)": "calc(var(--vh-100) - var(--space-160))",
    r"var\(--border-width-thick, 2px\)": "var(--border-width-thick, var(--space-2))",
    r"box-shadow: 0 4px 10px rgba\(0,0,0,0.3\);": "box-shadow: var(--shadow-sm);",
    r"box-shadow: 0 6px 14px rgba\(230, 81, 0, 0.4\);": "box-shadow: var(--shadow-md);"
}

for old, new in replacements.items():
    content = re.sub(old, new, content)

with open("pages/map.vue", "w") as f:
    f.write(content)

print("Done map.vue")
