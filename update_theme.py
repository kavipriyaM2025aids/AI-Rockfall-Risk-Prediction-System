import os

js_path = r'c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM\frontend\js\app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace hardcoded backgrounds
content = content.replace('background:#000;', 'background:#E8EFEB;')
content = content.replace('background:rgba(0,0,0,0.2);', 'background:#FAFCFA;')
content = content.replace('border:1px solid rgba(255,255,255,0.05);', 'border:1px solid #D7E1DC;')

# Also search for other dark theme colors
content = content.replace('background:rgba(255,255,255,0.05);', 'background:#F5F8F6;')
content = content.replace('rgba(255,255,255,0.05)', '#D7E1DC')

# Write back
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app.js")
