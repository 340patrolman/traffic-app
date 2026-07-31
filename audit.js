// audit.js — 전 페이지 순회 · pageerror · 가로넘침 (51탭 × 2모드 × 2폭 = 204 visits)
// usage: node audit.js <file.html>
const { chromium } = require('playwright');
const FILE = process.argv[2] || 'TBook_v19.8.3.html';
const BASE = 'http://127.0.0.1:8953/' + FILE;

const SEED = () => {
  try {
    localStorage.setItem('intro_hide_v141', '1');
    localStorage.setItem('entry_gate_ok', '1');
    localStorage.setItem('police_v6_accepted', '1');
    localStorage.setItem('tbook_tour_done', '1');
    localStorage.setItem('pwa_modal_closed_time', String(Date.now()));
  } catch (e) {}
};

(async () => {
  const browser = await chromium.launch();
  let visits = 0, errs = 0, over = 0;
  const errList = [], overList = [];

  for (const W of [360, 412]) {
    for (const mode of ['dash', 'classic']) {
      const ctx = await browser.newContext({ viewport: { width: W, height: 800 } });
      const page = await ctx.newPage();
      page.on('pageerror', e => { errs++; errList.push(`${mode}/${W} ${e.message.slice(0, 90)}`); });
      await page.addInitScript(SEED);
      await page.addInitScript(m => { try { localStorage.setItem('tbook_home_mode', m); } catch (e) {} }, mode);
      await page.goto(BASE);
      await page.waitForTimeout(500);

      const tabs = await page.evaluate(() => {
        const out = [];
        try { for (const g in GROUP_PAGES) for (const t of GROUP_PAGES[g]) out.push([g, t]); } catch (e) {}
        return [...new Set(out.map(JSON.stringify))].map(JSON.parse);
      });

      for (const [g, t] of tabs) {
        const r = await page.evaluate(([g, t]) => {
          try { showGroup(g); showSubPage(t); } catch (e) { return { miss: true }; }
          const el = document.getElementById('page-' + t);
          if (!el) return { miss: true };
          // HANDOFF 3-4: display 로 판정하지 않는다
          const rc = el.getBoundingClientRect();
          if (!(rc.width > 0)) return { hidden: true };
          const vw = document.documentElement.clientWidth;
          let n = 0;
          el.querySelectorAll('*').forEach(x => {
            const q = x.getBoundingClientRect();
            if ((q.width > 0 || q.height > 0) && q.right - vw > 1) n++;
          });
          return { over: n, w: Math.round(rc.width) };
        }, [g, t]);
        visits++;
        if (r.miss) { errList.push(`MISSING ${g}/${t}`); errs++; }
        else if (r.hidden) { errList.push(`NOT-RENDERED ${g}/${t} @${mode}/${W}`); errs++; }
        else if (r.over > 0) { over++; overList.push(`${g}/${t} @${mode}/${W} = ${r.over}`); }
      }
      await ctx.close();
    }
  }
  await browser.close();
  console.log(`── audit.js : ${FILE}`);
  console.log(`   visits=${visits}  pageerror/미렌더=${errs}  가로넘침 페이지=${over}`);
  errList.slice(0, 12).forEach(e => console.log('   ! ' + e));
  overList.slice(0, 14).forEach(e => console.log('   ▸ 넘침 ' + e));
  process.exit(errs ? 1 : 0);
})();
