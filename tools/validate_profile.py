#!/usr/bin/env python3
"""Validate the static GitHub profile and its local light/dark stack tiles."""
from __future__ import annotations

import json
import re
import struct
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProfileParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = set()
        self.tiles = []
        self.errors = []
        self.link = None
        self.picture = None

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if tag in {'script', 'style', 'iframe', 'table'}:
            self.errors.append(f'Unsupported README element: {tag}')
        if any(key in attr for key in ('style', 'class', 'id')):
            self.errors.append(f'Custom CSS dependency on {tag}')
        if tag == 'a':
            self.link = attr.get('href')
        elif tag == 'picture':
            self.picture = {'link': self.link, 'sources': {}, 'images': []}
            self.tiles.append(self.picture)
        elif tag == 'source' and self.picture is not None:
            self.picture['sources'][attr.get('media')] = attr.get('srcset')
        elif tag == 'img':
            if self.picture is None:
                self.errors.append('Image is missing its light/dark picture wrapper')
            else:
                self.picture['images'].append(attr)
            if not attr.get('alt'):
                self.errors.append('Tool image is missing descriptive alt text')
            if (attr.get('width'), attr.get('height')) != ('80', '66'):
                self.errors.append('Tool display dimensions must be 80 × 66')
        for key in ('src', 'srcset'):
            if key in attr:
                self.refs.add(attr[key])

    def handle_endtag(self, tag):
        if tag == 'picture':
            self.picture = None
        elif tag == 'a':
            self.link = None


def png_size(data):
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('Invalid PNG signature')
    position = 8
    while position + 12 <= len(data):
        length = struct.unpack_from('>I', data, position)[0]
        kind = data[position + 4:position + 8]
        if kind == b'acTL':
            raise ValueError('Animated PNG is not allowed')
        position += length + 12
        if kind == b'IEND':
            break
    return struct.unpack_from('>II', data, 16)


def main():
    errors = []
    readme = (ROOT / 'README.md').read_text()
    if (ROOT / 'README-static.md').read_text() != readme:
        errors.append('README-static.md must match the static README.md')
    if not readme.startswith('# Md Rysul Kabir\n'):
        errors.append('Missing readable name heading')
    if 'https://mdrkabir.github.io/homepage/' not in readme:
        errors.append('Missing personal website link')
    sections = re.findall(r'^## (.+)$', readme, re.M)
    if not sections or not sections[-1].startswith('Tech Stack'):
        errors.append('The tech stack must be the final section')
    if re.search(r'\.gif\b|<animate\b', readme, re.I):
        errors.append('Animation is not allowed in the current profile')

    groups = json.loads((ROOT / 'design/toolchain.json').read_text())
    tools = [tool for group in groups for tool in group['tools']]
    expected_refs = {
        f"assets/profile-v4/tool-{tool['key']}-{theme}.png"
        for tool in tools for theme in ('light', 'dark')
    }
    parser = ProfileParser()
    parser.feed(readme)
    errors.extend(parser.errors)
    if parser.refs != expected_refs:
        errors.append(f'Missing assets: {sorted(expected_refs - parser.refs)}; '
                      f'unexpected assets: {sorted(parser.refs - expected_refs)}')
    if len(parser.tiles) != len(tools):
        errors.append(f'Expected {len(tools)} tool tiles, found {len(parser.tiles)}')
    if '<picture>' in readme.split('## Tech Stack', 1)[0]:
        errors.append('Stack images must appear in the final tech stack section')
    for tool in tools:
        matches = [tile for tile in parser.tiles if tile['link'] == tool['url']]
        if len(matches) != 1:
            errors.append(f"Expected one linked tile for {tool['label']}")
            continue
        tile = matches[0]
        expected_sources = {
            f'(prefers-color-scheme: {theme})':
            f"assets/profile-v4/tool-{tool['key']}-{theme}.png"
            for theme in ('light', 'dark')
        }
        if tile['sources'] != expected_sources:
            errors.append(f"Incorrect theme sources for {tool['label']}")
        if len(tile['images']) != 1:
            errors.append(f"Expected one fallback image for {tool['label']}")
        else:
            img = tile['images'][0]
            if (img.get('src') != expected_sources['(prefers-color-scheme: light)']
                    or img.get('alt') != tool['label']):
                errors.append(f"Incorrect fallback or label for {tool['label']}")
    for ref in sorted(expected_refs):
        path = ROOT / ref
        try:
            dimensions = png_size(path.read_bytes())
            if dimensions != (240, 198):
                errors.append(f'Unexpected tile dimensions in {ref}: {dimensions}')
        except (OSError, ValueError, struct.error) as error:
            errors.append(f'{ref}: {error}')

    if any(path for pattern in ('*.ttf', '*.otf', '*.woff', '*.woff2')
           for path in ROOT.rglob(pattern)):
        errors.append('Font files should not be bundled')
    print(json.dumps({'tools': len(tools), 'groups': len(groups),
                      'static_assets': len(expected_refs), 'errors': errors,
                      'result': 'FAIL' if errors else 'PASS'}, indent=2))
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
