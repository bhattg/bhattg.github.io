#!/usr/bin/env python3
"""Create responsive local previews. Run with Pillow; normal site builds need only stdlib."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageOps
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site';OUT=SITE/'assets/previews';OUT.mkdir(exist_ok=True)
data=json.loads((ROOT/'data/content.json').read_text());diagrams={p['image'] for p in data['publications']}
def prepare(source):
 relative=source.relative_to(SITE).as_posix();raw=source.read_bytes();fingerprint=hashlib.sha256(raw+b'webp-q84-lossless-diagrams-v1').hexdigest()[:10]
 with Image.open(source) as original:
  original.load();im=ImageOps.exif_transpose(original)
  im=im.convert('RGBA' if 'A' in im.getbands() else 'RGB');width,height=im.size;variants=[]
  for target in sorted({min(width,w) for w in [320,640,960,1600]}):
   resized=im.resize((target,max(1,round(height*target/width))),Image.Resampling.LANCZOS) if target<width else im
   dest=OUT/f'{source.stem}-{fingerprint}-{target}.webp'
   if not dest.exists():resized.save(dest,'WEBP',quality=84,method=6,lossless=relative in diagrams,icc_profile=original.info.get('icc_profile',b''))
   b=dest.read_bytes();variants.append({'path':dest.relative_to(SITE).as_posix(),'width':resized.width,'height':resized.height,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
 return relative,{'width':width,'height':height,'original_bytes':len(raw),'original_sha256':hashlib.sha256(raw).hexdigest(),'variants':variants}
sources=sorted(p for p in (SITE/'assets/images').iterdir() if p.suffix.lower() in ['.jpg','.jpeg','.png'])
with ThreadPoolExecutor(max_workers=4) as pool:manifest=dict(pool.map(prepare,sources))
(ROOT/'data/image-variants.json').write_text(json.dumps(manifest,indent=2)+'\n')
original=sum(m['original_bytes'] for m in manifest.values());mobile=sum(min(m['variants'],key=lambda v:abs(v['width']-640))['bytes'] for m in manifest.values())
print(f'{len(manifest)} source images; {sum(len(m["variants"]) for m in manifest.values())} responsive previews. Original: {original:,} bytes; ~640px previews: {mobile:,} bytes ({100*(1-mobile/original):.1f}% smaller).')
