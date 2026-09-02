/* T-Book 배포 전 확인 — 계약서 8항을 코드가 지킨다. (2026-09-02)
   사용:  node preflight.js <index.html 경로> [비교 기준 index.html 경로]
   필요:  node 18+ , npm i playwright (크로미움 1회 설치: npx playwright install chromium)
   검사:
     A. 정적 — ① 판 번호 7곳 일치 ② 무결성 6종(title·lang=ko·CSP connect-src open-meteo 1건·frame-ancestors·manifest·icon·theme-color·body 안 style 0)
                ③ script/style 개수와 계약서 머리 「현재 규모」 줄의 숫자 대조 ④ 태그 여닫힘 증감 균형(기준 파일 대비) ⑤ 모든 인라인 script node --check
     B. 동적(헤드리스) — ⑥ GROUP_PAGES 전 화면 진입 ⑦ 콘솔·페이지 오류 0 (환경 잡음: frame-ancestors 메타 경고, 로컬 sw.js 404 는 제외)
   결과: 하나라도 FAIL 이면 종료코드 1. 화면 그림이 같아도 통과가 아니다(계약서 8항 ⚠). */
const fs = require('fs'), path = require('path'), cp = require('child_process'), os = require('os'), http = require('http');
const file = process.argv[2]; const base = process.argv[3];
if (!file) { console.error('사용: node preflight.js <index.html> [기준 index.html]'); process.exit(2); }
const s = fs.readFileSync(file, 'utf8'); let fails = 0;
function ok(name, pass, detail) { console.log((pass ? 'PASS ' : 'FAIL ') + name + (detail ? '  — ' + detail : '')); if (!pass) fails++; }
function cnt(re) { return (s.match(re) || []).length; }

/* ① 판 번호 7곳 */
const vers = {
  계약서: (s.match(/코드 계약서\s+ver\.2\s+\((v[\d.]+)/) || [])[1],
  title: (s.match(/<title>T-Book (v[\d.]+)/) || [])[1],
  APP_VERSION: (s.match(/const APP_VERSION='(v[\d.]+)'/) || [])[1],
  DEPLOY_TAG: (s.match(/DEPLOY_TAG = "T-Book (v[\d.]+)/) || [])[1],
  footer: (s.match(/🚔 T-Book (v[\d.]+) \(2026 전국 공용판\) · 2026/) || [])[1],
  팝업: (s.match(/🚓 T-Book (v[\d.]+)<\/div>/) || [])[1],
  상단막대: (s.match(/<span class="ver">(v[\d.]+)<\/span>/) || [])[1],
};
const vset = new Set(Object.values(vers));
ok('판 번호 7곳 일치', vset.size === 1 && !vset.has(undefined), JSON.stringify(vers));

/* ② 무결성 6종 */
ok('title 비어 있지 않음', /<title>[^<]{3,}<\/title>/.test(s));
ok('html lang=ko', /<html lang="ko">/.test(s));
ok("CSP connect-src (open-meteo 1건만 · v21.87)", /http-equiv="Content-Security-Policy"[^>]*connect-src https:\/\/api\.open-meteo\.com; /.test(s));
ok("CSP frame-ancestors 'none'", /frame-ancestors 'none'/.test(s));
ok('manifest.json · icon 링크', /rel="manifest" href="manifest\.json"/.test(s) && /rel="icon" href="icon\.png"/.test(s));
ok('theme-color 메타', /<meta name="theme-color"/.test(s));
const body = s.slice(s.indexOf('<body'));
ok('body 안 정적 style 태그 0', (body.match(/<style\b/g) || []).length === 0);

/* ③ 계약서 머리 규모 줄 대조 */
const scripts = cnt(/<script\b/g), styles = cnt(/<style\b/g), imp = cnt(/!important/g), lines = (s.match(/\n/g) || []).length, man = ([...s].length / 10000).toFixed(1); /* 파이썬 len()과 같은 기준: 코드포인트 수 · 줄 = 개행 수 */
const head = s.match(/(\d+\.\d)만자 \/ ([\d,]+)줄 · script (\d+)개 · style (\d+)개[^·]*· !important (\d+)개/);
ok('계약서 머리 「현재 규모」 = 실측', !!head && head[1] === man && head[2] === lines.toLocaleString('en-US') && +head[3] === scripts && +head[4] === styles && +head[5] === imp,
   `실측 ${man}만자/${lines.toLocaleString('en-US')}줄/script ${scripts}/style ${styles}/!important ${imp} · 머리 ${head ? head.slice(1).join('/') : '못 찾음'}`);

/* ④ 태그 균형(기준 대비) */
if (base) {
  const b = fs.readFileSync(base, 'utf8'); const bad = [];
  for (const t of ['div', 'details', 'p', 'span', 'button', 'summary', 'ul', 'li', 'table', 'tr', 'td', 'svg']) {
    const o = (x) => (x.match(new RegExp('<' + t + '\\b', 'g')) || []).length, c = (x) => (x.match(new RegExp('</' + t + '>', 'g')) || []).length;
    if ((o(s) - o(b)) !== (c(s) - c(b))) bad.push(`${t} 여 ${o(s) - o(b)} / 닫 ${c(s) - c(b)}`);
  }
  ok('태그 여닫힘 증감 균형(기준 대비)', bad.length === 0, bad.join(', ') || '전부 균형');
  ok('script 개수 불변(기준 대비)', scripts === (b.match(/<script\b/g) || []).length, `${(b.match(/<script\b/g) || []).length} → ${scripts}`);
}

/* ⑤ node --check */
let synErr = 0; const blocks = [...s.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)];
for (const m of blocks) { if (!m[1].trim()) continue; const tmp = path.join(os.tmpdir(), 'tb_' + Math.random().toString(36).slice(2) + '.js'); fs.writeFileSync(tmp, m[1]);
  const r = cp.spawnSync('node', ['--check', tmp]); if (r.status) { synErr++; console.log('   문법 오류:', String(r.stderr).slice(0, 200)); } fs.unlinkSync(tmp); }
ok('인라인 script node --check', synErr === 0, `${blocks.length}블록`);

/* ⑥⑦ 헤드리스 */
(async () => {
  let chromium; try { chromium = require('playwright').chromium; } catch (e) { ok('헤드리스(playwright 없음 — 건너뜀)', true); return done(); }
  const dir = path.dirname(path.resolve(file)), fname = path.basename(file);
  const srv = http.createServer((q, r) => { const u = q.url.split('?')[0]; const f = path.join(dir, u === '/' ? fname : u); if (fs.existsSync(f) && fs.statSync(f).isFile()) { r.setHeader('content-type', f.endsWith('.html') ? 'text/html; charset=utf-8' : 'application/octet-stream'); fs.createReadStream(f).pipe(r); } else { r.statusCode = 404; r.end(); } }).listen(0);
  const port = srv.address().port; const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
  await ctx.addInitScript(() => { try { localStorage.setItem('entry_gate_ok', '1'); localStorage.setItem('lawrev_seen', '1'); } catch (e) {} });
  const pg = await ctx.newPage(); const errs = [];
  pg.on('console', m => { if (m.type() === 'error' && !/frame-ancestors|404/.test(m.text())) errs.push(m.text().slice(0, 160)); });
  pg.on('pageerror', e => errs.push('PAGEERROR ' + String(e).slice(0, 160)));
  await pg.goto('http://127.0.0.1:' + port + '/', { waitUntil: 'load' }); await pg.waitForTimeout(2500);
  const groups = await pg.evaluate(() => Object.keys(GROUP_PAGES)); let visited = 0; const fail = [];
  for (const g of groups) for (const p of await pg.evaluate(g => GROUP_PAGES[g], g)) {
    const r = await pg.evaluate(([g, p]) => { try { showGroup(g); showSubPage(p); const el = document.getElementById('page-' + p); return !!el && el.classList.contains('active'); } catch (e) { return 'ERR ' + e.message; } }, [g, p]);
    visited++; if (r !== true) fail.push(p + ':' + r); await pg.waitForTimeout(40);
  }
  const ver = await pg.evaluate(() => APP_VERSION);
  ok('화면 전수 진입', fail.length === 0, `${visited}개 진입, 실패 ${fail.length} ${fail.slice(0, 5).join(' ')}`);
  ok('콘솔·페이지 오류 0', errs.length === 0, errs.slice(0, 5).join(' | ') || `APP_VERSION ${ver}`);
  await b.close(); srv.close(); done();
})();
function done() { console.log(fails ? `\n✗ FAIL ${fails}건 — 덮어쓰지 말 것 (계약서 8항)` : '\n✓ 전부 통과'); process.exit(fails ? 1 : 0); }
