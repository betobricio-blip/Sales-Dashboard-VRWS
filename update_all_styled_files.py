import json

# 1. Run generate_protected_files.py to create the full styled HTML
import generate_protected_files

with open('public/full-index.html', 'r', encoding='utf-8') as f:
    full_html = f.read()

print("Read full_html, length:", len(full_html))

# Verify that full styles are present
assert '--bg: #f5f6f9;' in full_html
assert '.table-scroll' in full_html
assert '.badge.Pipeline' in full_html
assert 'IBM Plex Sans' in full_html

# Save to public/standalone.html
with open('public/standalone.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

# Save to public/index.html (for direct standalone download)
with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

# Update src/defaultContent.ts
json_str = json.dumps(full_html)
with open('src/defaultContent.ts', 'w', encoding='utf-8') as f:
    f.write('export const DEFAULT_STANDALONE_HTML = ' + json_str + ';\n')

print("Updated public/full-index.html, public/standalone.html, and src/defaultContent.ts successfully!")
