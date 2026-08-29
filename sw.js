const CACHE='adwya-shell-v1';
const SHELL=['./','./index.html','./styles.css','./app.js','./manifest.webmanifest','./assets/mark.svg'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{const req=e.request;if(req.method!=='GET')return;const u=new URL(req.url);if(u.hostname==='raw.githubusercontent.com')return;e.respondWith(caches.match(req).then(hit=>hit||fetch(req).then(res=>{if(res.ok&&u.origin===location.origin){const copy=res.clone();caches.open(CACHE).then(c=>c.put(req,copy))}return res}).catch(()=>caches.match('./index.html'))))});
