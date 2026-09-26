#!/usr/bin/env python3
"""Check local asset/document links and SVG safety without network dependencies."""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
errors = []
checked = 0
for source in ROOT.rglob('*.md'):
    body = source.read_text(encoding='utf-8')
    links = re.findall(r'\]\(([^\s)]+)', body)
    links += re.findall(r'(?:src|srcset|href)="([^"]+)"', body)
    for link in links:
        if link.startswith(('https://','http://','mailto:','#')):
            continue
        path = unquote(urlsplit(link).path)
        if path and not (source.parent / path).exists():
            errors.append(f'{source.relative_to(ROOT)}: missing target {path}')
        checked += 1
    if source.name in ('README.md','README.pt-BR.md') and source.parent == ROOT:
        for bad in ('YOUR_USERNAME','TODO','example.com','PLACEHOLDER'):
            if bad in body:
                errors.append(f'{source.name}: unresolved marker {bad}')
for path in (ROOT / 'assets').rglob('*.svg'):
    try:
        tree = ET.fromstring(path.read_text())
        for element in tree.iter():
            if element.tag.rsplit('}',1)[-1] in ('script','foreignObject'):
                errors.append(f'{path.name}: unsupported SVG element')
            for key, value in element.attrib.items():
                if key.lower().startswith('on') or value.startswith(('http:','https:','javascript:')):
                    errors.append(f'{path.name}: active/external SVG content')
    except ET.ParseError as exc:
        errors.append(f'{path.name}: {exc}')
if errors:
    print('\n'.join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f'Checked {checked} local references and all SVG assets.')
