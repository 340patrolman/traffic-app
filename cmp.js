// cmp.js — 기준선 대비 하단 메뉴 버튼 개수·페이지 수 대조
// usage: node cmp.js <baseline.html> <target.html>
const { chromium } = require('playwright');
const A = process.argv[2], B = process.argv[3];

async function probe(browser, file) {
  const ctx = await browser.newContext({ viewport: { width: 412, height: 900 } });
  const p = await ctx.newPage();
  await p.addInitScript(() => {
    try {
      ['intro_hide_v141', 'entry_gate_ok', 'police_v6_accepted', 'tbook_tour_done'].forEach(k => localStorage.setItem(k, '1'));
      localStorage.setItem('pwa_modal_closed_time', String(Date.now()));
    } catch (e) {}
  });
  await p.goto('http://127.0.0.1:8953/' + file);
  await p.waitForTimeout(500);
  const r = await p.evaluate(() => {
    const hd = document.getElementById('hd_tabs');
    const nav = hd ? [...hd.querySelectorAll('button,.ntab,[onclick]')]
      .filter(b => b.getBoundingClientRect().width > 0).map(b => (b.textContent || '').trim().slice(0, 8)) : [];
    let tabs = 0; try { for (const g in GROUP_PAGES) tabs += GROUP_PAGES[g].length; } catch (e) {}
    return { nav, navN: nav.length, pages: document.querySelectorAll('.page').length, tabs };
  });
  await ctx.close();
  return r;
}

(async () => {
  const browser = await chromium.launch();
  const a = await probe(browser, A), b = await probe(browser, B);
  await browser.close();
  console.log(`── cmp.js`);
  console.log(`   기준선 ${A}: 하단메뉴 ${a.navN}개 ${JSON.stringify(a.nav)} · 페이지 ${a.pages} · 탭 ${a.tabs}`);
  console.log(`   대상  ${B}: 하단메뉴 ${b.navN}개 ${JSON.stringify(b.nav)} · 페이지 ${b.pages} · 탭 ${b.tabs}`);
  const bad = a.navN !== b.navN || a.pages !== b.pages || a.tabs !== b.tabs;
  console.log(bad ? '\n🔴 cmp.js 불일치 — 배포 중단' : '\n✅ cmp.js 통과 (하단 메뉴·페이지·탭 수 동일)');
  process.exit(bad ? 1 : 0);
})();
