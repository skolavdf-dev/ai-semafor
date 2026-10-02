#!/usr/bin/env python3
"""Přidá ke každému lokálnímu assetu v *.html parametr ?v=<otisk obsahu>.

Spuštění před nahráním na server (z kořene projektu):
    python tools/bump-version.py

Verze se mění jen u souborů, jejichž obsah se opravdu změnil,
ostatní zůstanou v cache prohlížeče.
"""
import glob, hashlib, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = re.compile(r'((?:href|src)="(assets/[^"?#]+))(?:\?v=[^"]*)?"')

def digest(path):
    with open(path, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]

changed = 0
for page in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    with open(page, encoding='utf-8') as f:
        src = f.read()

    def fix(m):
        asset = os.path.join(ROOT, *m.group(2).split('/'))
        if not os.path.isfile(asset):
            print('CHYBÍ soubor:', m.group(2), 'v', os.path.basename(page), file=sys.stderr)
            return m.group(0)
        return '%s?v=%s"' % (m.group(1), digest(asset))

    out = REF.sub(fix, src)
    if out != src:
        with open(page, 'w', encoding='utf-8', newline='') as f:
            f.write(out)
        changed += 1
        print('aktualizováno:', os.path.basename(page))
print('hotovo, změněno stránek:', changed)
