import fs from 'node:fs';
import path from 'node:path';

const root=process.cwd();
const out=path.join(root,'_site');
const site=(process.env.SITE_URL||'https://adwya.iegy.net').replace(/\/$/,'');
fs.rmSync(out,{recursive:true,force:true});
fs.mkdirSync(out,{recursive:true});

for(const f of ['index.html','styles.css','theme-v2.css','grid-bg.css','shell-v3.css','site-shell.js','medical-info.js','app.js','search-worker.js','sw.js','manifest.webmanifest','about.html','sources.html','privacy.html','health.html','health.js']){
  fs.copyFileSync(path.join(root,f),path.join(out,f));
}
fs.cpSync(path.join(root,'assets'),path.join(out,'assets'),{recursive:true});
fs.cpSync(path.join(root,'data'),path.join(out,'data'),{recursive:true});
if(fs.existsSync(path.join(root,'health')))fs.cpSync(path.join(root,'health'),path.join(out,'health'),{recursive:true});
fs.copyFileSync(path.join(root,'index.html'),path.join(out,'404.html'));

const data=JSON.parse(fs.readFileSync(path.join(root,'data/egyptian-drugs.json'),'utf8'));
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function fnv1a(s){let h=0x811c9dc5;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,0x01000193)}return(h>>>0).toString(16).padStart(8,'0')}
function uid(d){return fnv1a([d.commercial_name_en,d.scientific_name,d.manufacturer,d.route].map(x=>x||'').join('|'))}
function slug(s){return String(s||'medicine').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,72)||'medicine'}
function strength(name=''){const h=String(name).toUpperCase().match(/\b\d+(?:\.\d+)?\s*(?:MCG|MG|GM|G|ML|IU|I\.U\.|%)(?:\s*\/\s*\d+(?:\.\d+)?\s*(?:MCG|MG|GM|G|ML))?/g)||[];return h.join(' + ')||'غير ظاهر بوضوح في الاسم'}
function dosageForm(name='',route=''){const s=(name+' '+route).toUpperCase();const map=[[/\b(TAB|TABS|TABLET|TABLETS)\b/,'أقراص'],[/\b(CAP|CAPS|CAPSULE|CAPSULES)\b/,'كبسولات'],[/\b(SUSP|SUSPENSION)\b/,'معلق'],[/\b(SYR|SYRUP)\b/,'شراب'],[/\b(AMP|AMPOULE|AMPOULES)\b/,'أمبولات'],[/\b(VIAL|VIALS)\b/,'فيال'],[/\b(CREAM|CRM)\b/,'كريم'],[/\b(OINT|OINTMENT)\b/,'مرهم'],[/\b(GEL)\b/,'جل'],[/\b(DROP|DROPS)\b/,'قطرات'],[/\b(SUPP|SUPPOSITORY|SUPPOSITORIES)\b/,'لبوس/تحاميل'],[/\b(SPRAY)\b/,'بخاخ'],[/\b(INHALER|INHALATION)\b/,'مستحضر استنشاق'],[/\b(PATCH)\b/,'لاصقة دوائية'],[/\b(POWDER|PWD)\b/,'مسحوق'],[/\b(SOLUTION|SOLN|SOL\.)\b/,'محلول']];for(const[x,y]of map)if(x.test(s))return y;return'غير محدد بوضوح'}

const urls=[`${site}/`,`${site}/about.html`,`${site}/sources.html`,`${site}/privacy.html`,`${site}/health.html`,`${site}/health/healthy-diet.html`,`${site}/health/fruit-vegetables-fiber.html`,`${site}/health/salt-blood-pressure.html`,`${site}/health/free-sugars.html`,`${site}/health/healthy-fats.html`,`${site}/health/protein-basics.html`,`${site}/health/hydration.html`,`${site}/health/physical-activity.html`,`${site}/health/sleep.html`,`${site}/health/food-safety.html`,`${site}/health/supplements.html`,`${site}/health/diabetes-prevention.html`,`${site}/health/heart-health.html`,`${site}/health/healthy-weight.html`,`${site}/health/vitamins-minerals.html`];

const pageStyle=`body{font-family:Cairo,Arial,sans-serif;margin:0;color:#183532;background:#f6f7f5}main.seo-main{max-width:900px;margin:32px auto;padding:0 18px 48px}.seo-card{background:#fff;border:1px solid #dce5e1;border-radius:24px;padding:28px}.p{font-size:32px;font-weight:800;direction:ltr;text-align:left}.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.b{background:#f1f4f2;padding:12px;border-radius:12px}.n{color:#657b77;font-size:13px}.warn{margin-top:20px;padding:12px;border:1px solid #e8d3b8;border-radius:12px}.seo-list li{margin:9px 0}footer{max-width:900px;margin:0 auto 30px;padding:0 18px}.credit{text-align:center}@media(max-width:600px){.grid{grid-template-columns:1fr}.seo-card{padding:19px}.p{font-size:25px}}`;

function shell(rel='../../'){
  return `<header class="site-header"><a class="brand" href="${rel}" aria-label="أدوية مصر - الرئيسية"><img src="${rel}assets/logo.png" class="brand-logo" width="92" height="76" alt="أدوية مصر - ADWYA EGYPT"><span class="brand-text"><strong>أدوية مصر</strong><small>ADWYA EGYPT</small></span></a><nav class="header-links" aria-label="التنقل الرئيسي"><a class="nav-link" href="${rel}">البحث</a><a class="nav-link" href="${rel}health.html">صحة وتغذية</a><a class="nav-link" href="${rel}sources.html">المصادر</a><a class="nav-link" href="${rel}about.html">عن الموقع</a></nav><div class="header-actions"><button class="icon-btn" id="themeBtn" type="button" aria-label="تبديل الوضع الليلي">◐</button></div></header>`;
}
function footer(rel='../../'){
  return `<footer><p class="credit">Designed &amp; Developed by Mohammed Hussein · <a href="https://iegy.net/" target="_blank" rel="noopener"><strong>iegy.net</strong></a> © ${new Date().getFullYear()}</p></footer><script>const t=document.getElementById('themeBtn');if(localStorage.getItem('adwya-theme')==='dark')document.body.classList.add('dark');t?.addEventListener('click',()=>{const d=document.body.classList.toggle('dark');localStorage.setItem('adwya-theme',d?'dark':'light')});</script><script src="${rel}site-shell.js"></script>`;
}
function head(title,desc,url,rel='../../',structured=''){
  return `<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#0b746d"><title>${esc(title)}</title><meta name="description" content="${esc(desc)}"><link rel="canonical" href="${url}"><link rel="icon" href="${rel}assets/mark.svg"><link rel="stylesheet" href="${rel}styles.css"><link rel="stylesheet" href="${rel}theme-v2.css"><link rel="stylesheet" href="${rel}grid-bg.css"><link rel="stylesheet" href="${rel}shell-v3.css"><style>${pageStyle}</style>${structured}`;
}

for(const d of data){
  const id=uid(d),s=slug(d.commercial_name_en),dir=path.join(out,'drug',`${s}-${id}`);
  fs.mkdirSync(dir,{recursive:true});
  const url=`${site}/drug/${s}-${id}/`;urls.push(url);
  const title=`${d.commercial_name_ar||d.commercial_name_en} | أدوية مصر`;
  const desc=`${d.commercial_name_en||''} — ${d.scientific_name||''} — ${d.manufacturer||''} — ${d.price_egp??''} EGP`;
  const schema=`<script type="application/ld+json">${JSON.stringify({'@context':'https://schema.org','@type':'Drug','name':d.commercial_name_en||'','activeIngredient':d.scientific_name||'','manufacturer':{'@type':'Organization','name':d.manufacturer||''}})}</script>`;
  const html=`<!doctype html><html lang="ar" dir="rtl"><head>${head(title,desc,url,'../../',schema)}</head><body>${shell('../../')}<main class="seo-main"><article class="seo-card"><a href="../../">← العودة إلى البحث</a><h1 class="p">${esc(d.commercial_name_en)}</h1><h2>${esc(d.commercial_name_ar||'')}</h2><div class="grid"><div class="b"><span class="n">المادة الفعالة</span><br>${esc(d.scientific_name||'—')}</div><div class="b"><span class="n">الشركة</span><br>${esc(d.manufacturer||'—')}</div><div class="b"><span class="n">التصنيف</span><br>${esc(d.drug_class||'—')}</div><div class="b"><span class="n">طريق الاستخدام</span><br>${esc(d.route||'—')}</div><div class="b"><span class="n">الشكل الدوائي الظاهر</span><br>${esc(dosageForm(d.commercial_name_en,d.route))}</div><div class="b"><span class="n">التركيز الظاهر في الاسم</span><br><span dir="ltr">${esc(strength(d.commercial_name_en))}</span></div><div class="b"><span class="n">السعر الاسترشادي</span><br><strong>${esc(d.price_egp??'—')} EGP</strong></div></div><p><a href="../../?drug=${id}">فتح الصفحة التفاعلية لعرض البدائل والمعلومات الطبية الإضافية والمقارنة</a></p><p class="warn">مرجع معلوماتي فقط. لا يصف جرعات ولا يقرر الاستبدال العلاجي، ويجب التحقق من السعر والنشرة والبيانات الرسمية.</p></article></main>${footer('../../')}</body></html>`;
  fs.writeFileSync(path.join(dir,'index.html'),html);
}

function groupPages(type,field,label){
  const groups=new Map();
  for(const d of data){const v=String(d[field]||'').trim();if(!v)continue;if(!groups.has(v))groups.set(v,[]);groups.get(v).push(d)}
  for(const [value,items] of groups){
    const id=fnv1a(value),s=slug(value),dir=path.join(out,type,`${s}-${id}`);fs.mkdirSync(dir,{recursive:true});
    const url=`${site}/${type}/${s}-${id}/`;urls.push(url);
    const list=items.slice(0,80).map(d=>`<li><a href="../../?drug=${uid(d)}">${esc(d.commercial_name_en||'')}</a> — ${esc(d.price_egp??'—')} EGP</li>`).join('');
    const title=`${value} | ${label} | أدوية مصر`;const desc=`${label}: ${value} — ${items.length} مستحضر في قاعدة أدوية مصر`;
    const html=`<!doctype html><html lang="ar" dir="rtl"><head>${head(title,desc,url,'../../')}</head><body>${shell('../../')}<main class="seo-main"><article class="seo-card"><a href="../../">← أدوية مصر</a><p class="n">${label}</p><h1>${esc(value)}</h1><p>${items.length} مستحضر في قاعدة البيانات الحالية.</p><p><a href="../../?q=${encodeURIComponent(value)}">فتح البحث التفاعلي لكل النتائج</a></p><ul class="seo-list">${list}</ul><p class="warn">المعلومات والأسعار استرشادية ويجب التحقق منها قبل الاستخدام أو الشراء.</p></article></main>${footer('../../')}</body></html>`;
    fs.writeFileSync(path.join(dir,'index.html'),html);
  }
  console.log('Built',groups.size,type,'pages');
}

groupPages('ingredient','scientific_name','المادة الفعالة');
groupPages('company','manufacturer','الشركة المنتجة');
groupPages('class','drug_class','التصنيف الدوائي');
const xml=`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${urls.map(u=>`<url><loc>${u}</loc></url>`).join('')}</urlset>`;
fs.writeFileSync(path.join(out,'sitemap.xml'),xml);
fs.writeFileSync(path.join(out,'robots.txt'),`User-agent: *\nAllow: /\nSitemap: ${site}/sitemap.xml\n`);
console.log('Built',data.length,'drug pages and',urls.length,'sitemap URLs');
