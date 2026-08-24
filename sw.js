/* 교통외근 통합보조 — 서비스워커
   목적: ⓐ홈화면 앱 설치(아이콘 생성) 가능화  ⓑ현장 음영지역 오프라인 작동
   전략: 네트워크 우선(network-first) → 온라인이면 항상 최신본을 받아 "수정본 자동반영" 유지,
        오프라인일 때만 캐시 사용. 외부 전송 없음(같은 오리진 자기 파일만 캐시).
   v2: 네트워크 요청에 cache:'no-store' 적용 — 브라우저/Pages HTTP 캐시를 우회해
        온라인이면 항상 진짜 최신본을 받도록(수정본이 즉시 반영되지 않던 문제 해결).
   v3: 응답 지연 안전장치 — 캐시본이 있으면 NET_TIMEOUT 안에 네트워크가 응답하지 않을 때
        캐시본으로 즉시 전환한다. 터널·지하주차장처럼 "연결됨으로 보이지만 응답이 없는"
        구간에서 흰 화면으로 매달리던 문제를 막는다.
        캐시본이 없는 첫 방문은 종전대로 끝까지 기다린다(설치가 되어야 하므로).
        캐시 이름은 v2를 유지한다 — 이름을 바꾸면 전 사용자가 2.84MB를 다시 받는다. */
var CACHE = 'gtw-app-v2';
var CORE = ['./', 'index.html', 'icon.png', 'robots.txt'];
var NET_TIMEOUT = 2500;   // ms. 현장 체감상 3초를 넘기면 "안 열린다"고 느낀다

self.addEventListener('install', function (e) {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE).then(function (c) {
      return c.addAll(CORE).catch(function () {}); // 일부 파일 없어도 설치 진행
    })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        if (k !== CACHE) return caches.delete(k); // 구버전 캐시 제거
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;

  e.respondWith(
    caches.match(req).then(function (cached) {

      // 네트워크 시도 — 정상 응답이면 캐시를 최신본으로 갱신
      var net = fetch(req, { cache: 'no-store' }).then(function (res) {
        if (res && res.status === 200 && res.type === 'basic') {
          var copy = res.clone();
          caches.open(CACHE).then(function (c) { c.put(req, copy); });
        }
        return res;
      });

      // (1) 캐시본 없음(첫 방문) — 종전대로 네트워크를 끝까지 기다린다
      if (!cached) {
        return net.catch(function () {
          return caches.match('index.html').then(function (m) {
            return m || caches.match('./');
          });
        });
      }

      // (2) 캐시본 있음 — 제한시간 안에 오면 최신본, 늦으면 캐시본으로 즉시 전환.
      //     늦게 도착한 응답도 위 net 안에서 캐시에 반영되므로 다음 실행 때 최신본이 뜬다.
      return Promise.race([
        net.catch(function () { return cached; }),
        new Promise(function (resolve) {
          setTimeout(function () { resolve(cached); }, NET_TIMEOUT);
        })
      ]);
    })
  );
});
/* 교통외근 통합보조 — 서비스워커
   목적: ⓐ홈화면 앱 설치(아이콘 생성) 가능화  ⓑ현장 음영지역 오프라인 작동
   전략: 네트워크 우선(network-first) → 온라인이면 항상 최신본을 받아 "수정본 자동반영" 유지,
        오프라인일 때만 캐시 사용. 외부 전송 없음(같은 오리진 자기 파일만 캐시).
   v2: 네트워크 요청에 cache:'no-store' 적용 — 브라우저/Pages HTTP 캐시를 우회해
        온라인이면 항상 진짜 최신본을 받도록(수정본이 즉시 반영되지 않던 문제 해결).
   v3: 응답 지연 안전장치 — 캐시본이 있으면 NET_TIMEOUT 안에 네트워크가 응답하지 않을 때
        캐시본으로 즉시 전환한다. 터널·지하주차장처럼 "연결됨으로 보이지만 응답이 없는"
        구간에서 흰 화면으로 매달리던 문제를 막는다.
        캐시본이 없는 첫 방문은 종전대로 끝까지 기다린다(설치가 되어야 하므로).
        캐시 이름은 v2를 유지한다 — 이름을 바꾸면 전 사용자가 2.84MB를 다시 받는다. */
var CACHE = 'gtw-app-v2';
var CORE = ['./', 'index.html', 'icon.png', 'robots.txt'];
var NET_TIMEOUT = 2500;   // ms. 현장 체감상 3초를 넘기면 "안 열린다"고 느낀다

self.addEventListener('install', function (e) {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE).then(function (c) {
      return c.addAll(CORE).catch(function () {}); // 일부 파일 없어도 설치 진행
    })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        if (k !== CACHE) return caches.delete(k); // 구버전 캐시 제거
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;

  e.respondWith(
    caches.match(req).then(function (cached) {

      // 네트워크 시도 — 정상 응답이면 캐시를 최신본으로 갱신
      var net = fetch(req, { cache: 'no-store' }).then(function (res) {
        if (res && res.status === 200 && res.type === 'basic') {
          var copy = res.clone();
          caches.open(CACHE).then(function (c) { c.put(req, copy); });
        }
        return res;
      });

      // (1) 캐시본 없음(첫 방문) — 종전대로 네트워크를 끝까지 기다린다
      if (!cached) {
        return net.catch(function () {
          return caches.match('index.html').then(function (m) {
            return m || caches.match('./');
          });
        });
      }

      // (2) 캐시본 있음 — 제한시간 안에 오면 최신본, 늦으면 캐시본으로 즉시 전환.
      //     늦게 도착한 응답도 위 net 안에서 캐시에 반영되므로 다음 실행 때 최신본이 뜬다.
      return Promise.race([
        net.catch(function () { return cached; }),
        new Promise(function (resolve) {
          setTimeout(function () { resolve(cached); }, NET_TIMEOUT);
        })
      ]);
    })
  );
});
/* 교통외근 통합보조 — 서비스워커
   목적: ①홈화면 앱 설치(아이콘 생성) 가능화  ②현장 음영지역 오프라인 작동
   전략: 네트워크 우선(network-first) → 온라인이면 항상 최신본을 받아 "수정본 자동반영" 유지,
         오프라인일 때만 캐시 사용. 외부 전송 없음(같은 오리진 자기 파일만 캐시).
   v2: 네트워크 요청에 cache:'no-store' 적용 — 브라우저/Pages HTTP 캐시를 우회해
       온라인이면 항상 진짜 최신본을 받도록(수정본이 즉시 반영되지 않던 문제 해결). */
var CACHE = 'gtw-app-v2';
var CORE = ['./', 'index.html', 'icon.png', 'robots.txt'];

self.addEventListener('install', function (e) {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE).then(function (c) {
      return c.addAll(CORE).catch(function () {}); // 일부 파일 없어도 설치 진행
    })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        if (k !== CACHE) return caches.delete(k); // 구버전 캐시 제거
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;
  e.respondWith(
    fetch(req, { cache: 'no-store' }).then(function (res) {
      // 정상 응답이면 최신본을 캐시에 갱신
      if (res && res.status === 200 && res.type === 'basic') {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(req, copy); });
      }
      return res;
    }).catch(function () {
      // 오프라인: 캐시 → 없으면 앱 셸로 폴백
      return caches.match(req).then(function (m) {
        return m || caches.match('index.html') || caches.match('./');
      });
    })
  );
});
