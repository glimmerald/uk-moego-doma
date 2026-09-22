import re
import glob

replacements = {
    r"color: #fff;": "color: var(--color-white);",
    r"background: #fff;": "background: var(--color-white);",
    r"color: #1a1a1a;": "color: var(--color-dark);",
    r"max-width: 320px;": "max-width: var(--max-width-footer-col);",
    r"transform: translateY\(3.5px\)": "transform: translateY(var(--hamburger-offset))",
    r"transform: translateY\(-3.5px\)": "transform: translateY(calc(var(--hamburger-offset) * -1))",
    r"width: 100vw;": "width: var(--vw-100);",
    r"height: 100vh;": "height: var(--vh-100);",
    r"max-width: 100vw;": "max-width: var(--vw-100);",
    r"width: 480px;": "width: var(--menu-width);",
    r"height: 600px;": "height: var(--slider-height);",
    r"max-width: 800px;": "max-width: var(--slider-max-width);",
    r"'1200px'": "'var(--perspective-slider)'"
}

files = glob.glob("components/*.vue")
for file in files:
    with open(file, "r") as f:
        content = f.read()
    
    for old, new in replacements.items():
        content = re.sub(old, new, content)
        
    with open(file, "w") as f:
        f.write(content)

print("Done components")
