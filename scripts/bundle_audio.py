"""Bundle key samples byte-for-byte to reduce requests. Re-run after make_sounds.py."""
from pathlib import Path
import json,re,base64,shutil
root=Path(__file__).resolve().parents[1]/'docs';html=root/'index.html';s=html.read_text();bundle=root/'audio-data.js'
data=json.loads(bundle.read_text().removeprefix('window.ddalkkakAudio=').removesuffix(';\n')) if bundle.exists() else {}
paths=json.loads(re.search(r'<script id="audioAssets"[^>]*>(.*?)</script>',s,re.S)[1])
for key,path in paths.items():
 p=root/path
 if p.exists():data[key]='data:'+('audio/wav' if p.suffix=='.wav' else 'audio/mpeg')+';base64,'+base64.b64encode(p.read_bytes()).decode()
 assert key in data,key
bundle.write_text('window.ddalkkakAudio='+json.dumps(data,separators=(',',':'))+';\n')
for d in ['assets/sounds','assets/generated']:
 if (root/d).exists():shutil.rmtree(root/d)
print('Bundled',len(data),'samples without changing audio bytes')
