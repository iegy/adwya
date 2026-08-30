const CACHE='adwya-shell-v9';
const DATA_CACHE='adwya-data-v3';
const SHELL=['./','./index.html','./styles.css','./theme-v2.css','./grid-bg.css','./shell-v3.css','./app.js','./site-shell.js','./medical-info.js','./search-worker.js','./health.js','./manifest.webmanifest','./assets/mark.svg','./assets/logo.png','./about.html','./sources.html','./privacy.html','./health.html'];

self.addEventListener('install',e=>{
  e.waitUntil((async()=>{
    const c=await caches.open(CACHE);
    await Promise.allSettled(SHELL.map(async url=>{
      try{const r=await fetch(url,{cache:'reload'});if(r.ok)await c.put(url,r.clone())}catch{}
    }));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate',e=>{
  e.waitUntil((async()=>{
    const keys=await caches.keys();
    await Promise.all(keys.filter(k=>![CACHE,DATA_CACHE].includes(k)).map(k=>caches.delete(k)));
    await self.clients.claim();
  })());
});

self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  const u=new URL(e.request.url);
  if(u.origin!==location.origin)return;

  if(u.pathname.endsWith('/data/egyptian-drugs.json')){
    e.respondWith(fetch(e.request,{cache:'no-store'}));
    return;
  }

  if(u.pathname.includes('/data/')){
    e.respondWith((async()=>{
      const c=await caches.open(DATA_CACHE);
      try{
        const fresh=await fetch(e.request,{cache:'no-store'});
        if(fresh.ok)await c.put(e.request,fresh.clone());
        return fresh;
      }catch(err){
        const cached=await c.match(e.request);
        if(cached)return cached;
        throw err;
      }
    })());
    return;
  }

  if(e.request.mode==='navigate'){
    e.respondWith((async()=>{
      try{
        const fresh=await fetch(e.request,{cache:'no-store'});
        if(fresh.ok){const c=await caches.open(CACHE);c.put(e.request,fresh.clone())}
        return fresh;
      }catch{
        return (await caches.match(e.request))||(await caches.match('./index.html'))||Response.error();
      }
    })());
    return;
  }

  const isCode=/\.(?:js|css)$/.test(u.pathname);
  if(isCode){
    e.respondWith((async()=>{
      const c=await caches.open(CACHE);
      try{
        const fresh=await fetch(e.request,{cache:'no-store'});
        if(fresh.ok)await c.put(e.request,fresh.clone());
        return fresh;
      }catch{
        return (await c.match(e.request))||Response.error();
      }
    })());
    return;
  }

  e.respondWith((async()=>{
    const c=await caches.open(CACHE);
    const cached=await c.match(e.request);
    if(cached)return cached;
    try{const fresh=await fetch(e.request);if(fresh.ok)await c.put(e.request,fresh.clone());return fresh}catch{return Response.error()}
  })());
});
