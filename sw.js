/* 교통외근 통합보조 — 서비스워커
   목적: ①홈화면 앱 설치(아이콘 생성) 가능화  ②현장 음영지역 오프라인 작동
   전략: 네트워크 우선(network-first) → 온라인이면 항상 최신본을 받아 "수정본 자동반영" 유지,
         오프라인일 때만 캐시 사용. 외부 전송 없음(같은 오리진 자기 파일만 캐시). */
var CACHE = 'gtw-app-v1';
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
    fetch(req).then(function (res) {
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
