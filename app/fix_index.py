import re

with open("pages/index.vue", "r") as f:
    content = f.read()

replacements = {
    r"height: 70vh;": "height: var(--vh-70);",
    r"max-width: 600px;": "max-width: var(--max-width-text);",
    r"max-width: 100vw;": "max-width: var(--vw-100);",
    r"width: 85vw;": "width: var(--vw-85);",
    r"height: 100vh;": "height: var(--vh-100);",
    r"height: 50%;": "height: var(--percent-50);",
    r"max-height: 400px;": "max-height: var(--max-height-dropdown);",
    r"transform: translateX\(-50%\);": "transform: translateX(var(--translate-half-neg));",
    r"transform: translateY\(-100%\);": "transform: translateY(var(--translate-full-neg));",
    r"transform: translateY\(200%\);": "transform: translateY(var(--translate-double));",
    r"transform: translateY\(100%\);": "transform: translateY(var(--translate-full));",
    r"left: 50%;": "left: var(--percent-50);",
    r"calc\(50% \+ 140px\)": "calc(var(--percent-50) + var(--img-offset-140))",
    r"15%": "var(--percent-15)",
    r"50%": "var(--percent-50)",
    r"75%": "var(--percent-75)",
    r"40%": "var(--percent-40)",
    r"`\$\{wIndex \* 0.03\}s`": "`calc(${wIndex} * var(--anim-word-step))`"
}

for old, new in replacements.items():
    content = re.sub(old, new, content)

with open("pages/index.vue", "w") as f:
    f.write(content)

print("Done")
