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
OUT = ROOT / 'assets' / 'profile-v4'
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

# Both header panels use the SAME size. Inline images wrap naturally on phones;
# no device-specific <source> branches or website-only layout CSS are needed.
PANEL_W, PANEL_H = 312, 250
SCALE=3

def console_panel(theme,command=None,visible=3,cursor=False,scene=1):
    p=PALETTES[theme]; w,h=PANEL_W,PANEL_H
    block=CFG['console_scenes'][scene]
    if command is None: command=block['command']
    output=block['lines']
    if not 0 <= visible <= len(output):
        raise ValueError('Invalid visible line count')
    colors=block.get('colors',['purple','cyan','amber'])
    if len(output)>3 or len(colors)!=len(output):
        raise ValueError('The compact console supports up to three output lines')
    s=rect(.5,.5,w-1,h-1,p['panel'],10,p['line'])
    s+='<path d="M10 1H302Q311 1 311 10V31H1V10Q1 1 10 1Z" fill="'+p['bar']+'"/>'
    for cx,c in [(15,'#CD8494'),(26,'#BC9B5F'),(37,'#61A49B')]:s+=f'<circle cx="{cx}" cy="16" r="2.5" fill="{c}"/>'
    s+=txt(50,19,'mdrkabir / research.console',8.1,p['muted'],'mono')
    s+=txt(17,68,CFG['name'],26,p['text'],'bold')
    s+=txt(18,92,CFG['role'],11.5,p['muted'])
    s+=txt(18,109,CFG['institution'],11.5,p['muted'])
    prompt='rysul@research:~$'
    s+=txt(18,145,prompt,10.2,p['cyan'],'mono')
    x=18+measure(prompt,10.2,'mono')+8
    s+=txt(x,145,command,10.2,p['text'],'mono')
    if cursor:s+=rect(x+measure(command,10.2,'mono')+2,136,4.5,10,p['faint'])
    if x+measure(command,10.2,'mono')+7>294:
        raise ValueError('Console command is too long: '+command)
    for i in range(visible):
        key=colors[i]; y=170+21*i
        s+=rect(18,y-9,2,11,p[key],1)
        if measure(output[i],10.4,'mono')>267:
            raise ValueError('Console output is too long: '+output[i])
        s+=txt(27,y,output[i],10.4,p[key],'mono')
    s+=line(18,230,294,230,p['line'])
    s+=txt(18,243,'learning methods → model behavior',8,p['faint'],'mono')
    return svg(s,w,h,'Animated research console — '+CFG['name'])

def focus_panel(theme):
    p=PALETTES[theme]; w,h=PANEL_W,PANEL_H
    s=rect(.5,.5,w-1,h-1,p['panel'],10,p['line'])
    s+='<path d="M10 1H302Q311 1 311 10V31H1V10Q1 1 10 1Z" fill="'+p['bar']+'"/>'
    s+=txt(17,19,'research.focus',9,p['muted'],'mono')
    for i,block in enumerate(CFG['focus']):
        color=['purple','cyan','amber'][i]; y=46+i*59
        s+=rect(13,y,286,52,p[color+'_bg'],7)
        # Title and subtitle share one center; numbers have their own fixed column.
        cx=(47+299)/2
        s+=txt(29,y+29,f'{i+1:02d}',10,p[color],'mono','middle')
        s+=line(47,y+13,47,y+39,p['line'])
        assert measure(block['title'],12,'bold')<231
        s+=txt(cx,y+21,block['title'],12,p['text'],'bold','middle')
        sub=' '.join(block['subtitle'])
        assert measure(sub,10.2)<231, sub
        s+=txt(cx,y+38,sub,10.2,p['muted'],'regular','middle')
    s+=line(18,230,294,230,p['line'])
    s+=txt(18,243,'Bloomington, Indiana',8,p['faint'],'mono')
    return svg(s,w,h,'Research focus: '+'; '.join(b['title']+' — '+' '.join(b['subtitle']) for b in CFG['focus']))

def raster(svg_text):
    rgba=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg_text.encode(),scale=SCALE))).convert('RGBA')
    # Do not quantize onto transparency: blend around the corner using theme bg.
    return rgba

def console_timeline():
    """Return every frame's semantic state; timings are in milliseconds.

    A complete whoami output is the opening frame so a thumbnail is meaningful.
    The loop then types research, selected work, and whoami again. Completed
    outputs pause for reading. The closing whoami flows into the first frame.
    """
    scenes=CFG['console_scenes']
    if [b['id'] for b in scenes]!=['identity','research','selected-work']:
        raise ValueError('Expected identity, research, selected-work scenes')
    def state(i,command,visible,cursor,ms,phase):
        if ms<=0 or ms%10:
            raise ValueError('GIF frame timing must be a positive multiple of 10ms')
        return dict(scene=i,scene_id=scenes[i]['id'],command=command,visible=visible,
                    cursor=cursor,duration_ms=ms,phase=phase)
    states=[state(0,scenes[0]['command'],3,False,scenes[0]['hold_ms'],'hold')]
    for i in [1,2,0]:
        command=scenes[i]['command']
        states.append(state(i,'',0,True,220,'clear'))
        for n in range(1,len(command)+1):
            states.append(state(i,command[:n],0,True,70,'type'))
        states.append(state(i,command,0,True,200,'execute'))
        for n in range(1,4):
            states.append(state(i,command,n,True,220,'reveal'))
        if i!=0:
            states.append(state(i,command,3,False,scenes[i]['hold_ms'],'hold'))
            states.append(state(i,command,3,True,350,'cursor'))
            states.append(state(i,command,3,False,350,'cursor'))
    return states

def write_console(theme,include_focus=True):
    static_id=CFG.get('console_static_scene','research')
    scene_ids=[b['id'] for b in CFG['console_scenes']]
    static_index=scene_ids.index(static_id)
    full=console_panel(theme,scene=static_index)
    (OUT/f'console-{theme}.svg').write_text(full)
    raster(full).save(OUT/f'console-{theme}-still.png')
    def flatten(rgba):
        im=Image.new('RGB',rgba.size,PALETTES[theme]['bg'])
        im.paste(rgba,mask=rgba.getchannel('A'))
        return im
    # Derive one palette from all three completed scenes, avoiding palette flicker.
    panels=[flatten(raster(console_panel(theme,scene=i,cursor=True))) for i in range(3)]
    atlas=Image.new('RGB',(panels[0].width*3,panels[0].height))
    for i,im in enumerate(panels):atlas.paste(im,(i*im.width,0))
    palette=atlas.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    states=console_timeline()
    frames=[];durations=[]
    for st in states:
        rgba=raster(console_panel(theme,st['command'],st['visible'],st['cursor'],scene=st['scene']))
        frames.append(flatten(rgba).quantize(palette=palette,dither=Image.Dither.NONE))
        durations.append(st['duration_ms'])
    frames[0].save(OUT/f'console-{theme}.gif',save_all=True,append_images=frames[1:],
                  duration=durations,loop=0,disposal=1,optimize=True)
    if include_focus:
        foc=focus_panel(theme)
        (OUT/f'focus-{theme}.svg').write_text(foc)
        raster(foc).save(OUT/f'focus-{theme}.png')
    print('Built three-scene animation',theme,'('+str(sum(durations)/1000)+'s)',flush=True)

def nav(key,label,theme,width):
    import xml.etree.ElementTree as ET
    p=PALETTES[theme]; root=ET.parse(ROOT/f'design/navigation-icons/{key}.svg').getroot()
    view=[float(v) for v in root.attrib['viewBox'].split()]; iw,ih=view[2:]
    paths=''.join(ET.tostring(el,encoding='unicode') for el in root if el.tag.endswith('path'))
    color=('#0A66C2' if key=='linkedin' else '#4285F4' if key=='scholar' else p['text'])
    s=rect(.5,.5,width-1,29,p['panel'],5,p['line'])
    scale=14/max(iw,ih); x=10+(14-iw*scale)/2; y=8+(14-ih*scale)/2
    s+=f'<g fill="{color}" transform="translate({x},{y}) scale({scale})">{paths}</g>'
    s+=txt(31,19,label,11,p['text'],'medium')
    assert 31+measure(label,11,'medium')<=width-8
    return svg(s,width,30,label)

# Small project metadata carries the lavender/cyan/amber accent. Titles and their
# numbers are native text on a single shared baseline, not a mixed image/table.
def meta(project,theme):
    p=PALETTES[theme];i=int(project['id'])-1;key=['purple','cyan','amber'][i];c=p[key]
    venue=project['venue']; width=measure(venue,9,'mono')+16
    s=rect(.5,.5,width,21,p[key+'_bg'],4)
    s+=txt(8,14.5,venue,9,c,'mono')
    x=width+12
    if i==0:
        for a,b in [((x,11),(x+16,5)),((x,11),(x+16,17)),((x+16,5),(x+32,11)),((x+16,17),(x+32,11))]:s+=line(*a,*b,p['line'])
        for a,b in [(x,11),(x+16,5),(x+16,17),(x+32,11)]:s+=f'<circle cx="{a}" cy="{b}" r="1.8" fill="{c}"/>'
    elif i==1:
        for j in range(2):s+=f'<path d="M{x} {6+7*j} C{x+17} {25+3*j},{x+25} {-6+7*j},{x+44} {8+7*j}" fill="none" stroke="{c}" opacity="{.45+.4*j}"/>'
    else:
        for j in range(2):s+=f'<path d="M{x} 19 C{x+12+j*9} 19,{x+9+j*9} 3,{x+18+j*9} 3 S{x+29+j*9} 19,{x+45} 19" fill="none" stroke="{c}" opacity="{.5+.4*j}"/>'
    return svg(s,260,22,venue)

GROUPS=[(g['heading'],[(t['key'],t['label'],t['url']) for t in g['tools']]) for g in json.loads((ROOT/'design/toolchain.json').read_text())]

def make_tile(key,label,theme):
    p=PALETTES[theme];path=SOURCE/f'logo-{key}.svg'
    if not path.exists():path=SOURCE/f'logo-{key}-{theme}.svg'
    mark=Image.open(io.BytesIO(cairosvg.svg2png(url=str(path),output_width=480))).convert('RGBA')
    bbox=mark.getchannel('A').getbbox()
    if bbox:mark=mark.crop(bbox)
    mark.thumbnail((56*3,32*3),Image.Resampling.LANCZOS)
    im=Image.new('RGBA',(80*3,66*3))
    im.alpha_composite(mark,((240-mark.width)//2,3*3+(32*3-mark.height)//2))
    assert measure(label,10.5)<77
    labels=svg(txt(40,54,label,10.5,p['muted'],'regular','middle'),80,66,label)
    im.alpha_composite(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=labels.encode(),scale=3))).convert('RGBA'))
    im.save(OUT/f'tool-{key}-{theme}.png',optimize=True)

def picture(stem,alt,width,ext='svg',height=None):
    s=f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/profile-v4/{stem}-dark.{ext}"><source media="(prefers-color-scheme: light)" srcset="assets/profile-v4/{stem}-light.{ext}"><img src="assets/profile-v4/{stem}-light.{ext}" alt="{html.escape(alt,quote=True)}" width="{width}"'
    if height:s+=f' height="{height}"'
    return s+'></picture>'

def write_readme():
    navs=[('scholar','Google Scholar',126,'https://scholar.google.com/citations?user=-BT9-3AAAAAJ&hl=en'),('linkedin','LinkedIn',100,'https://www.linkedin.com/in/mdrysulkabir/'),('repositories','Repositories',122,'https://github.com/mdrkabir?tab=repositories')]
    for key,label,w,url in navs:
        for t in PALETTES:(OUT/f'nav-{key}-{t}.svg').write_text(nav(key,label,t,w))
    lines=['<!-- Self-contained profile: upload README.md and assets/profile-v4/. -->',
      '<!-- Two equal-sized panels wrap naturally; no mobile-image selection or custom CSS. -->','',
      '<p>'+picture('console',CFG['name']+' — animated research console',PANEL_W,'gif',PANEL_H)+' '+picture('focus','Large language models: Post-training · Interpretability. Reinforcement learning: Policy optimization · Reward shaping. Probabilistic modeling: Hierarchical models · MCMC.',PANEL_W,'svg',PANEL_H)+'</p>','',
      '<p>'+' '.join('<a href="'+html.escape(url,quote=True)+'" title="'+label+'">'+picture('nav-'+key,label,w,'svg',30)+'</a>' for key,label,w,url in navs)+'</p>','',CFG['bio'],'','## research.registry','']
    for project in CFG['projects']:
        lines += ['### '+project['id']+' · '+project['title'],'', '<p>'+picture('meta-'+project['id'],project['venue'],260,'svg',22)+'</p>','',project['description'],'']
        links=f'**[Paper ↗]({project["paper"]})**'
        if project.get('code'):links+=f' &nbsp; · &nbsp; **[Code ↗]({project["code"]})**'
        lines += [links+' &nbsp; · &nbsp; '+' · '.join('`'+t+'`' for t in project['tags']),'']
    lines += ['## toolchain','','<!-- Tool marks retain the prior kit’s artwork; provenance is in ICON-SOURCES.md. -->','']
    for heading,tools in GROUPS:
        lines += ['#### '+heading,'','<p>']
        lines += ['<a href="'+html.escape(url,quote=True)+'" title="'+html.escape(label,quote=True)+'">'+picture('tool-'+key,label,80,'png',66)+'</a>' for key,label,url in tools]
        lines += ['</p>','']
    lines += ['---','','<sub>Research focus: LLM post-training · model behavior · evaluation</sub>','']
    content='\n'.join(lines)
    (ROOT/'README.md').write_text(content)
    (ROOT/'README-static.md').write_text(content.replace('console-dark.gif','console-dark-still.png').replace('console-light.gif','console-light-still.png'))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skip-animation',action='store_true')
    parser.add_argument('--animation-only',action='store_true',help='Rebuild only the console GIFs and stills; preserve README, focus, navigation, and toolchain')
    parser.add_argument('--assets-only',action='store_true',help='Preserve hand-edited README text')
    args=parser.parse_args()
    if args.animation_only:
        if args.skip_animation:
            parser.error('--animation-only cannot be combined with --skip-animation')
        for theme in PALETTES:write_console(theme,include_focus=False)
        print('Console-only rebuild complete. All other assets and README preserved.')
        raise SystemExit(0)
    for theme in PALETTES:
        if not args.skip_animation:write_console(theme)
        for pr in CFG['projects']:(OUT/f'meta-{pr["id"]}-{theme}.svg').write_text(meta(pr,theme))
        for _,tools in GROUPS:
            for key,label,_ in tools:make_tile(key,label,theme)
    if not args.assets_only:write_readme()
    print('Built local display assets. No font files or external images are used.')
