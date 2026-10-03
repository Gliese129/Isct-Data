"""Report course codes visible in downloaded guide text but absent from JSON.

This is a review aid: wrapped rows and cross-department references require human
judgment before adding a course. Run from the repository with a sibling
`/tmp/isct-guides/{2025,2026}/{01..17}.txt` download.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).parents[1]
GUIDES = Path('/tmp/isct-guides')
DEPS = ['math','physics','chemistry','eps','mech','sc','ee','ict','ie','mat','chem-eng','mcs','cs','life','arch','civil','transdisciplinary']
for year in ('2025','2026'):
    for n, dep in enumerate(DEPS, 1):
        text = GUIDES/year/f'{n:02d}.txt'
        data = ROOT/'departments'/f'{year}.json'
        if not text.exists() or not data.exists(): continue
        published = set(re.findall(r'\b[A-Z]{3}\.[A-Z]\d{3}(?:\.[A-Z])?\b', text.read_text(errors='ignore')))
        published = {x.rsplit('.',1)[0] if x.rsplit('.',1)[-1].isalpha() else x for x in published}
        current = json.loads(data.read_text())
        obj = next(x for x in current['departments'] if x['id']==dep)
        present = {x['code'] for x in obj['recommended']}
        print(year, dep, 'published=',len(published), 'stored=',len(present), 'missing=',sorted(published-present))
