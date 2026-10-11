import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
with open('frontend/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()
with open('frontend/css/login.css', 'r', encoding='utf-8') as f:
    login_css = f.read()
with open('frontend/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

css_min = re.sub(r'\s+', ' ', css)
login_css_min = re.sub(r'\s+', ' ', login_css)
html_min = re.sub(r'\s+', ' ', html).replace('> <', '><')

def minify_backticks(match):
    return re.sub(r'\s+', ' ', match.group(0))

js_min_templates = re.sub(r'`[^`]*`', minify_backticks, js)

js_lines = []
for line in js_min_templates.split('\n'):
    line = line.strip()
    if not line or line.startswith('//'): continue
    js_lines.append(line)

combined = '/* style.css */\n' + css_min + '\n\n/* login.css */\n' + login_css_min + '\n\n<!-- index.html -->\n' + html_min + '\n\n/* app.js */\n' + '\n'.join(js_lines)

with open('frontend_code_compressed.txt', 'w', encoding='utf-8') as f:
    f.write(combined)

print(len(combined.split('\n')))
