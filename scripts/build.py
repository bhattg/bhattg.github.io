#!/usr/bin/env python3
"""Build the site using only Python's standard library. Edit data/content.json."""
from pathlib import Path
from html import escape
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]; SITE=ROOT/'site'; D=json.loads((ROOT/'data/content.json').read_text())
H=json.loads((ROOT/'data/unsplash-highlights.json').read_text())
O=json.loads((ROOT/'data/photography-overview.json').read_text())
I=json.loads((ROOT/'data/image-variants.json').read_text())
C=json.loads((ROOT/'data/photo-captions.json').read_text())
P=json.loads((ROOT/'data/publications.json').read_text())
DIAGRAMS={p['image'] for p in D['publications']}
E=lambda s:escape(str(s),quote=True)
CV='/'+D['cv']
REPAIRS=json.loads((ROOT/'data/link-repairs.json').read_text())
def repair_links(markup):
 for item in REPAIRS:
  if not item.get('publication'): markup=markup.replace('href="'+E(item['original'])+'"','href="'+E(item['replacement'])+'"')
 return markup
def link(label,url,cls=''):
 return f'<a href="{E(url)}"'+(f' class="{cls}"' if cls else '')+f'>{label}</a>'
def asset_url(path):
 return '/'+path+'?v='+hashlib.sha256((SITE/path).read_bytes()).hexdigest()[:12]
def page(title,body,path='/',photo=False,description=None):
 nav=[('About','/#about'),('Publications','/#publications'),('Photography','/photography/'),('CV',CV)]
 navigation=''.join(link(label,url,'nav-link'+(' active' if (photo and label=='Photography') or (path=='/publications/' and label=='Publications') else '')) for label,url in nav)
 description=description or 'Gantavya Bhatt — PhD candidate at the University of Washington, Seattle. Research on data efficiency, large-scale models, and submodular optimization.'
 rendered=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} · Gantavya Bhatt</title><meta name="description" content="{E(description)}">
<link rel="canonical" href="{D['url'].rstrip('/')}{path}"><meta property="og:title" content="{E(title)} · Gantavya Bhatt"><meta property="og:description" content="{E(description)}"><meta property="og:type" content="website"><meta property="og:url" content="{D['url'].rstrip('/')}{path}"><meta property="og:image" content="{D['url'].rstrip('/')}/{D['profile_image']}">
<meta name="theme-color" content="#faf7f2"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><script src="{asset_url('assets/site.js')}"></script><link rel="stylesheet" href="{asset_url('assets/style.css')}"></head>
<body class="{'photography-page' if photo else 'academic-page'}"><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><a class="wordmark" href="/" aria-label="Gantavya Bhatt home"><span class="brand-mark" aria-hidden="true">gb.</span><span>Gantavya Bhatt</span></a><nav aria-label="Main navigation">{navigation}</nav><button class="theme-toggle" type="button" aria-label="Switch to night theme" hidden><svg class="theme-icon-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 13.2A8.5 8.5 0 0 1 10.8 3.5 8.5 8.5 0 1 0 20.5 13.2Z"/></svg><svg class="theme-icon-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="3.5"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg><span class="theme-label">Night</span></button></div></header>
<main id="main">{body}</main><footer class="site-footer"><div><a class="footer-name" href="/">Gantavya Bhatt</a><span>University of Washington, Seattle</span></div><div>{link('Email','mailto:'+D['email'])}{link('Google Scholar',next(s['url'] for s in D['social'] if s['label']=='Google Scholar'))}{link('Back to top ↑','#main')}</div></footer></body></html>'''
 return repair_links(rendered)
def write(path,html):
 p=SITE/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(html)
def img(src,alt,cls='',eager=False,sizes=None):
 meta=I[src];variants=meta['variants'];fallback=min(variants,key=lambda v:abs(v['width']-960))
 if sizes is None:
  if cls=='portrait':sizes='(max-width: 700px) 116px, (max-width: 900px) 180px, 208px'
  elif src in DIAGRAMS:sizes='(max-width: 700px) 157px, 159px'
  elif cls=='landscape':sizes='(max-width: 700px) calc(100vw - 40px), 503px'
  elif eager:sizes='(max-width: 700px) calc(100vw - 40px), (max-width: 1032px) calc(100vw - 72px), 960px'
  else:sizes='(max-width: 700px) calc(100vw - 40px), (max-width: 1032px) calc(50vw - 48.5px), 468px'
 srcset=', '.join('/'+v['path']+' '+str(v['width'])+'w' for v in variants)
 return f'<img src="/{E(fallback["path"])}" srcset="{E(srcset)}" sizes="{E(sizes)}" width="{meta["width"]}" height="{meta["height"]}" data-original-src="/{E(src)}" alt="{E(alt)}" class="{cls}" loading="{"eager" if eager else "lazy"}" decoding="async"'+(' fetchpriority="high"' if eager else '')+'>'
# Biography remains from the original public site; publications use the verified catalog.
bio=D['biography'];social=[]
for s in D['social']:
 label={'LinkedIN':'LinkedIn'}.get(s['label'],s['label'])
 social.append(link(E(label), CV if label=='CV' else s['url']))
hero=f'''<section class="profile wrap" id="about"><aside class="profile-aside">{img(D['profile_image'],'Gantavya Bhatt','portrait',True)}<div class="social-links" aria-label="Professional profiles">{''.join(social)}</div></aside><div class="profile-copy"><h1>Gantavya Bhatt</h1><p class="affiliation">PhD candidate · University of Washington, Seattle</p><div class="biography" id="research"><p>{bio[0]}</p><p class="job-market">{bio[1]}</p><p>{bio[2]}</p></div></div></section>'''
news=''
for n in D['news']:
 match=re.match(r'\[([^\]]+)\]\s*(.*)',n['html']); date=match[1] if match else '';text=match[2] if match else n['html']
 news+=f'<li><span class="news-date">{date}</span><span>{text}</span></li>'
news=f'<section class="news-section wrap" id="news"><div class="section-heading"><h2>Recent updates</h2></div><ul class="news-list">{news}</ul></section>'
def author_markup(name):
 text=E(name).replace('Gantavya Bhatt','<strong>Gantavya Bhatt</strong>')
 return re.sub(r'([*†])$',r'<sup>\1</sup>',text)
def publication_entry(p,heading):
 authors=', '.join(author_markup(name) for name in p['authors'])
 resources=''.join(link(E(item['label']),item['url']) for item in p['links'])
 note=f'<p class="pub-note">{author_markup(p["note"])}</p>' if p.get('note') else ''
 return f'<article class="publication" id="{E(p["id"])}" data-year="{p["year"]}"><h{heading} class="publication-title">{link(E(p["title"]),p["links"][0]["url"])}</h{heading}><p class="pub-authors">{authors}</p><p class="pub-venue">{E(p["venue"])}</p>{note}<div class="pub-links" aria-label="Links for {E(p["title"])}">{resources}</div></article>'
def publication_catalog(home=False):
 heading=3 if home else 2
 out=''
 papers=[p for p in P['records'] if p['kind']=='paper']
 for year in sorted({p['year'] for p in papers},reverse=True):
  rows=''.join(publication_entry(p,heading+1) for p in sorted(papers,key=lambda p:p['date'],reverse=True) if p['year']==year)
  out+=f'<section class="publication-year" aria-labelledby="publications-{year}"><h{heading} class="publication-group-label" id="publications-{year}">{year}</h{heading}><div class="publication-list">{rows}</div></section>'
 notes=''.join(publication_entry(p,heading+1) for p in P['records'] if p['kind']=='notes')
 if notes:out+=f'<section class="publication-year" aria-labelledby="publication-notes"><h{heading} class="publication-group-label" id="publication-notes">Notes</h{heading}><div class="publication-list">{notes}</div></section>'
 return out+'<p class="publication-key">* and † mark equal contribution within the indicated groups.</p>'
publications=f'<section class="publications-section wrap" id="publications"><div class="section-heading publication-heading"><div><h1>Publications</h1><p class="section-description">Research papers, technical reports, and preprints.</p></div>{link("Google Scholar ↗",P["profile_url"],"text-link")}</div>{publication_catalog()}</section>'
write('publications/index.html',page('Publications',publications,'/publications/',description='Research publications, technical reports, and preprints by Gantavya Bhatt on data selection, representation learning, and efficient machine learning.'))
home_publications=f'<section class="home-publications wrap" id="publications"><div class="section-heading publication-heading"><div><h2>Publications</h2><p class="section-description">Research papers, technical reports, and preprints.</p></div>{link("All publications ↗","/publications/","text-link")}</div>{publication_catalog(home=True)}</section>'
photo=f'<section class="photo-teaser wrap"><a class="landscape-link" href="/photography/">{img(D["landscape_image"],"Mountain landscape from Gantavya Bhatt’s original website","landscape")}</a><div><h2>Outside research</h2><p>Photography, hiking, and the Pacific Northwest.</p>{link("Explore photography ↗","/photography/","text-link")}</div></section>'
contact=f'<section class="contact-section wrap" id="contact"><h2>Contact</h2><a class="contact-email" href="mailto:{D["email"]}">{D["email"]}</a></section>'
write('index.html',page('Research',hero+news+home_publications+photo+contact))

def collections(current):
 entries=[('/photography/','Overview'),('/photography/highlights-of-2025/','Highlights of 2025'),('/photography/highlights-of-2024/','Highlights of 2024'),('/photography/highlights-of-2023/','Highlights of 2023'),('/photography/mountains-by-the-day/','Mountains by the Day'),('/photography/mountains-by-the-night/','Mountains by the Night')]
 return '<nav class="collection-nav" aria-label="Photography collections">'+''.join(f'<a href="{u}"'+(' aria-current="page"' if current==u else '')+f'>{t}</a>' for u,t in entries)+'</nav>'
def gallery_content(g):
 es=g['events']
 # Put the original essay before the photographs, then include its opening
 # night-sky photo in the first group. Photo order and all source copy survive.
 if g['slug']=='photography/highlights-of-2023':
  first_image=next(i for i,e in enumerate(es) if e['type']=='img')
  first_section=next(i for i,e in enumerate(es) if i>first_image and e['type'] in ['h2','h3'])
  caption_end=first_image+1
  while caption_end<first_section and es[caption_end]['type']=='p' and len(es[caption_end]['text'])<240 and caption_end<=first_image+2:caption_end+=1
  es=[*es[:first_image],*es[caption_end:first_section],es[first_section],*es[first_image:caption_end],*es[first_section+1:]]
 out='';pending=[];i=0;first=True
 def flush():
  nonlocal out
  if pending:out+='<div class="gallery-grid">'+''.join(pending)+'</div>';pending.clear()
 while i<len(es):
  e=es[i]
  if e['type']=='img':
   captions=[];j=i+1
   while j<len(es) and es[j]['type']=='p' and len(es[j]['text'])<240 and len(captions)<2:
    captions.append(es[j]);j+=1
   caption=C.get(e['src'],captions[0]['text'] if captions else 'Photograph from '+g['title'])
   alt=' — '.join([caption]+[c['text'] for c in captions[1:]])
   cap='<figcaption><p>'+E(caption)+'</p>'+''.join(f'<p>{c["html"]}</p>' for c in captions[1:])+'</figcaption>'
   ratio=I[e['src']]['width']/I[e['src']]['height']
   pending.append(f'<figure class="gallery-figure" style="--photo-ratio:{ratio:.8f}">{link(img(e["src"],alt,eager=first),"/"+e["src"],"image-link")}{cap}</figure>');i=j;first=False;continue
  flush()
  if e['type'] in ['h1','h2','h3']:
   # First heading becomes the page title above the collection navigation.
   if i>0:out+=f'<h2 class="gallery-section-title">{e["html"]}</h2>'
  elif e['text']:
   out+=f'<div class="gallery-prose"><p>{e["html"]}</p></div>'
  i+=1
 flush()
 return out
for g in D['galleries']:
 if g['slug']=='photography':continue
 if any(h['slug']==g['slug'] for h in H['galleries']):continue
 url='/'+g['slug']+'/'
 title='Photography' if g['slug']=='photography' else g['title']
 background=''.join('<figure class="gallery-figure">'+img(src,'Header photograph from '+g['title'])+'</figure>' for src in g.get('backgrounds',[]))
 subtitle='<p class="section-description">Highlights of 2023</p>' if g['slug']=='photography' else ''
 body=f'<section class="gallery-header wrap"><h1>{E(title)}</h1>{subtitle}{collections(url)}</section><div class="gallery wrap">{background}{gallery_content(g)}</div>'
 write(g['slug']+'/index.html',page(title,body,url,True,'Photography by Gantavya Bhatt — '+g['title']+'.'))
def unsplash_figure(p,featured=False):
 caption=f'<p>{E(C.get(p["local_path"],p["caption"]))}</p>'
 if p.get('location'):caption+=f'<p>{E(p["location"])}</p>'
 image_markup=img(p['local_path'],C.get(p['local_path'],p['alt']),eager=featured)
 image=link(image_markup,'/'+p['local_path'],'image-link')
 ratio=I[p['local_path']]['width']/I[p['local_path']]['height']
 return f'<figure class="gallery-figure" style="--photo-ratio:{ratio:.8f}" id="photo-{E(p["id"])}" data-posted-at="{E(p["posted_at"])}">{image}<figcaption>{caption}</figcaption></figure>'
photo_lookup={p['id']:p for g in H['galleries'] for p in g['photos']}
overview_intro='<div class="gallery-note wrap"><div class="gallery-note-copy">'+''.join(f'<p>{E(p)}</p>' for p in O['introduction'])+'</div></div>'
overview_selections=''
for i,selection in enumerate(O['selections']):
 p=photo_lookup[selection['photo_id']]
 image_markup=img(p['local_path'],p['alt'],eager=i<3,sizes='(max-width: 700px) calc(100vw - 40px), (max-width: 900px) calc(50vw - 48px), 304px')
 overview_selections+=f'<article class="portfolio-selection"><a href="{E(selection["href"])}" class="portfolio-link">{image_markup}<h2>{E(selection["title"])}</h2></a><p>{E(selection["summary"])}</p></article>'
overview_body=f'<section class="gallery-header wrap"><h1>{E(O["title"])}</h1>{collections("/photography/")}</section>{overview_intro}<section class="portfolio-grid wrap" aria-label="Selected photography">{overview_selections}</section>'
write('photography/index.html',page('Photography',overview_body,'/photography/',True,'Photography by Gantavya Bhatt — mountains, night skies, forests, and city skylines.'))
for g in H['galleries']:
 url='/'+g['slug']+'/'
 intro='<div class="gallery-note wrap"><div class="gallery-note-copy">'+''.join(f'<p>{E(p)}</p>' for p in g['introduction'])+'</div></div>'
 gallery=''
 for i,p in enumerate(sorted(g['photos'],key=lambda p:(p['posted_at'],p['id']))):
  gallery+=unsplash_figure(p,i==0)
 body=f'<section class="gallery-header wrap"><h1>{E(g["title"])}</h1>{collections(url)}</section>{intro}<div class="gallery wrap"><div class="gallery-grid">{gallery}</div></div>'
 write(g['slug']+'/index.html',page(g['title'],body,url,True,'Photography by Gantavya Bhatt — highlights shared in '+str(g['year'])+'.'))
# Existing Google Sites home and bookmarks get useful destinations under the new domain.
write('home/index.html','<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url=/"><title>Gantavya Bhatt</title><link rel="canonical" href="https://bhattg.github.io/"></head><body><p><a href="/">Gantavya Bhatt — Home</a></p></body></html>')
write('404.html',page('Page not found','<section class="wrap error-page"><p class="eyebrow">404</p><h1>Page not found.</h1><p>The page may have moved.</p><p><a class="button" href="/">Return home</a></p><p><a href="/photography/">Browse photography</a></p></section>','/404.html'))
(SITE/'.nojekyll').touch()
urls=list(dict.fromkeys(['/','/publications/',*[('/'+g['slug']+'/') for g in D['galleries']],*[('/'+g['slug']+'/') for g in H['galleries']]]))
(SITE/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+D['url'].rstrip('/')+u+'</loc></url>' for u in urls)+'</urlset>')
(SITE/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://bhattg.github.io/sitemap.xml\n')
print('Built',len(list(SITE.rglob('*.html'))),'HTML pages in',SITE)
