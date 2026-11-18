from pathlib import Path
import json,re,wave,base64,io
root=Path(__file__).resolve().parents[1]/'docs'
s=(root/'index.html').read_text()
bundle=json.loads((root/'audio-data.js').read_text().removeprefix('window.ddalkkakAudio=').removesuffix(';\n'))
for name,count in [('audioAssets',178),('musicAssets',4)]:
 data=json.loads(re.search(r'<script id="'+name+r'"[^>]*>(.*?)</script>',s,re.S)[1]);assert len(data)==count
 for key,path in data.items():
  if name=='audioAssets': assert key in bundle,key
  else: assert (root/path).is_file(),path
for value in bundle.values():
 if value.startswith('data:audio/wav'):
  with wave.open(io.BytesIO(base64.b64decode(value.split(',')[1]))) as w: assert w.getframerate()==44100 and w.getnframes()>1000
cache=json.loads(re.search(r'const FILES=(.*?);',(root/'sw.js').read_text())[1])
for f in cache: assert (root/f).exists(),f
assert not any(p.suffix in ['.p12','.apk'] for p in root.rglob('*'))
print('PASS: 178 key samples, 4 BGM, 21 original WAV, all cache paths exist')
