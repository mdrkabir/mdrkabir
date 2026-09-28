#!/usr/bin/env python3
"""Validate the shipped profile using the Python standard library only."""
from __future__ import annotations
import json, re, sys, xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Check(HTMLParser):
    def __init__(self):super().__init__();self.images=[];self.paths=set();self.errors=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in {'script','style','iframe','table','ruby'}:self.errors.append('Unexpected layout/script element: '+tag)
        if tag=='img':
            self.images.append(a)
            if not a.get('alt'):self.errors.append('Image needs alt text')
            if not a.get('width'):self.errors.append('Image needs explicit display width')
            if a.get('width','').isdigit() and int(a['width'])>760:self.errors.append('Oversized image: '+a.get('src',''))
        for key in (['src'] if tag=='img' else ['srcset'] if tag=='source' else []):
            path=a.get(key,'')
            if path.startswith(('https:','http:','data:')):self.errors.append('Profile image is not repository-local: '+path[:80])
            elif path:self.paths.add(path)

def main():
    errors=[];refs=set();report={}
    for name in ['README.md','README-static.md']:
        content=(ROOT/name).read_text();p=Check();p.feed(content)
        for path in p.paths:
            dest=ROOT/path
            if not dest.is_file():p.errors.append('Missing file: '+path)
            elif dest.suffix=='.svg':
                try:ET.parse(dest)
                except ET.ParseError as e:p.errors.append(str(e)+': '+path)
            elif dest.suffix=='.png' and dest.read_bytes()[:8]!=b'\x89PNG\r\n\x1a\n':p.errors.append('Invalid PNG: '+path)
            elif dest.suffix=='.gif' and dest.read_bytes()[:6] not in [b'GIF87a',b'GIF89a']:p.errors.append('Invalid GIF: '+path)
        if 'FSDP' in content or 'LaTeX' in content:p.errors.append('An excluded tool is present')
        if len(re.findall(r'^#### ',content,re.M))!=5:p.errors.append('Expected five toolchain sections')
        if len(re.findall(r'^### ',content,re.M))!=3:p.errors.append('Expected three native project headings')
        report[name]={'images':len(p.images),'local_assets':len(p.paths),'errors':p.errors}
        refs.update(p.paths);errors.extend(p.errors)
    forbidden=list(ROOT.rglob('*.ttf'))+list(ROOT.rglob('*.otf'))+list(ROOT.rglob('*.woff*'))
    if forbidden:errors.append('Do not distribute system font files')
    print(json.dumps(report,indent=2))
    print(f'{len(refs)} unique local image assets checked. '+('FAIL' if errors else 'PASS'))
    return 1 if errors else 0
if __name__=='__main__':sys.exit(main())
