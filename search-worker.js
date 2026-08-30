let drugs=[],byUid=new Map(),ready=false;
const LOCAL='data/egyptian-drugs.json';
const META='data/meta.json';
const FALLBACK='https://raw.githubusercontent.com/karem505/egyptian-drug-database/main/data/egyptian-drugs.json';
function normalize(v=''){return String(v).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[إأآٱ]/g,'ا').replace(/ى/g,'ي').replace(/ؤ/g,'و').replace(/ئ/g,'ي').replace(/ة/g,'ه').replace(/[ًٌٍَُِّْـ]/g,'').replace(/[ضظ]/g,'ظ').replace(/[ذز]/g,'ز').replace(/[ثس]/g,'س').replace(/[^a-z0-9\u0600-\u06ff%]+/g,' ').replace(/\s+/g,' ').trim()}
function fnv1a(s){let h=0x811c9dc5;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,0x01000193)}return(h>>>0).toString(16).padStart(8,'0')}
function uid(d){return fnv1a([d.commercial_name_en,d.scientific_name,d.manufacturer,d.route].map(x=>x||'').join('|'))}
function strengthSig(name=''){const s=String(name).toUpperCase();const hits=s.match(/\b\d+(?:\.\d+)?\s*(?:MG|MCG|G|GM|ML|IU|I\.U\.|%)(?:\s*\/\s*\d+(?:\.\d+)?\s*(?:ML|MG|G|GM))?/g)||[];return hits.map(x=>x.replace(/\s+/g,'')).sort().join('+')}
function publicDrug(d){return{uid:d.uid,commercial_name_en:d.commercial_name_en,commercial_name_ar:d.commercial_name_ar,scientific_name:d.scientific_name,manufacturer:d.manufacturer,drug_class:d.drug_class,route:d.route,price_egp:d.price_egp}}
function grams(s){s=normalize(s).replace(/\s/g,'');if(s.length<2)return[s];const a=[];for(let i=0;i<s.length-1;i++)a.push(s.slice(i,i+2));return a}
function dice(a,b){const A=grams(a),B=grams(b);if(!A.length||!B.length)return 0;const m=new Map;for(const x of A)m.set(x,(m.get(x)||0)+1);let hit=0;for(const x of B){const n=m.get(x)||0;if(n){hit++;m.set(x,n-1)}}return 2*hit/(A.length+B.length)}
function fieldText(d,filter){if(filter==='name')return normalize((d.commercial_name_en||'')+' '+(d.commercial_name_ar||''));if(filter==='ingredient')return normalize(d.scientific_name||'');if(filter==='company')return normalize(d.manufacturer||'');if(filter==='class')return normalize(d.drug_class||'');return d._s||''}
function score(d,q,filter){const f=fieldText(d,filter);if(!f)return 0;if(f===q)return 150;if(f.startsWith(q))return 125;if(f.includes(q))return 92;let s=0;const words=q.split(' ').filter(Boolean);for(const w of words){if(f.split(' ').some(x=>x.startsWith(w)))s+=12;else if(f.includes(w))s+=6}if(s<45&&q.length>=4){const tokens=f.split(' ').filter(x=>Math.abs(x.length-q.length)<=4).slice(0,40);let best=0;for(const token of tokens){const sim=dice(q,token);if(sim>best)best=sim;if(best>.88)break}if(best>.66)s=Math.max(s,Math.round(best*78))}return s}
function countTop(map,limit=24){return[...map.entries()].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])).slice(0,limit).map(([value,count])=>({value,count}))}
async function fetchJson(url,tries=2){let last;for(let i=0;i<tries;i++){try{const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw new Error('HTTP '+r.status);const j=await r.json();return j}catch(e){last=e;if(i<tries-1)await new Promise(r=>setTimeout(r,500*(i+1)))}}throw last||new Error('Fetch failed')}
async function load(){
  postMessage({type:'progress',message:'loading'});
  let raw;
  try{raw=await fetchJson(LOCAL,2)}catch(localErr){try{raw=await fetchJson(FALLBACK,2)}catch(remoteErr){throw new Error('تعذر تحميل قاعدة الأدوية: '+(remoteErr?.message||localErr?.message||'network'))}}
  if(!Array.isArray(raw)||raw.length<20000)throw new Error('Invalid dataset');
  drugs=raw;
  byUid=new Map();
  const ing=new Map(),companies=new Map(),classes=new Map();
  for(let i=0;i<drugs.length;i++){
    const d=drugs[i];
    d.uid=uid(d);
    d._s=normalize([d.commercial_name_en,d.commercial_name_ar,d.scientific_name,d.manufacturer,d.drug_class].filter(Boolean).join(' '));
    byUid.set(d.uid,d);
    const a=String(d.scientific_name||'').trim(),b=String(d.manufacturer||'').trim(),c=String(d.drug_class||'').trim();
    if(a)ing.set(a,(ing.get(a)||0)+1);if(b)companies.set(b,(companies.get(b)||0)+1);if(c)classes.set(c,(classes.get(c)||0)+1);
    if(i&&i%5000===0)postMessage({type:'progress',message:'indexing',done:i,total:drugs.length});
  }
  let meta={total:drugs.length,brands:0,companies:companies.size,ingredients:ing.size};
  try{const m=await fetchJson(META,1);meta={total:m.total||drugs.length,brands:m.brands||0,companies:m.companies||companies.size,ingredients:m.ingredients||ing.size}}catch{}
  ready=true;
  postMessage({type:'ready',meta,browse:{ingredients:countTop(ing),companies:countTop(companies),classes:countTop(classes)}});
}
function doSearch(m){const q=normalize(m.q);if(!q){postMessage({type:'search',id:m.id,total:0,results:[]});return}const rows=[];for(const d of drugs){const s=score(d,q,m.filter||'all');if(s>25)rows.push({d,s})}switch(m.sort){case'priceAsc':rows.sort((a,b)=>(Number(a.d.price_egp)||Infinity)-(Number(b.d.price_egp)||Infinity)||b.s-a.s);break;case'priceDesc':rows.sort((a,b)=>(Number(b.d.price_egp)||-Infinity)-(Number(a.d.price_egp)||-Infinity)||b.s-a.s);break;case'name':rows.sort((a,b)=>String(a.d.commercial_name_en||'').localeCompare(String(b.d.commercial_name_en||'')));break;default:rows.sort((a,b)=>b.s-a.s||(Number(a.d.price_egp)||Infinity)-(Number(b.d.price_egp)||Infinity))}postMessage({type:'search',id:m.id,total:rows.length,results:rows.slice(0,m.limit||24).map(x=>publicDrug(x.d))})}
function alternatives(m){const d=byUid.get(m.uid);if(!d||!d.scientific_name){postMessage({type:'alternatives',uid:m.uid,results:[]});return}const sci=String(d.scientific_name||'').trim().toLowerCase(),route=String(d.route||'').trim().toLowerCase(),strength=strengthSig(d.commercial_name_en);const same=[];for(const x of drugs){if(x.uid===d.uid||String(x.scientific_name||'').trim().toLowerCase()!==sci)continue;const sameRoute=!!route&&String(x.route||'').trim().toLowerCase()===route;const sameStrength=!!strength&&strengthSig(x.commercial_name_en)===strength;const rank=(sameRoute?20:0)+(sameStrength?30:0);same.push({x,rank,match:sameRoute&&sameStrength?'sameStrength':sameRoute?'sameRoute':'activeOnly'})}same.sort((a,b)=>b.rank-a.rank||(Number(a.x.price_egp)||Infinity)-(Number(b.x.price_egp)||Infinity));postMessage({type:'alternatives',uid:m.uid,results:same.slice(0,14).map(({x,match})=>({...publicDrug(x),match}))})}
onmessage=async e=>{const m=e.data||{};try{if(m.type==='init'){if(!ready)await load();return}if(!ready)await load();if(m.type==='search')doSearch(m);else if(m.type==='detail')postMessage({type:'detail',drug:byUid.has(m.uid)?publicDrug(byUid.get(m.uid)):null});else if(m.type==='alternatives')alternatives(m);else if(m.type==='favorites')postMessage({type:'favorites',results:(m.uids||[]).map(x=>byUid.get(x)).filter(Boolean).map(publicDrug)});else if(m.type==='compare')postMessage({type:'compare',results:(m.uids||[]).map(x=>byUid.get(x)).filter(Boolean).map(publicDrug)})}catch(err){postMessage({type:'error',message:String(err?.message||err)})}};