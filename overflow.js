// overflow.js — 실측 가로넘침 검사 (HANDOFF 3-4: getBoundingClientRect 기준)
// usage: node overflow.js <file.html> <pageId> [width]
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const file = path.resolve(process.argv[2]);
  const pageId = process.argv[3];
  const W = parseInt(process.argv[4] || '360', 10);

  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: W, height: 800 }, deviceScaleFactor: 2 });
  const pg = await ctx.newPage();
  const errs = [];
  pg.on('pageerror', e => errs.push(String(e)));
  await pg.goto('file://' + file);
  await pg.waitForTimeout(400);

  const res = await pg.evaluate((pid) => {
    // 서브페이지 열기
    if (typeof showSubPage === 'function') { try { showSubPage(pid); } catch (e) {} }
    const root = document.getElementById('page-' + pid);
    if (!root) return { error: 'page not found' };
    root.style.display = 'block';
    // details 전부 펼치기
    root.querySelectorAll('details').forEach(d => d.open = true);

    const vw = document.documentElement.clientWidth;
    const docScroll = document.documentElement.scrollWidth;
    const bad = [];
    root.querySelectorAll('*').forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.width <= 0 && r.height <= 0) return;          // 미렌더 요소 제외
      const over = Math.round(r.right - vw);
      const selfScroll = el.scrollWidth - el.clientWidth;
      if (over > 1 || selfScroll > 1) {
        bad.push({
          tag: el.tagName.toLowerCase(),
          cls: el.className && el.className.toString().slice(0, 40),
          right: Math.round(r.right),
          w: Math.round(r.width),
          over,
          selfScroll,
          txt: (el.textContent || '').trim().slice(0, 45)
        });
      }
    });
    return { vw, docScroll, rootW: Math.round(root.getBoundingClientRect().width), bad };
  }, pageId);

  if (res.error) { console.log('ERR', res.error); await browser.close(); process.exit(2); }
  console.log(`viewport=${W}  clientWidth=${res.vw}  document.scrollWidth=${res.docScroll}  page.width=${res.rootW}`);
  console.log(`pageerror=${errs.length}`);
  console.log(`넘침 요소 ${res.bad.length}개`);
  // 자체 스크롤(tbl-scroll 등 의도된 것)과 실제 뷰포트 넘침 구분
  const real = res.bad.filter(b => b.over > 1);
  console.log(`  └ 뷰포트 밖으로 나간 것: ${real.length}개`);
  real.slice(0, 25).forEach(b =>
    console.log(`   ${b.tag}.${b.cls} w=${b.w} right=${b.right} over=+${b.over} sc=${b.selfScroll} | ${b.txt}`));
  await browser.close();
  process.exit(res.docScroll > res.vw + 1 ? 1 : 0);
})();
