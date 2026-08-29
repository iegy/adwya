const CACHE='adwya-shell-v5';
const DATA_CACHE='adwya-data-v1';
const SHELL=['./','./index.html','./styles.css','./theme-v2.css','./app.js','./search-worker.js','./manifest.webmanifest','./assets/mark.svg','./assets/logo.webp','./about.html','./sources.html','./privacy.html'];

self.addEventListener('install',e=>{
  e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()));
});

self.addEventListener('activate',e=>{
  e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>![CACHE,DATA_CACHE].includes(k)).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));
});

self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  const u=new URL(e.request.url);

  if(u.pathname.endsWith('/data/egyptian-drugs.json')||u.pathname.endsWith('/data/price-history.json')||u.pathname.endsWith('/data/meta.json')){
    e.respondWith(caches.open(DATA_CACHE).then(async c=>{
      try{
        const fresh=await fetch(e.request);
        if(fresh.ok)c.put(e.request,fresh.clone());
        return fresh;
      }catch{
        return (await c.match(e.request))||Response.error();
      }
    }));
    return;
  }

  if(u.origin===location.origin){
    e.respondWith(caches.open(CACHE).then(async c=>{
      try{
        const fresh=await fetch(e.request);
        if(fresh.ok)c.put(e.request,fresh.clone());
        return fresh;
      }catch{
        return (await c.match(e.request))||(await c.match('./index.html'))||Response.error();
      }
    }));
  }
});
