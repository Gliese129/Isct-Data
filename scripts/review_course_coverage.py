#!/usr/bin/env python3
import argparse,json,re,sys
from pathlib import Path
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--data-root',required=True,type=Path);ap.add_argument('--guides-dir',required=True,type=Path);ap.add_argument('--year',action='append',required=True);ap.add_argument('--format',choices=('text','json'),default='text');ap.add_argument('--shift29',action='store_true');a=ap.parse_args();out=[];bad=False
 for year in a.year:
  f=a.data_root/'departments'/f'{year}.json'
  if not f.exists(): ap.error(f'missing {f}')
  d=json.loads(f.read_text())
  for dep in d['departments']:
   m=re.search(r'/([0-9]{2})-([0-9]{2})\.pdf$',dep.get('guidePdf',''))
   if not m: ap.error(f'bad guidePdf for {dep["id"]}')
   txt=a.guides_dir/year/f'{m.group(2)}.txt'
   if not txt.exists(): ap.error(f'missing guide text {txt}')
   s=txt.read_text(errors='ignore')
   if a.shift29 and year=='2025' and dep['id']=='chemistry': s=''.join(chr(ord(c)+29) if (ord(c)<=31 or c in '&+%/') else c for c in s)
   pub={x.rsplit('.',1)[0] if x.rsplit('.',1)[-1].isalpha() else x for x in re.findall(r'\b[A-Z]{3}\.[A-Z]\d{3}(?:\.[A-Z])?\b',s)};have={x['code'] for x in dep['recommended']};miss=sorted(pub-have);extra=sorted(have-pub);bad |= bool(miss or extra);out.append({'year':year,'department':dep['id'],'published':len(pub),'stored':len(have),'missing':miss,'extra':extra})
 print(json.dumps(out,ensure_ascii=False,indent=2) if a.format=='json' else '\n'.join(f"{x['year']} {x['department']}: published={x['published']} stored={x['stored']} missing={len(x['missing'])} extra={len(x['extra'])}" for x in out));return 1 if bad else 0
if __name__=='__main__':sys.exit(main())
