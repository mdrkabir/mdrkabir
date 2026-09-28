#!/usr/bin/env python3
"""Validate the GitHub profile README and its local light/dark artwork."""
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProfileParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = set()
        self.images = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if tag in {'script', 'style', 'iframe', 'table'}:
            self.errors.append(f'Unsupported README element: {tag}')
        if any(key in attr for key in ('style', 'class', 'id')):
            self.errors.append(f'Custom CSS dependency on {tag}')
        if tag == 'img':
            self.images.append(attr)
            if 'alt' not in attr:
                self.errors.append('Image is missing alt text')
            width = attr.get('width', '')
            if not width.isdigit() or int(width) > 760:
                self.errors.append('Image width must be numeric and at most 760px')
        for key in ('src', 'srcset'):
            if key in attr:
                path = attr[key]
                if not path.startswith('assets/profile-v5/'):
                    self.errors.append(f'Unexpected image path: {path}')
                self.refs.add(path)


def main():
    errors = []
    readme = (ROOT / 'README.md').read_text()
    static = (ROOT / 'README-static.md').read_text()
    if readme != static:
        errors.append('README-static.md must match the static README.md')
    if not readme.startswith('# Md Rysul Kabir\n'):
        errors.append('Missing profile heading')
    if '## Selected research' not in readme:
        errors.append('Missing selected research section')
    if len(re.findall(r'^### ', readme, re.M)) != 3:
        errors.append('Expected three selected publications')
    if len(re.findall(r'\[Paper ↗\]\(https://', readme)) != 3:
        errors.append('Expected three paper links')
    if 'profile-v4/' in readme or '.gif' in readme:
        errors.append('The current README references archived artwork')

    parser = ProfileParser()
    parser.feed(readme)
    errors.extend(parser.errors)
    expected = {f'assets/profile-v5/research-thread-{theme}.svg'
                for theme in ('light', 'dark')}
    if parser.refs != expected:
        errors.append(f'Unexpected artwork references: {sorted(parser.refs)}')
    for path in parser.refs:
        asset = ROOT / path
        if not asset.is_file():
            errors.append(f'Missing artwork: {path}')
            continue
        try:
            root = ET.parse(asset).getroot()
        except ET.ParseError:
            errors.append(f'Invalid SVG: {path}')
            continue
        for element in root.iter():
            if element.tag.endswith('script'):
                errors.append(f'Script in artwork: {path}')
            for key, value in element.attrib.items():
                if key.endswith('href') and value.startswith(('http:', 'https:', 'file:')):
                    errors.append(f'External artwork dependency: {path}')

    fonts = [path for pattern in ('*.ttf', '*.otf', '*.woff', '*.woff2')
             for path in ROOT.rglob(pattern)]
    if fonts:
        errors.append('Font files should not be bundled')
    report = {'images': len(parser.images), 'assets': sorted(parser.refs),
              'errors': errors, 'result': 'FAIL' if errors else 'PASS'}
    print(json.dumps(report, indent=2))
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
