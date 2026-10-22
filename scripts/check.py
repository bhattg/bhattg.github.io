#!/usr/bin/env python3
"""Check local links, anchors, image signatures, and migrated copy; no network."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,sys,hashlib
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site'
class Doc(HTMLParser):
 def __init__(self,markup):
  super().__init__(convert_charrefs=True);self.attrs=[];self.ids=[];self.texts=[];self.h1=0;self.feed(markup)
 def handle_starttag(self,t,a):
  a=dict(a);self.attrs.append((t,a));self.h1+=t=='h1'
  if 'id'in a:self.ids.append(a['id'])
 def handle_data(self,s):self.texts.append(s)
 def text(self):return re.sub(r'\s+',' ',''.join(self.texts)).strip()
def plain(s):return Doc(s).text()
docs={p:Doc(p.read_text()) for p in SITE.rglob('*.html')};errors=[];refs=0;coverage=0
for p,d in docs.items():
 # Google ownership files must retain Google's exact verification response.
 if p.parent==SITE and re.fullmatch(r'google[0-9a-f]{16}\.html',p.name):
  if p.read_text().strip()!='google-site-verification: '+p.name:errors.append(f'{p}: invalid Google verification content')
  continue
 if len(d.ids)!=len(set(d.ids)):errors.append(f'{p}: duplicate IDs')
 if p.parent.name!='home' and d.h1!=1:errors.append(f'{p}: expected one H1')
 for tag,a in d.attrs:
  if tag=='img' and not a.get('alt'):errors.append(f'{p}: image without alt text')
  if tag=='img' and not all(a.get(k,'').isdigit() and int(a[k])>0 for k in ['width','height']):errors.append(f'{p}: image without intrinsic dimensions')
  references=[a.get(key,'') for key in (['href'] if tag in ['a','link'] else ['src'] if tag in ['img','script'] else [])]
  if tag=='img':references.extend(part.strip().split()[0] for part in a.get('srcset','').split(',') if part.strip())
  for reference in references:
   u=urlsplit(reference)
   if u.scheme or u.netloc:continue
   target=(SITE/u.path.lstrip('/') if u.path.startswith('/') else p.parent/u.path) if u.path else p
   target=target.resolve()
   if not target.is_relative_to(SITE.resolve()):errors.append(f'{p}: path outside site {u.path}');continue
   if target.is_dir():target=target/'index.html'
   refs+=1
   if not target.is_file():errors.append(f'{p.relative_to(SITE)}: missing {u.path}');continue
   if u.fragment and target in docs and unquote(u.fragment) not in docs[target].ids:errors.append(f'{p}: unknown anchor {u.fragment}')
   if tag=='img':
    b=target.read_bytes()
    if not (b.startswith((b'\x89PNG',b'\xff\xd8',b'GIF8',b'RIFF')) or b.lstrip().startswith(b'<svg')):errors.append(f'{target}: not a valid image format')
data=json.loads((ROOT/'data/content.json').read_text());highlights=json.loads((ROOT/'data/unsplash-highlights.json').read_text());captions=json.loads((ROOT/'data/photo-captions.json').read_text());home=docs[SITE/'index.html'].text();pubs=docs[SITE/'publications/index.html'].text()
def present(text,output,location):
 global coverage
 if plain(text) not in output:errors.append('Missing source text in '+location+': '+plain(text)[:80])
 coverage+=1
for s in data['biography']:present(s,home,'biography')
for n in data['news']:
 # News dates are displayed in a separate table column, with brackets removed.
 present(re.sub(r'^\[[^\]]+\]\s*','',n['html']),home,'news')
for p in data['publications']:
 present(p['title'],pubs,p['title'])
 for s in p['paragraphs']:present(s['html'],pubs,p['title'])
for g in data['galleries']:
 # The original overview repeated 2023; the owner requested a distinct portfolio summary.
 if g['slug']=='photography':continue
 # Owner requested replacing the archived 2024 “Stay tuned!” placeholder.
 if any(h['slug']==g['slug'] for h in highlights['galleries']):continue
 output=docs[SITE/g['slug']/'index.html'].text()
 replacement_indices={i+1:captions[e['src']] for i,e in enumerate(g['events'][:-1]) if e['type']=='img' and e['src'] in captions and g['events'][i+1]['type']=='p'}
 for i,e in enumerate(g['events']):
  if e['type']!='img':present(replacement_indices.get(i,e['html']),output,g['slug'])
overview=json.loads((ROOT/'data/photography-overview.json').read_text())
overview_output=docs[SITE/'photography/index.html'].text()
for paragraph in overview['introduction']:present(paragraph,overview_output,'photography overview')
for selection in overview['selections']:
 present(selection['title'],overview_output,'photography overview')
 present(selection['summary'],overview_output,'photography overview')
highlight_count=0
for g in highlights['galleries']:
 output=docs[SITE/g['slug']/'index.html'].text()
 present(g['title'],output,g['slug'])
 for paragraph in g['introduction']:present(paragraph,output,g['slug'])
 photos=g['photos']
 rendered_dates=[a['data-posted-at'] for tag,a in docs[SITE/g['slug']/'index.html'].attrs if tag=='figure' and 'data-posted-at' in a]
 if rendered_dates!=sorted(p['posted_at'] for p in photos):errors.append('Gallery is not chronological: '+g['slug'])
 if len({p['id'] for p in photos})!=len(photos):errors.append('Duplicate highlights: '+g['slug'])
 for p in photos:
  highlight_count+=1
  present(captions.get(p['local_path'],p['caption']),output,g['slug'])
  if p.get('location'):present(p['location'],output,g['slug'])
  if not p['posted_at'].startswith(str(g['year'])+'-'):errors.append('Wrong upload year: '+p['id'])
  if p['username']!='gbhatt_2':errors.append('Unexpected photo author: '+p['id'])
  f=SITE/p['local_path']
  if not f.exists() or hashlib.sha256(f.read_bytes()).hexdigest()!=p['sha256']:errors.append('Missing or changed Unsplash photo: '+p['id'])
# Check the final outgoing destinations, including overlapping legacy URL prefixes.
for repair in json.loads((ROOT/'data/link-repairs.json').read_text()):
 if repair.get('publication'):
  index=next(i for i,p in enumerate(data['publications'],1) if p['title']==repair['publication'])
  markup=(SITE/'publications/index.html').read_text().split(f'id="publication-{index}"',1)[1].split('</article>',1)[0]
  target_docs=[Doc(markup)]
 else:target_docs=list(docs.values())
 destinations=[a.get('href') for d in target_docs for tag,a in d.attrs if tag=='a']
 if repair['original'] in destinations:errors.append('Unrepaired destination: '+repair['original'])
 if repair['replacement'] not in destinations:errors.append('Missing repaired destination: '+repair['replacement'])
assets=json.loads((ROOT/'migration/source-assets.json').read_text())
for a in assets:
 f=SITE/a['local_path']
 if not f.exists() or hashlib.sha256(f.read_bytes()).hexdigest()!=a['sha256']:errors.append('Missing or changed source asset: '+a['local_path'])
cv=SITE/data['cv']
if not cv.read_bytes().startswith(b'%PDF-'):errors.append('CV is not a PDF')
variants=json.loads((ROOT/'data/image-variants.json').read_text())
for source,meta in variants.items():
 if hashlib.sha256((SITE/source).read_bytes()).hexdigest()!=meta['original_sha256']:errors.append('Changed original image: '+source)
 for variant in meta['variants']:
  f=SITE/variant['path']
  if not f.exists() or hashlib.sha256(f.read_bytes()).hexdigest()!=variant['sha256']:errors.append('Missing or changed preview: '+variant['path'])
if errors:
 print('\n'.join(errors));sys.exit(1)
print(f'PASS: {len(docs)} HTML pages, {refs} local references, {coverage} text checks, {len(assets)} original images, {highlight_count} Unsplash highlights, CV PDF.')
