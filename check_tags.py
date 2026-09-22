from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []

    def handle_starttag(self, tag, attrs):
        if tag in ['div', 'section', 'main', 'h2', 'h3', 'h4', 'span', 'p']:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in ['div', 'section', 'main', 'h2', 'h3', 'h4', 'span', 'p']:
            if self.stack and self.stack[-1][0] == tag:
                self.stack.pop()
            else:
                print(f"Mismatched end tag: {tag} at {self.getpos()}, expected {self.stack[-1][0] if self.stack else 'None'}")

with open('app/pages/index.vue', 'r') as f:
    content = f.read()
    
# Extract only template
template = content.split('<template>')[1].split('</template>')[0]
parser = MyHTMLParser()
parser.feed(template)

for tag, pos in parser.stack:
    print(f"Unclosed tag: {tag} at {pos}")
