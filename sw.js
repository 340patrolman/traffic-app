/* 교통외근 통합보조 — 서비스워커
   목적: ⓐ홈화면 앱 설치(아이콘 생성) 가능화 ⓑ현장 음영지역 오프라인 작동
   v2: 네트워크 요청에 cache:'no-store' — 브라우저/Pages HTTP 캐시 우회.
   v3: 응답 지연 안전장치 — 캐시본이 있으면 NET_TIMEOUT 안에 네트워크가 응답하지 않을 때 캐시본으로 전환.
   v4 (2026-09-02): 「캐시 먼저, 뒤에서 갱신」(stale-while-revalidate).
       종전(v3)은 온라인이면 열 때마다 3MB를 새로 받은 뒤에야 화면이 떴다(no-store라 304도 안 됨).
       이제는 ① 캐시본이 있으면 그것으로 즉시 연다(회선과 무관)
              ② 뒤에서 조건부 요청(cache:'no-cache' → 서버가 같으면 304, 본문 전송 없음)으로 최신본을 확인하고
              ③ 내용이 바뀌었으면 캐시를 갈아 끼우고 열린 화면에 TB_UPDATED 를 보낸다
                 → index.html(v20.1 부터 있는 수신부)이 「🆕 새 판이 준비됐습니다 · 새로고침」 띠를 띄운다.
                 자동 새로고침은 하지 않는다. 현장에서 쓰던 화면이 갑자기 날아가면 안 된다.
       첫 방문(캐시 없음)은 종전대로 네트워크를 끝까지 기다린다.
       캐시 이름은 v2를 유지한다 — 이름을 바꾸면 전 사용자가 3MB를 다시 받는다.
       외부 전송 없음(같은 출처 GET만 다룬다). 다른 출처 요청은 손대지 않는다.
   되돌리려면 v3 파일로 교체하면 된다. */
var CACHE = 'gtw-app-v2';
var CORE = ['./', 'index.html', 'icon.png', 'robots.txt'];

self.addEventListener('install', function (e) {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE).then(function (c) {
      return Promise.all(CORE.map(function (u) {
        return c.add(new Request(u, { cache: 'reload' })).catch(function () { return null; });
      }));
    })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        if (k !== CACHE) return caches.delete(k);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('message', function (e) {
  if (e.data && e.data.type === 'TBOOK_SKIP_WAITING') { self.skipWaiting(); }
});

/* 두 응답이 같은 내용인지 — 검증 헤더가 있으면 그걸로, 없으면 본문을 비교한다 */
function sameContent(a, b) {
  try {
    var ea = a.headers.get('etag'), eb = b.headers.get('etag');
    if (ea && eb) return Promise.resolve(ea === eb);
    var la = a.headers.get('last-modified'), lb = b.headers.get('last-modified');
    if (la && lb) return Promise.resolve(la === lb);
  } catch (err) {}
  return Promise.all([a.clone().text(), b.clone().text()]).then(function (t) {
    return t[0] === t[1];
  }).catch(function () { return false; });
}

/* 페이지의 수신부(index.html v20.1)는 load 뒤에 붙는다. 회선이 빠르면 갱신이 그보다 먼저 끝나
   메시지가 허공에 떨어지므로, 잠시 뒤에 보내고 한 번 더 보낸다(수신부가 띠 중복을 막는다). */
function notifyClients(msg) {
  function send() {
    return self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function (cs) {
      cs.forEach(function (c) { try { c.postMessage(msg); } catch (err) {} });
    });
  }
  function later(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  return later(2500).then(send).then(function () { return later(5000); }).then(send);
}

function offlinePage() {
  return caches.match('index.html').then(function (m) {
    return m || caches.match('./');
  }).then(function (m) {
    return m || new Response(
      '<meta charset="utf-8"><body style="font-family:sans-serif;padding:40px;text-align:center;background:#0f172a;color:#fff">' +
      '<h3>오프라인 사본이 아직 없습니다</h3><p style="color:#cbd5e1">인터넷이 되는 곳에서 한 번 열면 이후에는 음영지역에서도 열립니다.</p></body>',
      { status: 503, headers: { 'Content-Type': 'text/html; charset=utf-8' } });
  });
}

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;
  var url;
  try { url = new URL(req.url); } catch (err) { return; }
  if (url.origin !== self.location.origin) return;

  var isDoc = (req.mode === 'navigate') ||
              (req.headers.get('accept') || '').indexOf('text/html') >= 0;

  var cachedP = caches.match(req);

  /* 뒤에서 최신본 확인·갱신. 조건부 요청이라 내용이 같으면 서버가 304로 답하고 본문은 안 온다. */
  var netP = cachedP.then(function (cached) {
    return fetch(req, { cache: 'no-cache' }).then(function (res) {
      if (!(res && res.status === 200 && res.type === 'basic')) return res;
      var copy = res.clone();
      var update = caches.open(CACHE).then(function (c) {
        if (!cached) return c.put(req, copy);
        return sameContent(cached, res).then(function (same) {
          if (same) return null;
          return c.put(req, copy).then(function () {
            if (isDoc) return notifyClients({ type: 'TB_UPDATED' });
          });
        });
      }).catch(function () {});
      return update.then(function () { return res; });
    });
  });
  e.waitUntil(netP.catch(function () {}));

  e.respondWith(
    cachedP.then(function (cached) {
      /* (2) 캐시본 있음 — 즉시 캐시본으로 연다. 최신본은 뒤에서 확인한다. */
      if (cached) return cached;
      /* (1) 캐시본 없음(첫 방문) — 네트워크를 끝까지 기다린다 */
      return netP.catch(function () {
        return isDoc ? offlinePage() : Response.error();
      });
    })
  );
});
