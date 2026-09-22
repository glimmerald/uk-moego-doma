import re

with open("pages/index.vue", "r") as f:
    content = f.read()

# 1. Remove the inline transform on press__item
content = re.sub(
    r':style="pressItemTops\.length \? \{ transform: `translateY\(\$\{\(scrollY \+ winHeight / 2 - pressItemTops\[index\]\) \* \(index % 2 === 0 \? 0\.06 : -0\.06\)\}px\)` \} : \{\}"',
    '',
    content
)

# 2. Add GSAP imports
gsap_imports = """import { onMounted, onUnmounted, computed, nextTick } from 'vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

if (typeof window !== 'undefined') {
  gsap.registerPlugin(ScrollTrigger)
}
"""
content = re.sub(r"import \{ onMounted, onUnmounted, computed \} from 'vue'", gsap_imports, content)

# 3. Replace IntersectionObserver and manual scroll with GSAP in script
# We will use regex to slice out the old onMounted and onUnmounted and replace with new.

script_to_remove_start = content.find("// Глобальный скролл для параллакса")
script_to_remove_end = content.find("</script>")

if script_to_remove_start != -1 and script_to_remove_end != -1:
    old_script_chunk = content[script_to_remove_start:script_to_remove_end]
    
    # We will keep onPressMouseMove
    press_mouse_move_start = old_script_chunk.find("// Эффект \"фонарика\"")
    press_mouse_move_end = old_script_chunk.find("onMounted(() => {")
    
    press_mouse_move_code = old_script_chunk[press_mouse_move_start:press_mouse_move_end]
    
    new_script_chunk = press_mouse_move_code + """
onMounted(() => {
  nextTick(() => {
    // 1. Hero Animation
    const heroTl = gsap.timeline();
    heroTl.fromTo('.hero__title-line', 
      { y: 50, opacity: 0 }, 
      { y: 0, opacity: 1, duration: 1, stagger: 0.2, ease: 'power3.out' }
    ).fromTo('.hero__subtitle', 
      { y: 20, opacity: 0 }, 
      { y: 0, opacity: 0.9, duration: 1, ease: 'power2.out' }, 
      "-=0.5"
    );

    // 2. Dispatch Section Parallax
    ScrollTrigger.matchMedia({
      "(min-width: 1025px)": function() {
        gsap.utils.toArray('.dispatch__photo--offset').forEach(photo => {
          gsap.to(photo, {
            yPercent: -20,
            ease: 'none',
            scrollTrigger: {
              trigger: '.section-dispatch',
              start: 'top bottom',
              end: 'bottom top',
              scrub: true
            }
          });
        });
      }
    });

    // 3. Press Section Parallax (О нас пишут)
    gsap.utils.toArray('.press__item').forEach((item, index) => {
      const direction = index % 2 === 0 ? 1 : -1;
      gsap.fromTo(item, 
        { y: 100 * direction },
        {
          y: -100 * direction,
          ease: 'none',
          scrollTrigger: {
            trigger: '.section-press',
            start: 'top bottom',
            end: 'bottom top',
            scrub: true
          }
        }
      );
    });

    // 4. Reveal items (News, Press, Dispatch photos)
    const revealElements = gsap.utils.toArray('.dispatch__photo, .press__item, .news-list__item, .advantages__item');
    revealElements.forEach(el => {
      ScrollTrigger.create({
        trigger: el,
        start: 'top 85%',
        onEnter: () => el.classList.add('is-revealed'),
        once: true
      });
    });
  });
})

onUnmounted(() => {
  ScrollTrigger.getAll().forEach(t => t.kill());
})
"""
    content = content[:script_to_remove_start] + new_script_chunk + content[script_to_remove_end:]

with open("pages/index.vue", "w") as f:
    f.write(content)

print("Done index.vue gsap")
