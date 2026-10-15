import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(path.join(root,p))).digest('hex');
const manifest=read('MANIFEST.json');
let checked=0;
for(const f of manifest.files){
  const resolved=path.resolve(root,f.path);
  if(!resolved.startsWith(root+path.sep)||fs.lstatSync(resolved).isSymbolicLink())throw Error('Unsafe manifest path');
  if(fs.statSync(resolved).size!==f.bytes||hash(f.path)!==f.sha256)throw Error('Changed file: '+f.path);
  checked++;
}
const coverage=read('demo/reports/coverage.json');
for(const s of [...coverage.modules,...coverage.test_sources])if(hash(s.path)!==s.sha256)throw Error('Demo source differs from measured version: '+s.path);
const evidence=read('data/evidence.json');
for(const c of evidence.claims)for(const id of c.sources)if(!evidence.sources.find(s=>s.id===id))throw Error('Missing evidence source: '+id);
for(const s of evidence.sources.filter(s=>s.availability==='PUBLIC_IN_THIS_PACKAGE'))if(hash(s.label)!==s.sha256)throw Error('Public report hash differs: '+s.id);
console.log(JSON.stringify({passed:true,version:manifest.version,manifest_files:checked,evidence_claims:evidence.claims.length,measured_demo_sources_match:true}));
