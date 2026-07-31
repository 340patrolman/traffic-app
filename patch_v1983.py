#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
patch_v1983.py — T-Book v19.8.2 → v19.8.3
전부 assert 가드. 앵커가 1개가 아니면 즉시 중단(HANDOFF 3-1 ①).

변경
 1) #page-police_gen 스코프 CSS 삽입 — 360px 가로넘침(+804px 실측) 해소 + 4단 뼈대
 2) 「🚦 교통 단속에서 바로 이어지는 3가지」 4단 + 사례 재작성
 3) 지역경찰 형사·여청 카드 3개 → 우선순위 재배열 + 전 항목 4단화 + 사례
 4) 「🧩 다음 판 후보」 카드 → 🚓 단속처리 이동 안내로 교체
 5) 🚓 단속처리(enforce)에 「🛴 PM·자전거·약물·보복」 카드 신설
 6) 버전 5곳 + 발자취 1항목
"""
import sys, io, re
sys.path.insert(0, '/home/claude/tb')
from parts_css_a import CSS, CARD_A
from parts_b import CARDS
from parts_c import ENFORCE_CARD, TAIL_CARD

SRC = '/home/claude/tb/base_v19.8.2.html'
OUT = '/home/claude/tb/TBook_v19.8.3.html'

s = io.open(SRC, encoding='utf-8').read()
LOG = []


def rep(old, new, label, n=1):
    global s
    c = s.count(old)
    assert c == n, '앵커 「%s」 %d개 (기대 %d) — 중단' % (label, c, n)
    s = s.replace(old, new, n)
    LOG.append('  ✓ %s' % label)


# ── 1) 페이지 여는 태그에 pg-narrow 클래스 + 스코프 CSS 삽입
rep('<div class="page" id="page-police_gen">\n',
    '<div class="page pg-narrow" id="page-police_gen">\n' + CSS,
    '1) CSS 삽입 + pg-narrow 클래스')

# ── 2) 교통 연결 카드 재작성
OLD_A = io.open('/home/claude/tb/OLD_A.txt', encoding='utf-8').read()
assert OLD_A.startswith(' <div class="card"'), 'OLD_A 앵커 파일 이상'
rep(OLD_A, ' ' + CARD_A.rstrip('\n') + '\n', '2) 교통 연결 3가지 4단 재작성')

# ── 3) 형사·여청 카드 3개 통째 교체 (우선순위 재배열)
OLD_B = io.open('/home/claude/tb/OLD_B.txt', encoding='utf-8').read()
rep(OLD_B, ' ' + CARDS.rstrip('\n') + '\n\n', '3) 형사·여청 19개 4단화 + 사례')

# ── 4) 꼬리 카드 교체
OLD_C = io.open('/home/claude/tb/OLD_C.txt', encoding='utf-8').read()
rep(OLD_C, ' ' + TAIL_CARD.rstrip('\n') + '\n', '4) 다음 판 후보 카드 → 이동 안내')

# ── 5) 단속처리 페이지에 카드 신설
ANCHOR_E = ('goCard(\'sop\',\'sop_enforce\',\'us_safety\')">🇺🇸 오피서 세이프티 전문'
            '</button></div></div></div>\n</div> ')
rep(ANCHOR_E,
    ANCHOR_E.replace('</div></div></div>\n</div> ',
                     '</div></div></div>\n' + ENFORCE_CARD.rstrip('\n') + '\n</div> '),
    '5) 단속처리에 PM·자전거·약물·보복 카드 신설')

# ── 6) 버전 5곳
rep('<title>T-Book v19.8.2 (2026 정식배포판)</title>',
    '<title>T-Book v19.8.3 (2026 정식배포판)</title>', '6a) title')
rep('<span class="ver">v19.8.2</span>', '<span class="ver">v19.8.3</span>', '6b) 상단 배지')
rep('도입기부터 v19.8.2까지', '도입기부터 v19.8.3까지', '6c) 발자취 소제목')
rep('🚔 T-Book v19.8.2 (2026 정식배포판) · 2026.7 · 로컬처리 · 외부',
    '🚔 T-Book v19.8.3 (2026 정식배포판) · 2026.7 · 로컬처리 · 외부', '6d) footer-note')
rep('>T-Book v19.8.2 (2026 정식배포판)</div>',
    '>T-Book v19.8.3 (2026 정식배포판)</div>', '6e) 정보 카드')

# ── 7) 발자취 항목 추가 (v19.8.2 항목 앞에, open 은 새 항목으로 이동)
OLD_TR = ('<details style="margin:6px 0" open><summary style="font-weight:800;cursor:pointer;'
          'padding:6px 0">🚦 v19.8.2 — 지역경찰 일반 조문 검증 + 교통 연결 (2026.7.30)</summary>')
NEW_TR = ('<details style="margin:6px 0" open><summary style="font-weight:800;cursor:pointer;'
          'padding:6px 0">📱 v19.8.3 — 지역경찰 4단 재작성 + 폰 폭 수정 (2026.7.31)</summary>'
          '<div class="u-p8-0"><p class="u-fs13">「지역경찰」 탭이 <b>360px 화면에서 표가 1,129px까지 늘어나</b> '
          '옆으로 잘려 나가고 있었다. 원인은 전 앱 공통의 <b>표 가로스크롤 규칙(td 줄바꿈 금지)</b>이 이 탭에만 '
          '해제돼 있지 않았던 것 — 서류매뉴얼·계절대비 탭에 이미 있던 해제 패턴을 그대로 적용해 '
          '<b>실측 넘침을 0으로</b> 만들었다. 앞선 검사가 이걸 못 잡은 이유는 <b>body에 overflow-x:hidden</b>이 '
          '걸려 있어 문서 폭만 재면 정상으로 보였기 때문이다.<br>'
          '내용도 전부 다시 썼다. 19개 항목을 <b>「📞 이런 신고다 → 🚗 도착해서 먼저 → 🔍 무엇으로 갈리나 → '
          '📮 어디로 넘긴다」 4단</b>으로 통일하고, 급할 때 눈이 가도록 <b>「⚠️ 이것만은 하지 마라」</b>와 '
          '<b>현장 사례</b>를 붙였다. 순서도 교통 외근이 실제로 걸리는 순서(수배 → 신분증 → 즉결 → 피싱 → '
          '변사·흉기 → 여청 → 나머지 형사)로 바꿨다.<br>'
          '교통인데 절차가 다른 <b>PM·자전거·약물·보복 4가지</b>는 <b>🚓 단속처리</b> 페이지로 옮겨 같은 4단으로 '
          '넣었다 — 탭을 늘리면 360px에서 서브탭이 한 줄 더 생기기 때문이다.</p></div></details>'
          + OLD_TR)
rep(OLD_TR, NEW_TR, '7) 발자취 v19.8.3 항목')

io.open(OUT, 'w', encoding='utf-8').write(s)
print('── patch_v1983.py')
for l in LOG:
    print(l)
print('  → %s  (%d bytes)' % (OUT, len(s.encode('utf-8'))))
