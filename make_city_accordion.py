import re

with open('app/pages/index.vue', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's replace the whole debt__list section manually by extracting it.
start_str = '        <div class="debt__list">'
end_str = '      </div>\n    </section>\n  </div>\n</template>'

start_idx = content.find(start_str)
end_idx = content.find(end_str) + len(end_str)

debt_list_content = content[start_idx:end_idx]

# We know the structure. We want to add the accordion header.
debt_list_content = debt_list_content.replace(
"""          <div class="debt__city" v-for="city in debtRegistry" :key="city.id">
            <h2 class="debt__city-title">{{ city.name }}</h2>
            
            <div class="debt__complex-list">""",
"""          <div 
            class="debt__city" 
            v-for="city in debtRegistry" 
            :key="city.id"
            :class="{ 'is-open': city.isOpen }"
          >
            <div class="debt__city-header" @click="toggleCity(city)">
              <h2 class="debt__city-title">{{ city.name }}</h2>
              <div class="debt__icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="icon-plus"/>
                </svg>
              </div>
            </div>
            
            <div class="debt__city-body-wrapper">
              <div class="debt__city-body">
                <div class="debt__complex-list">""")

# Now add two closing tags at the very end of debt_list_content
# Before the end_str which is:
#       </div>
#     </section>
#   </div>
# </template>
# We need to insert the closing tags before the closing of debt__list
# Wait, the structure was:
#                 </div> <!-- debt__body-wrapper -->
#               </div> <!-- debt__complex -->
#             </div> <!-- debt__complex-list -->
#           </div> <!-- debt__city -->
#         </div> <!-- debt__list -->

# Let's just find the closing tags of debt__complex-list inside debt_list_content
debt_list_content = debt_list_content.replace(
"""              </div>
            </div>
          </div>
        </div>
      </div>
    </section>""",
"""              </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>""")

content = content[:start_idx] + debt_list_content + content[end_idx:]

# 2. Add toggleCity to script
old_script = """const toggleComplex = (complex) => {"""
new_script = """const toggleCity = (city) => {
  city.isOpen = !city.isOpen
}

const toggleComplex = (complex) => {"""
content = content.replace(old_script, new_script)

# 3. Add CSS for debt__city-header, body-wrapper etc.
old_css = """.debt__city-title {
  font-size: var(--text-h5);
  font-weight: var(--font-weight-regular);
  margin-bottom: var(--space-40);
  color: #000;
}"""

new_css = """.debt__city-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  padding-bottom: var(--space-40);
  border-bottom: var(--border-width) solid var(--color-border);
}

.debt__city.is-open .debt__city-header {
  border-bottom: none;
}

.debt__city-title {
  font-size: var(--text-h5);
  font-weight: var(--font-weight-regular);
  color: #000;
  margin: 0;
}

.debt__city-body-wrapper {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows var(--transition-slow);
}

.debt__city.is-open .debt__city-body-wrapper {
  grid-template-rows: 1fr;
}

.debt__city-body {
  overflow: hidden;
}

.debt__city.is-open .debt__city-header .icon-plus {
  d: path("M5 12H19"); /* transform to minus */
}
"""
content = content.replace(old_css, new_css)

with open('app/pages/index.vue', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done.")
