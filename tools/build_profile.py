#!/usr/bin/env python3
"""Build a GitHub-safe profile from local source assets.

Requirements: Pillow, CairoSVG, fonttools. No network, accounts, or font downloads.
Fonts are used from the local system and are NOT copied into this repository.
"""
from __future__ import annotations
import argparse, functools, html, io, json, re, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import cairosvg
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'profile-v2'
SOURCE = ROOT / 'design' / 'legacy-logos'
CFG = json.loads((ROOT/'design/profile.json').read_text())
OUT.mkdir(parents=True, exist_ok=True)
PALETTES = {
 'light': dict(bg='#FFFFFF', panel='#F7F9FC', bar='#EDF1F7', line='#DCE3EF', text='#162238', muted='#58677E', faint='#7E8BA0', purple='#7255C5', cyan='#157D88', amber='#9B641C', purple_bg='#F0ECFA', cyan_bg='#EAF4F5', amber_bg='#F7F1E7'),
 'dark': dict(bg='#0D1117', panel='#131B27', bar='#1B2433', line='#2D394C', text='#E6EDF6', muted='#A9B8CD', faint='#8494AB', purple='#B8A0EF', cyan='#77C9D1', amber='#E6B86E', purple_bg='#221E35', cyan_bg='#162B33', amber_bg='#2E271E')
}

def find_font(style: str) -> Path:
    inter = {'regular':'Inter-Regular.otf','medium':'Inter-Medium.otf','bold':'Inter-SemiBold.otf'}
    names = [Path('/usr/share/fonts/opentype/inter')/inter.get(style,'Inter-Regular.otf')]
    d = Path('/usr/share/fonts/truetype/dejavu')
    if style == 'mono': names=[d/'DejaVuSansMono.ttf']
    else: names += [d/('DejaVuSans-Bold.ttf' if style=='bold' else 'DejaVuSans.ttf')]
    # Optional user-specified font directory without bundling any font files.
    import os
    if os.environ.get('PROFILE_FONT_DIR'):
        names.insert(0,Path(os.environ['PROFILE_FONT_DIR'])/('DejaVuSansMono.ttf' if style=='mono' else inter[style]))
    names += [Path('/Library/Fonts/Arial.ttf'),Path('C:/Windows/Fonts/arial.ttf')]
    for p in names:
        if p.exists(): return p
    raise FileNotFoundError('Install Inter or DejaVu fonts, or set PROFILE_FONT_DIR to a font directory.')

@functools.lru_cache(None)
def face(style='regular'):
    f=TTFont(find_font(style)); return f, f.getGlyphSet(),f.getBestCmap(),f['head'].unitsPerEm

@functools.lru_cache(None)
def glyph(style, ch):
    f,gs,cmap,upm=face(style); name=cmap.get(ord(ch),'.notdef')
    pen=SVGPathPen(gs); gs[name].draw(pen)
    return pen.getCommands(),f['hmtx'].metrics[name][0]

def measure(s,size,style='regular'):
    return sum(glyph(style,c)[1] for c in s)*size/face(style)[3]

def txt(x,y,s,size,color,style='regular',anchor='start'):
    """Outlined text keeps the exact font metrics on GitHub without font files."""
    width=measure(s,size,style)
    if anchor=='middle': x-=width/2
    elif anchor=='end': x-=width
    scale=size/face(style)[3]; parts=[]; dx=0
    for c in s:
        d,adv=glyph(style,c)
        if d: parts.append(f'<path d="{d}" transform="translate({dx},0)"/>')
        dx+=adv
    return f'<g fill="{color}" aria-label="{html.escape(s,quote=True)}" transform="translate({x:.3f},{y:.3f}) scale({scale:.7f},{-scale:.7f})">'+''.join(parts)+'</g>'

def rect(x,y,w,h,fill,rx=0,stroke=None,sw=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>'

def line(x1,y1,x2,y2,color,sw=1,extra=''):
    return f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{sw}" {extra}/>'

def svg(body,w,h,title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{html.escape(title)}</title>{body}</svg>'

def terminal(theme, command='cat research.txt', visible=3, cursor=True):
    p=PALETTES[theme]; W,H=760,336
    s=rect(.5,.5,759,335,p['panel'],13,p['line'])
    s+= '<path d="M13 1H747Q759 1 759 13V37H1V13Q1 1 13 1Z" fill="'+p['bar']+'"/>'
    for cx,c in [(20,'#CF8C99'),(35,'#C5AC75'),(50,'#74B5AB')]:
        s+=f'<circle cx="{cx}" cy="19" r="4" fill="{c}"/>'
    s+=txt(70,22.5,'mdrkabir / research.console',10,p['muted'],'mono')
    s+=txt(738,22.5,'RESEARCH · CODE · EVALUATION',8.6,p['faint'],'mono','end')
    s+=txt(28,94,CFG['name'],32,p['text'],'bold')
    s+=txt(29,121,CFG['role'],13,p['muted'])
    s+=txt(29,143,CFG['institution'],13,p['muted'])
    s+=line(440,63,440,296,p['line'])
    prompt='rysul@research:~$'
    s+=txt(29,186,prompt,11.6,p['cyan'],'mono')
    start=29+measure(prompt,11.6,'mono')+11
    s+=txt(start,186,command,11.6,p['text'],'mono')
    if cursor: s+=rect(start+measure(command,11.6,'mono')+3,176,6,12,p['faint'])
    for i in range(visible):
        color=p[['purple','cyan','amber'][i]]
        s+=rect(29,209+i*25,2.5,13,color,1)
        s+=txt(41,220+i*25,CFG['terminal'][i],11.6,color,'mono')
    s+=txt(465,65,'RESEARCH FOCUS',9.5,p['muted'],'mono')
    for i,block in enumerate(CFG['focus']):
        accent=['purple','cyan','amber'][i]; y=82+i*73
        s+=rect(460,y,274,64,p[accent+'_bg'],8)
        s+=txt(476,y+23,f'{i+1:02d}',10,p[accent],'mono')
        # All titles and subtitle lines share this exact center and baseline grid.
        center=614
        assert measure(block['title'],13.5,'bold')<=230
        s+=txt(center,y+22,block['title'],13.5,p['text'],'bold','middle')
        subtitles=block['subtitle']
        by=y+42 if len(subtitles)>1 else y+44
        for j,sub in enumerate(subtitles):
            assert measure(sub,11.3)<=232
            s+=txt(center,by+j*14,sub,11.3,p['muted'],'regular','middle')
    s+=line(28,307,732,307,p['line'])
    s+=txt(29,325,'learning methods → model behavior',9.2,p['faint'],'mono')
    s+=txt(731,325,'Bloomington, Indiana',9.2,p['faint'],'mono','end')
    return svg(s,W,H,'Research console — '+CFG['name'])

def write_console(theme):
    # Start with readable completed content. Only terminal output moves.
    states=[('cat research.txt',3,True,4000),('cat research.txt',3,False,550),('',0,True,450)]
    cmd='cat research.txt'
    for n in range(1,len(cmd)+1):states.append((cmd[:n],0,True,80))
    states += [(cmd,0,True,220),(cmd,1,True,270),(cmd,2,True,270),(cmd,3,True,1800),(cmd,3,False,550)]
    full=terminal(theme)
    (OUT/f'console-{theme}.svg').write_text(full)
    # 3x physical pixels; display size remains 720 CSS pixels in the README.
    png=cairosvg.svg2png(bytestring=full.encode(),scale=3)
    (OUT/f'console-{theme}-still.png').write_bytes(png)
    rgba=Image.open(io.BytesIO(png)).convert('RGBA')
    ref=Image.new('RGB',rgba.size,PALETTES[theme]['bg']); ref.paste(rgba,mask=rgba.getchannel('A'))
    palette=ref.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    frames=[]; durations=[]
    for command,visible,cursor,ms in states:
        rendered=cairosvg.svg2png(bytestring=terminal(theme,command,visible,cursor).encode(),scale=3)
        rgba=Image.open(io.BytesIO(rendered)).convert('RGBA')
        im=Image.new('RGB',rgba.size,PALETTES[theme]['bg']); im.paste(rgba,mask=rgba.getchannel('A'))
        frames.append(im.quantize(palette=palette,dither=Image.Dither.NONE)); durations.append(ms)
    frames[0].save(OUT/f'console-{theme}.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=1,optimize=True)
    print('Built console',theme,flush=True)

def strip(project,theme):
    p=PALETTES[theme]; i=int(project['id'])-1; ac=['purple','cyan','amber'][i]; c=p[ac]
    s=rect(.5,.5,759,87,p['panel'],11,p['line'])
    s+=rect(1,19,3,50,c,1.5)
    s+=rect(20,23,42,42,p[ac+'_bg'],10)
    s+=txt(41,49,project['id'],14,c,'mono','middle')
    assert measure(project['title'],20,'bold')<490, project['title']
    s+=txt(82,39,project['title'],20,p['text'],'bold')
    s+=txt(83,62,project['venue'],9.4,p['muted'],'mono')
    # Decorative research motifs, not empirical result plots.
    if i==0:
        nodes=[(650,22),(680,30),(711,18),(661,65),(694,61),(733,48)]
        for a,b in [(0,1),(0,3),(1,2),(1,4),(2,5),(3,4),(4,5)]:
            s+=line(*nodes[a],*nodes[b],p['line'],1.4)
        for j,(x,y) in enumerate(nodes):
            s+=f'<circle cx="{x}" cy="{y}" r="{3 if j%2 else 4}" fill="{c if j%2 else p[ac+"_bg"]}" stroke="{c}" stroke-width="1"/>'
    elif i==1:
        for k in range(3):
            s+=f'<path d="M640 {64-k*12} C666 {60-k*12},674 {26+k*5},696 {33+k*7} S724 56,739 {20+k*12}" fill="none" stroke="{c}" stroke-width="1.3" opacity="{.45+k*.2}"/>'
        s+=f'<circle cx="695" cy="40" r="3" fill="{c}"/>'
    else:
        s+=line(634,66,740,66,p['line'])
        for dx,op in [(0,.9),(18,.55),(33,.3)]:
            s+=f'<path d="M634 66 C{645+dx} 66,{646+dx} 23,{662+dx} 23 S{676+dx} 66,740 66" fill="none" stroke="{c}" stroke-width="1.6" opacity="{op}"/>'
    return svg(s,760,88,project['title']+' — '+project['venue'])

def small_project_assets(project,theme):
    p=PALETTES[theme]; i=int(project['id'])-1; ac=['purple','cyan','amber'][i]
    chip=rect(0,0,30,20,p[ac+'_bg'],4)+txt(15,14,project['id'],10.2,p[ac],'mono','middle')
    (OUT/f'index-{project["id"]}-{theme}.svg').write_text(svg(chip,30,20,'Project '+project['id']))
    badge_w=measure(project['venue'],9.3,'mono')+18
    s=rect(.5,2.5,badge_w,22,p[ac+'_bg'],5)
    s+=txt(9,17,project['venue'],9.3,p[ac],'mono')
    # A restrained line motif carries the project accent, without image-based titles.
    left=badge_w+16
    if i==0:
        for a,b in [((left+4,14),(left+30,7)),((left+4,14),(left+30,21)),((left+30,7),(left+56,14)),((left+30,21),(left+56,14))]:
            s+=line(*a,*b,p['line'])
        for x,y in [(left+4,14),(left+30,7),(left+30,21),(left+56,14)]:
            s+=f'<circle cx="{x}" cy="{y}" r="2" fill="{p[ac]}"/>'
    elif i==1:
        for j in range(2):s+=f'<path d="M{left} {10+j*7}C{left+18} {25+j*3},{left+34} {-6+j*9},{left+64} {11+j*7}" fill="none" stroke="{p[ac]}" stroke-width="1" opacity="{.5+.4*j}"/>'
    else:
        for j in range(2):s+=f'<path d="M{left} 23C{left+15+j*15} 23,{left+10+j*15} 4,{left+24+j*15} 4S{left+36+j*15} 23,{left+72} 23" fill="none" stroke="{p[ac]}" stroke-width="1" opacity="{.5+.4*j}"/>'
    (OUT/f'meta-{project["id"]}-{theme}.svg').write_text(svg(s,300,28,project['venue']))

# Names and official project links are retained from the existing profile.
GROUPS=[
 ('LLM & deep learning', [('pytorch','PyTorch','https://pytorch.org/'),('transformers','Transformers','https://huggingface.co/docs/transformers/'),('verl','verl','https://github.com/verl-project/verl'),('vllm','vLLM','https://github.com/vllm-project/vllm'),('tensorflow','TensorFlow','https://www.tensorflow.org/')]),
 ('Bayesian modeling & data science',[('numpyro','NumPyro','https://num.pyro.ai/'),('jax','JAX','https://docs.jax.dev/'),('scikit-learn','scikit-learn','https://scikit-learn.org/'),('numpy','NumPy','https://numpy.org/'),('pandas','pandas','https://pandas.pydata.org/'),('matplotlib','Matplotlib','https://matplotlib.org/'),('seaborn','Seaborn','https://seaborn.pydata.org/')]),
 ('Compute & development',[('slurm','Slurm / HPC','https://slurm.schedmd.com/'),('linux','Linux','https://www.kernel.org/'),('shell','Bash / Zsh','https://www.gnu.org/software/bash/'),('docker','Docker','https://www.docker.com/'),('gcp','Google Cloud','https://cloud.google.com/compute'),('git','Git','https://git-scm.com/')]),
 ('Languages',[('python','Python','https://www.python.org/'),('cpp','C++','https://isocpp.org/'),('c','C','https://www.iso.org/standard/82075.html'),('sql','SQL','https://www.postgresql.org/docs/current/tutorial-sql.html'),('r','R','https://www.r-project.org/'),('matlab','MATLAB','https://www.mathworks.com/products/matlab.html')]),
 ('Databases',[('postgresql','PostgreSQL','https://www.postgresql.org/'),('mysql','MySQL','https://www.mysql.com/')])]

tool_config=ROOT/'design/toolchain.json'
if tool_config.exists():
    GROUPS=[(group['heading'],[(t['key'],t['label'],t['url']) for t in group['tools']]) for group in json.loads(tool_config.read_text())]

def make_tile(key,label,theme):
    p=PALETTES[theme]; path=SOURCE/f'logo-{key}.svg'
    if not path.exists():path=SOURCE/f'logo-{key}-{theme}.svg'
    art=cairosvg.svg2png(url=str(path),output_width=480)
    mark=Image.open(io.BytesIO(art)).convert('RGBA')
    bbox=mark.getchannel('A').getbbox()
    if bbox:mark=mark.crop(bbox)
    # Aspect ratios are preserved; all marks share a centered 64 x 38 optical box.
    mark.thumbnail((64*3,38*3),Image.Resampling.LANCZOS)
    im=Image.new('RGBA',(84*3,76*3),(0,0,0,0))
    im.alpha_composite(mark,((84*3-mark.width)//2,4*3+(38*3-mark.height)//2))
    labelsvg=svg(txt(42,63,label,11.2,p['muted'],'regular','middle'),84,76,label)
    labelim=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=labelsvg.encode(),scale=3))).convert('RGBA')
    im.alpha_composite(labelim); im.save(OUT/f'tool-{key}-{theme}.png',optimize=True)

def picture(stem,alt,width,ext='svg',height=None):
    s=f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/profile-v2/{stem}-dark.{ext}"><source media="(prefers-color-scheme: light)" srcset="assets/profile-v2/{stem}-light.{ext}"><img src="assets/profile-v2/{stem}-light.{ext}" alt="{html.escape(alt,quote=True)}" width="{width}"'
    if height:s+=f' height="{height}"'
    return s+'></picture>'

def nav(label,theme,width):
    p=PALETTES[theme]
    s=rect(.5,.5,width-1,31,p['panel'],6,p['line'])
    s+=txt(12,20,label,11.5,p['text'],'medium')
    s+=f'<path d="M{width-21} 11h9v9M{width-12} 11l-10 10" fill="none" stroke="{p["purple"]}" stroke-width="1.2"/>'
    return svg(s,width,32,label)

def write_readme():
    W=CFG['display_width']
    navs=[('scholar','Google Scholar',137,'https://scholar.google.com/citations?user=-BT9-3AAAAAJ&hl=en'),('linkedin','LinkedIn',108,'https://www.linkedin.com/in/mdrysulkabir/'),('repositories','Repositories',136,'https://github.com/mdrkabir?tab=repositories')]
    for key,label,w,url in navs:
        for t in PALETTES:(OUT/f'nav-{key}-{t}.svg').write_text(nav(label,t,w))
    lines=['<!-- Complete profile. Upload README.md and the full assets/profile-v2/ directory. -->',
           '<!-- Text changes: edit the native paragraphs below. Artwork: design/profile.json + tools/build_profile.py. -->','',
           '<p>'+picture('console','Md Rysul Kabir. Computer Science Ph.D. student, Indiana University Bloomington. Research: LLM post-training and interpretability; reinforcement learning; hierarchical probabilistic models and MCMC.',W,'gif')+'</p>','',
           '<p>'+''.join('<a href="'+html.escape(url,quote=True)+'" title="'+label+'">'+picture('nav-'+key,label,w)+'</a> ' for key,label,w,url in navs)+'</p>','',
           CFG['bio'],'',
           '## research.registry','']
    for pr in CFG['projects']:
        lines+=['### '+picture('index-'+pr['id'],'Project '+pr['id'],30,'svg',20)+' '+pr['title'],'','<p>'+picture('meta-'+pr['id'],pr['venue'],300,'svg',28)+'</p>','',pr['description'],'']
        links=f'**[Paper ↗]({pr["paper"]})**'
        if pr['code']:links+=f' &nbsp; · &nbsp; **[Code ↗]({pr["code"]})**'
        links+=' &nbsp; · &nbsp; '+' · '.join('`'+t+'`' for t in pr['tags'])
        lines += [links,'']
    lines+=['## toolchain','', '<!-- Fixed-size transparent logo/caption assets wrap without HTML tables or ruby annotations. -->','']
    for name,items in GROUPS:
        lines += ['#### '+name,'','<p>']
        for key,label,url in items:
            lines += ['<a href="'+html.escape(url,quote=True)+'" title="'+html.escape(label,quote=True)+'">'+picture('tool-'+key,label,84,'png',76)+'</a>']
        lines+=['</p>','']
    lines+=['---','','<sub>Research focus: LLM post-training · model behavior · evaluation</sub>','']
    content='\n'.join(lines)
    (ROOT/'README.md').write_text(content)
    static=content.replace('console-dark.gif','console-dark-still.png').replace('console-light.gif','console-light-still.png')
    (ROOT/'README-static.md').write_text(static)
    (ROOT/'design/toolchain.json').write_text(json.dumps([{'heading':name,'tools':[{'key':k,'label':l,'url':u} for k,l,u in items]} for name,items in GROUPS],indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skip-animation',action='store_true')
    parser.add_argument('--assets-only',action='store_true',help='Keep existing README wording untouched')
    args=parser.parse_args()
    for theme in PALETTES:
        if not args.skip_animation:write_console(theme)
        for pr in CFG['projects']:small_project_assets(pr,theme)
        for _,items in GROUPS:
            for key,label,_ in items:make_tile(key,label,theme)
    if not args.assets_only:write_readme()
    print('Profile assets and README generated. Run tools/validate_profile.py next.')
