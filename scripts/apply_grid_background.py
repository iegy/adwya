from pathlib import Path

ROOT = Path('.')

root_pages = [Path(x) for x in ['index.html','about.html','sources.html','privacy.html','health.html'] if Path(x).exists()]
health_pages = sorted(Path('health').glob('*.html')) if Path('health').exists() else []

for p in root_pages + health_pages:
    text = p.read_text(encoding='utf-8')
    href = 'grid-bg.css' if p.parent == Path('.') else '../grid-bg.css'
    tag = f'<link rel="stylesheet" href="{href}">'
    if tag in text:
        continue
    candidates = [
        '<link rel="stylesheet" href="theme-v2.css">',
        '<link rel="stylesheet" href="../theme-v2.css">',
        '<link rel="stylesheet" href="styles.css">',
        '<link rel="stylesheet" href="../styles.css">',
        '<link rel="stylesheet" href="theme-v2.css" />',
        '<link rel="stylesheet" href="../theme-v2.css" />',
        '<link rel="stylesheet" href="styles.css" />',
        '<link rel="stylesheet" href="../styles.css" />',
    ]
    inserted = False
    for marker in candidates:
        if marker in text:
            text = text.replace(marker, marker + tag, 1)
            inserted = True
            break
    if not inserted:
        text = text.replace('</head>', tag + '</head>', 1)
    p.write_text(text, encoding='utf-8')

build = Path('scripts/build-pages.mjs')
if build.exists():
    text = build.read_text(encoding='utf-8')
    old = "'styles.css','theme-v2.css','app.js'"
    new = "'styles.css','theme-v2.css','grid-bg.css','app.js'"
    if old in text:
        text = text.replace(old, new, 1)
    elif "'grid-bg.css'" not in text:
        raise RuntimeError('Could not locate build copy list')
    build.write_text(text, encoding='utf-8')

# Assertions
assert 'grid-bg.css' in Path('index.html').read_text(encoding='utf-8')
assert "'grid-bg.css'" in Path('scripts/build-pages.mjs').read_text(encoding='utf-8')
for p in health_pages:
    assert '../grid-bg.css' in p.read_text(encoding='utf-8'), p

print(f'Updated {len(root_pages)} root pages and {len(health_pages)} health pages')
