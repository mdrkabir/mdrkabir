#!/usr/bin/env python3
"""Offline, standard-library-only validation for the complete profile bundle."""
from __future__ import annotations
import json,re,sys,xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ProfileParser(HTMLParser):
    def __init__(self):
        super().__init__();self.refs=set();self.images=[];self.errors=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in {'script','style','iframe','table','ruby'}:self.errors.append('Unsupported layout element: '+tag)
        if any(k in a for k in ('style','class','id')):self.errors.append('README must not depend on custom CSS: '+tag)
        if tag=='img':
            self.images.append(a)
            if not a.get('alt'):self.errors.append('Missing alternative text')
            if not a.get('width','').isdigit():self.errors.append('Explicit numeric image width required')
            elif int(a['width'])>312:self.errors.append('Display image larger than the 312px panel cap')
        path=a.get('src' if tag=='img' else 'srcset' if tag=='source' else '', '')
        if path:
            if not path.startswith('assets/profile-v4/'):self.errors.append('Non-local or old-generation image: '+path)
            self.refs.add(path)

def main():
    errors=[];report={};refs=set()
    for name in ('README.md','README-static.md'):
        data=(ROOT/name).read_text();p=ProfileParser();p.feed(data)
        for path in p.refs:
            f=ROOT/path
            if not f.is_file():p.errors.append('Missing asset: '+path);continue
            b=f.read_bytes()
            if f.suffix=='.svg':
                try:
                    r=ET.fromstring(b)
                    for e in r.iter():
                        if e.tag.endswith('script'):p.errors.append('Script in image '+path)
                        for k,v in e.attrib.items():
                            if k.endswith('href') and v.startswith(('http','file:')):p.errors.append('External dependency in '+path)
                except ET.ParseError:p.errors.append('Invalid SVG '+path)
            elif f.suffix=='.png' and not b.startswith(b'\x89PNG\r\n\x1a\n'):p.errors.append('Invalid PNG '+path)
            elif f.suffix=='.gif' and b[:6] not in (b'GIF87a',b'GIF89a'):p.errors.append('Invalid GIF '+path)
        if len(re.findall(r'^#### ',data,re.M))!=5:p.errors.append('Expected five toolchain sections')
        if re.findall(r'^### (\d{2}) · ',data,re.M)!=['01','02','03']:p.errors.append('Expected three numbered native headings')
        if 'FSDP' in data or 'LaTeX' in data:p.errors.append('Excluded tool present')
        if 'Hierarchical models · MCMC' not in data:p.errors.append('Missing required focus wording')
        report[name]={'images':len(p.images),'local_assets':len(p.refs),'errors':p.errors}
        errors+=p.errors;refs|=p.refs
    cfg=json.loads((ROOT/'design/profile.json').read_text())
    if cfg['focus'][2]['subtitle']!=['Hierarchical models · MCMC']:errors.append('Configuration text mismatch')
    for t in ['light','dark']:
        if 'Hierarchical models · MCMC' not in (ROOT/f'assets/profile-v4/focus-{t}.svg').read_text():errors.append('Research focus not regenerated for '+t)
    if any(ROOT.rglob('*.ttf')) or any(ROOT.rglob('*.otf')) or any(ROOT.rglob('*.woff*')):errors.append('Do not distribute font files')
    report['total_assets']=len(refs);report['errors']=errors;report['result']='FAIL' if errors else 'PASS'
    print(json.dumps(report,indent=2));return bool(errors)
if __name__=='__main__':sys.exit(main())
