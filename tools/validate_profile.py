#!/usr/bin/env python3
"""Check local profile images, display sizes, theme variants, and tool captions.
No dependencies. Use --require-local after the one-time original-logo setup.
"""
from __future__ import annotations
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from fetch_official_logos import validate_png

ROOT = Path(__file__).resolve().parents[1]

class ProfileParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.sources = []
    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == 'img':
            self.images.append(data)
        elif tag == 'source':
            self.sources.append(data)


def check(root: Path = ROOT, require_local: bool = False) -> list[str]:
    errors = []
    expected = {x['url'] for x in json.loads((root/'tools/logo-sources.json').read_text())}
    local_paths = set()
    external_paths = set()
    for filename in ('README.md', 'README-static.md'):
        text = (root / filename).read_text(encoding='utf-8')
        parser = ProfileParser()
        parser.feed(text)
        for image in parser.images:
            if not image.get('alt'):
                errors.append(f'{filename}: missing alt text.')
            if not image.get('width', '').isdigit() or int(image['width']) > 720:
                errors.append(f'{filename}: invalid/oversized width: {image.get("src")}')
            if image.get('height'):
                errors.append(f'{filename}: remove fixed image height: {image.get("src")}')
        paths = [x.get('src','') for x in parser.images] + [x.get('srcset','') for x in parser.sources]
        for value in paths:
            if value.startswith(('https://','http://')):
                external_paths.add(value)
                if value not in expected:
                    errors.append(f'{filename}: unexpected external image: {value}')
                if require_local:
                    errors.append(f'{filename}: run fetch_official_logos.py to localize: {value}')
                continue
            path = Path(urllib.parse.unquote(value))
            if path.is_absolute() or '..' in path.parts or not path.parts or path.parts[0] != 'assets':
                errors.append(f'{filename}: unsafe/non-asset image path: {value}')
                continue
            local_paths.add(path)
            if not (root/path).is_file():
                errors.append(f'{filename}: missing {path}')
        block = text.split('<!-- TOOLCHAIN:START -->', 1)[-1].split('<!-- TOOLCHAIN:END -->', 1)[0]
        if re.search(r'\b(?:FSDP|LaTeX)\b', block, re.I):
            errors.append(f'{filename}: removed tool found in toolchain.')
        if '__' in block or '\\_' in block:
            errors.append(f'{filename}: unwanted underscores in tool labels.')
        if len(re.findall(r'<ruby>',block)) != 26:
            errors.append(f'{filename}: expected 26 labeled tools.')
        if len(re.findall(r'<h4>',block)) != 5:
            errors.append(f'{filename}: expected five toolchain headings.')
        if '<a' in re.sub(r'<rt>.*?</rt>', '', block, flags=re.S):
            errors.append(f'{filename}: tool captions should not be linked/underlined.')
        if '(prefers-color-scheme: dark)' not in text or '(prefers-color-scheme: light)' not in text:
            errors.append(f'{filename}: missing a theme condition.')

    for rel in sorted(local_paths):
        p=root/rel
        if not p.exists():continue
        try:
            if p.suffix=='.svg':
                data=p.read_text(); ET.fromstring(data)
                if re.search(r'<script|<foreignObject|(?:href|src)=["\']https?://',data,re.I):
                    errors.append(f'{rel}: unexpected external dependency or script.')
            elif p.suffix=='.png':validate_png(p.read_bytes())
            elif p.suffix=='.gif':
                if not p.read_bytes().startswith((b'GIF87a',b'GIF89a')):
                    errors.append(f'{rel}: invalid GIF signature.')
        except Exception as exc:
            errors.append(f'{rel}: {exc}')
    print(f'Checked {len(local_paths)} distinct local image references; {len(external_paths)} original-logo URLs.')
    if external_paths and not require_local:
        print('Original-logo setup pending. Run: python3 tools/fetch_official_logos.py')
    return errors

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--require-local',action='store_true')
    args=p.parse_args()
    errors=check(require_local=args.require_local)
    if errors:
        print('\n'.join('ERROR: '+e for e in errors),file=sys.stderr)
        sys.exit(1)
    print('All checked references and layout rules passed.')
