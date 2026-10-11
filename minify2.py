with open('frontend_code_compressed.txt', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

out = []
buffer = ''
for line in lines:
    # if it's a CSS or HTML line, just append
    if line.startswith('/*') or line.startswith('<!--') or line.startswith('<'):
        if buffer:
            out.append(buffer.strip())
            buffer = ''
        out.append(line)
        continue
    
    # join js lines
    buffer += ' ' + line
    if len(buffer) > 150: # wrap at 150 chars to reduce lines
        out.append(buffer.strip())
        buffer = ''

if buffer:
    out.append(buffer.strip())

combined = '\n'.join(out)
with open('frontend_code_super_compressed.txt', 'w', encoding='utf-8') as f:
    f.write(combined)

print(len(out))
