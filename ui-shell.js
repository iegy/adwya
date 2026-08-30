(()=>{'use strict';
const cs=document.currentScript;
const root=cs?new URL('.',cs.src):new URL('./',location.href);
const href=p=>new URL(p,root).href;

if(!document.getElementById('adwya-ui-shell-style')){
  const style=document.createElement('style');
  style.id='adwya-ui-shell-style';
  style.textContent=`
  .menu-toggle{display:none;width:44px;height:44px;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:14px;cursor:pointer;align-items:center;justify-content:center;flex-direction:column;gap:5px;padding:0}
  .menu-toggle span{display:block;width:20px;height:2px;border-radius:2px;background:currentColor;transition:.2s}
  .site-header.nav-open .menu-toggle span:nth-child(1){transform:translateY(7px) rotate(45deg)}
  .site-header.nav-open .menu-toggle span:nth-child(2){opacity:0}
  .site-header.nav-open .menu-toggle span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
  .site-header .brand-logo{object-fit:contain;object-position:center;display:block}
  footer .credit{display:block!important;text-align:center;margin:18px auto 0;padding:16px 12px 0;border-top:1px solid var(--line);color:var(--muted);font-size:13px}
  footer .credit a{color:var(--brand-dark);font-weight:800}
  @media(max-width:900px){
    .site-header{height:auto!important;min-height:78px;grid-template-columns:minmax(0,1fr) auto!important;gap:10px!important;padding:8px 14px!important;overflow:visible!important}
    .site-header .brand{min-width:0;height:62px!important;overflow:visible!important}
    .site-header .brand-logo{width:118px!important;max-width:36vw;height:58px!important;transform:none!important}
    .site-header .brand-text{display:none!important}
    .site-header .header-actions{grid-column:2;grid-row:1;display:flex!important;gap:6px!important;align-items:center;justify-content:flex-end}
    .site-header .header-actions .icon-btn,.site-header .header-actions .lang-btn,.site-header .menu-toggle{height:42px;min-width:42px;padding:0 10px;border-radius:13px}
    .menu-toggle{display:flex}
    .site-header .header-links{display:none!important;position:absolute;z-index:90;top:calc(100% + 8px);inset-inline:12px;background:var(--surface);border:1px solid var(--line);border-radius:18px;box-shadow:var(--shadow);padding:8px;flex-direction:column;align-items:stretch;gap:4px}
    .site-header.nav-open .header-links{display:flex!important}
    .site-header .header-links .nav-link{display:flex!important;width:100%;justify-content:flex-start;text-align:start;padding:11px 14px;border-radius:12px}
  }
  @media(max-width:520px){
    .site-header{padding-inline:10px!important}
    .site-header .brand-logo{width:102px!important;max-width:32vw;height:54px!important}
    .site-header .header-actions{gap:5px!important}
    .site-header .header-actions .icon-btn,.site-header .header-actions .lang-btn,.site-header .menu-toggle{height:40px;min-width:40px;padding:0 8px}
  }`;
  document.head.append(style);
}

const header=document.querySelector('.site-header');
if(header){
  const brand=header.querySelector('.brand');
  if(brand){
    let img=brand.querySelector('img');
    if(!img){img=document.createElement('img');brand.prepend(img)}
    img.src=href('assets/logo.png');
    img.classList.add('brand-logo');
    img.alt='أدوية مصر - ADWYA EGYPT';
    brand.href=href('./');
  }

  let nav=header.querySelector('.header-links');
  if(!nav){
    nav=document.createElement('nav');
    nav.className='header-links';
    nav.setAttribute('aria-label','التنقل الرئيسي');
    nav.innerHTML=`<a class="nav-link" href="${href('./')}">البحث</a><a class="nav-link" href="${href('health.html')}">صحة وتغذية</a><a class="nav-link" href="${href('sources.html')}">المصادر</a><a class="nav-link" href="${href('about.html')}">عن الموقع</a>`;
    header.insertBefore(nav,header.querySelector('.header-actions')||null);
  }

  let actions=header.querySelector('.header-actions');
  if(!actions){actions=document.createElement('div');actions.className='header-actions';header.append(actions)}
  let menu=actions.querySelector('.menu-toggle');
  if(!menu){
    menu=document.createElement('button');
    menu.type='button';menu.className='menu-toggle';menu.setAttribute('aria-label','فتح القائمة');menu.setAttribute('aria-expanded','false');
    menu.innerHTML='<span></span><span></span><span></span>';
    actions.append(menu);
  }
  const close=()=>{header.classList.remove('nav-open');menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','فتح القائمة')};
  menu.addEventListener('click',e=>{e.stopPropagation();const open=header.classList.toggle('nav-open');menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',open?'إغلاق القائمة':'فتح القائمة')});
  nav.addEventListener('click',e=>{if(e.target.closest('a,button'))close()});
  document.addEventListener('click',e=>{if(!header.contains(e.target))close()});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')close()});
}

const footer=document.querySelector('footer');
if(footer){
  let credit=footer.querySelector('.credit');
  if(!credit){credit=document.createElement('p');credit.className='credit';footer.append(credit)}
  credit.innerHTML=`Designed &amp; Developed by Mohammed Hussein · <a href="https://iegy.net/" target="_blank" rel="noopener"><strong>iegy.net</strong></a> © ${new Date().getFullYear()}`;
}
})();
