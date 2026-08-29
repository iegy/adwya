from pathlib import Path

ROOT = Path('.')
NEW = 'https://adwya.iegy.net'
OLD_BASES = ['https://iegy.net/adwya', 'https://iegy.github.io/adwya']
TEXT_EXTS = {'.html','.xml','.txt','.js','.mjs','.webmanifest','.md','.json','.css'}

changed=[]
for p in ROOT.rglob('*'):
    if not p.is_file():
        continue
    if '.git' in p.parts or '.github' in p.parts or p.name == 'migrate_to_subdomain.py':
        continue
    if p.suffix.lower() not in TEXT_EXTS and p.name not in {'robots.txt','CNAME'}:
        continue
    try:
        text=p.read_text(encoding='utf-8')
    except Exception:
        continue
    original=text
    for old in OLD_BASES:
        text=text.replace(old, NEW)
    if p.as_posix()=='index.html':
        if 'rel="canonical"' not in text:
            marker='  <meta name="robots" content="index,follow,max-image-preview:large" />\n'
            text=text.replace(marker, marker + f'  <link rel="canonical" href="{NEW}/" />\n')
        if 'property="og:url"' not in text:
            marker='  <meta property="og:description" content="دليلك الذكي للبحث عن الأدوية في مصر ومقارنة البدائل والأسعار." />\n'
            text=text.replace(marker, marker + f'  <meta property="og:url" content="{NEW}/" />\n')
        text=text.replace('content="assets/logo.png"', f'content="{NEW}/assets/logo.png"')
        text=text.replace('"target":"?q={search_term_string}"', f'"url":"{NEW}/","target":"{NEW}/?q={{search_term_string}}"')
    if text != original:
        p.write_text(text,encoding='utf-8')
        changed.append(p.as_posix())

Path('CNAME').write_text('adwya.iegy.net\n',encoding='utf-8')
if 'CNAME' not in changed: changed.append('CNAME')

# hard assertions for migration correctness
checks=['index.html','health.html','sitemap.xml','robots.txt','scripts/build-pages.mjs']
for f in checks:
    t=Path(f).read_text(encoding='utf-8')
    assert 'https://iegy.net/adwya' not in t, f
    assert 'https://iegy.github.io/adwya' not in t, f
assert 'https://adwya.iegy.net/' in Path('index.html').read_text(encoding='utf-8')
assert 'adwya.iegy.net' in Path('sitemap.xml').read_text(encoding='utf-8')
assert Path('CNAME').read_text(encoding='utf-8').strip()=='adwya.iegy.net'
print('Migrated files:', len(changed))
print('\n'.join(changed))
