from pathlib import Path
import base64,mimetypes,re
from markdown_it import MarkdownIt
ROOT=Path(__file__).resolve().parents[1]
body=MarkdownIt('commonmark',{'html':True}).render((ROOT/'README.md').read_text())
# Public output is generated from README, not an independent mockup layout.
css='''
*{box-sizing:border-box}html{color-scheme:light;--bg:#fff;--fg:#1f2328;--muted:#59636e;--line:#d1d9e0;--link:#0969da;--code:#eff1f3}
@media(prefers-color-scheme:dark){html:not([data-theme=light]){color-scheme:dark;--bg:#0d1117;--fg:#f0f6fc;--muted:#9198a1;--line:#3d444d;--link:#4493f8;--code:#252b33}}
html[data-theme=dark]{color-scheme:dark;--bg:#0d1117;--fg:#f0f6fc;--muted:#9198a1;--line:#3d444d;--link:#4493f8;--code:#252b33}
body{margin:0;background:var(--bg);color:var(--fg);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}
.preview-controls{max-width:854px;margin:16px auto 0;padding:0 32px;display:flex;justify-content:space-between;gap:12px;color:var(--muted);font-size:12px;line-height:1.4}
.preview-controls button{border:1px solid var(--line);border-radius:5px;padding:5px 9px;background:var(--bg);color:var(--fg);font:inherit;cursor:pointer}
.markdown-body{max-width:854px;margin:16px auto;padding:32px;font-size:16px;line-height:1.5;word-wrap:break-word}
.markdown-body>:first-child{margin-top:0!important}.markdown-body>:last-child{margin-bottom:0!important}
.markdown-body h2{font-size:1.5em;font-weight:600;line-height:1.25;margin:24px 0 16px;padding-bottom:.3em;border-bottom:1px solid var(--line)}
.markdown-body h3{font-size:1.25em;font-weight:600;line-height:1.25;margin:24px 0 16px}
.markdown-body h4{font-size:1em;font-weight:600;line-height:1.25;margin:24px 0 16px}
.markdown-body p{margin:0 0 16px}.markdown-body img{max-width:100%;height:auto;vertical-align:baseline;box-sizing:content-box}
.markdown-body a{color:var(--link);text-decoration:none}.markdown-body a:hover{text-decoration:underline}
.markdown-body strong{font-weight:600}.markdown-body code{padding:.2em .4em;font-size:85%;white-space:break-spaces;background:var(--code);border-radius:6px;font-family:ui-monospace,SFMono-Regular,Consolas,monospace}
.markdown-body sub{font-size:12px;position:relative;vertical-align:baseline;bottom:-.25em}.markdown-body hr{height:1px;background:var(--line);border:0;margin:24px 0}
@media(max-width:600px){.markdown-body{padding:16px;margin:16px auto}.preview-controls{padding:0 16px}.preview-controls span{max-width:235px}}
'''
bar='<div class="preview-controls"><span>Local rendering of the included README<br>Not a live GitHub screenshot</span><div><button onclick="setTheme(\'light\')">Light</button> <button onclick="setTheme(\'dark\')">Dark</button></div></div>'
script='''document.querySelectorAll('source').forEach(s=>s.dataset.theme=s.media.includes('dark')?'dark':'light');
function setTheme(value){document.documentElement.dataset.theme=value;document.querySelectorAll('picture').forEach(p=>{let s=p.querySelector('source[data-theme=\"'+value+'\"]');let img=p.querySelector('img');if(s){p.querySelectorAll('source').forEach(el=>el.media='not all');img.src=s.srcset}})}
'''
head='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Option C — compact layout</title><style>'+css+'</style></head><body>'
tail='</article><script>'+script+'</script></body></html>'
page=head+bar+'<article class="markdown-body">'+body+tail
(ROOT/'PREVIEW-local.html').write_text(page)
# The single-file preview embeds ONLY artwork, not fonts or external code.
def embed(m):
 attr,rel=m.group(1),m.group(2)
 path=ROOT/rel
 mime=mimetypes.guess_type(path)[0] or 'application/octet-stream'
 return attr+'="data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()+'"'
self_contained=re.sub(r'(src|srcset)="(assets/[^\"]+)"',embed,page)
(ROOT/'PREVIEW.html').write_text(self_contained)
# QA page uses normal media selection, no Javascript theme overrides.
(ROOT/'preview').mkdir(exist_ok=True)
(ROOT/'preview/qa.html').write_text(page.replace('assets/','../assets/'))
print('wrote previews')
