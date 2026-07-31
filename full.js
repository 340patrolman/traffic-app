// full.js — 전 페이지 순회 + 전 버튼 실클릭 + DOM 중첩 + onclick 함수 존재 + 하단 메뉴 5개
// usage: node full.js <file.html>
const { chromium } = require('playwright');
const FILE = process.argv[2] || 'TBook_v19.8.3.html';
const BASE = 'http://127.0.0.1:8953/' + FILE;
// 삭제·초기화·내보내기 계열은 클릭 제외
const SKIP = /삭제|초기화|리셋|전체지우|비우기|내보내기|다운로드|로그아웃|잠금|reset|clear|delete/i;

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 412, height: 900 } });
  const page = await ctx.newPage();
  const errs = [];
  page.on('pageerror', e => errs.push(e.message.slice(0, 120)));
  page.on('dialog', d => d.dismiss().catch(() => {}));
  await page.addInitScript(() => {
    try {
      ['intro_hide_v141', 'entry_gate_ok', 'police_v6_accepted', 'tbook_tour_done'].forEach(k => localStorage.setItem(k, '1'));
      localStorage.setItem('pwa_modal_closed_time', String(Date.now()));
      localStorage.setItem('tbook_home_mode', 'dash');
    } catch (e) {}
    window.print = () => {}; window.open = () => null;
  });
  await page.goto(BASE);
  await page.waitForTimeout(600);

  // ── 1) DOM 중첩 · onclick 함수 존재
  const structural = await page.evaluate(() => {
    const pages = [...document.querySelectorAll('.page')];
    const nested = pages.filter(p => p.parentElement !== document.body).map(p => p.id);
    const hd = document.getElementById('hd_tabs');
    const hdTrapped = hd ? !!hd.closest('.page') : 'hd_tabs 없음';
    const missingFn = new Set();
    document.querySelectorAll('[onclick]').forEach(el => {
      const code = el.getAttribute('onclick') || '';
      // 멤버호출(el.foo())·정의부는 제외하고 전역 함수 호출만 본다
      (code.match(/(^|[^\w$.])([A-Za-z_$][\w$]*)\s*\(/g) || []).forEach(raw => {
        const m = raw.match(/([A-Za-z_$][\w$]*)\s*\($/);
        if (!m) return;
        const fn = m[1];
        if (['if', 'for', 'while', 'return', 'typeof', 'function', 'catch', 'switch', 'String', 'Number', 'Array', 'Object', 'Date', 'Math', 'JSON', 'parseInt', 'parseFloat', 'alert', 'confirm', 'prompt', 'setTimeout'].includes(fn)) return;
        if (typeof window[fn] !== 'function') missingFn.add(fn);
      });
    });
    return { total: pages.length, nested, hdTrapped, hdCount: hd ? hd.querySelectorAll('button,.ntab,[onclick]').length : 0, missingFn: [...missingFn] };
  });

  // ── 2) 전 버튼 실클릭
  const tabs = await page.evaluate(() => {
    const o = []; try { for (const g in GROUP_PAGES) for (const t of GROUP_PAGES[g]) o.push([g, t]); } catch (e) {}
    return [...new Set(o.map(JSON.stringify))].map(JSON.parse);
  });
  let clicked = 0, skipped = 0;
  for (const [g, t] of tabs) {
    await page.evaluate(([g, t]) => { try { showGroup(g); showSubPage(t); } catch (e) {} }, [g, t]);
    await page.waitForTimeout(60);
    const n = await page.evaluate(t => {
      const el = document.getElementById('page-' + t); if (!el) return 0;
      return el.querySelectorAll('button,.btn,[onclick]').length;
    }, t);
    for (let i = 0; i < n; i++) {
      const res = await page.evaluate(([t, i, skipSrc]) => {
        const el = document.getElementById('page-' + t); if (!el) return 'miss';
        const b = el.querySelectorAll('button,.btn,[onclick]')[i]; if (!b) return 'miss';
        if (new RegExp(skipSrc, 'i').test(b.textContent || '')) return 'skip';
        const r = b.getBoundingClientRect();
        if (!(r.width > 0 || r.height > 0)) return 'skip';
        try { b.click(); } catch (e) { return 'err:' + e.message.slice(0, 60); }
        return 'ok';
      }, [t, i, SKIP.source]);
      if (res === 'ok') clicked++; else if (res === 'skip' || res === 'miss') skipped++;
      else errs.push(`click ${t}#${i} ${res}`);
      // 클릭으로 페이지가 바뀌었을 수 있으니 되돌린다
      await page.evaluate(([g, t]) => { try { showGroup(g); showSubPage(t); } catch (e) {} }, [g, t]);
    }
  }

  // ── 3) 하단 메뉴 5개 실클릭 전환
  const nav = await page.evaluate(() => {
    const hd = document.getElementById('hd_tabs'); if (!hd) return { n: 0 };
    const btns = [...hd.querySelectorAll('button,.ntab,[onclick]')].filter(b => {
      const r = b.getBoundingClientRect(); return r.width > 0;
    });
    const before = btns.length; let ok = 0;
    btns.forEach(b => {
      try {
        b.click();
        const vis = [...document.querySelectorAll('.page')].filter(p => p.getBoundingClientRect().width > 0);
        if (vis.length > 0) ok++;
      } catch (e) {}
    });
    return { n: before, ok };
  });

  await browser.close();
  console.log(`── full.js : ${FILE}`);
  console.log(`   페이지 ${structural.total}개 · body 비직속 ${structural.nested.length}건 ${structural.nested.slice(0, 5)}`);
  console.log(`   hd_tabs 페이지 안 갇힘: ${structural.hdTrapped}`);
  console.log(`   onclick 미정의 함수: ${structural.missingFn.length}건 ${structural.missingFn.slice(0, 8)}`);
  console.log(`   버튼 실클릭 ${clicked}개 (제외 ${skipped}) → pageerror ${errs.length}`);
  console.log(`   하단 메뉴 ${nav.n}개 클릭 → 전환 정상 ${nav.ok}`);
  errs.slice(0, 10).forEach(e => console.log('   ! ' + e));
  const bad = errs.length || structural.nested.length || structural.hdTrapped === true || structural.missingFn.length;
  console.log(bad ? '\n🔴 full.js 실패 — 배포 중단' : '\n✅ full.js 통과');
  process.exit(bad ? 1 : 0);
})();
