#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
patch_v1984.py — T-Book v19.8.3 → v19.8.4
기준선 = 라이브 index.html (커밋 68f0fc3). 전부 assert 가드.

변경 (형님 지시 4건)
 1) 지역경찰 상단 「✅ 조문 검증 완료」 + 「⚠️ 아직 안 찍은 것」 메타 박스 2개 삭제
 2) 흉기소지 항목의 「형법 §116 오류」 경고 박스 삭제
 3) 지역경찰 꼬리 「🛴 …단속처리로 옮겼다」 안내 카드 삭제
 4) 🚦카드 ② 를 「남의 주민등록증·면허증」으로 확장 — 주민등록증 표 신설
 5) 버전 5곳 + 발자취 1항목
"""
import sys, io
sys.path.insert(0, '/home/claude/tb')
from parts_d import CARD2

SRC = '/home/claude/tb/base_v19.8.3.html'
OUT = '/home/claude/tb/TBook_v19.8.4.html'

s = io.open(SRC, encoding='utf-8').read()
LOG = []


def rep(old, new, label, n=1):
    global s
    c = s.count(old)
    assert c == n, '앵커 「%s」 %d개 (기대 %d) — 중단' % (label, c, n)
    s = s.replace(old, new, n)
    LOG.append('  ✓ %s' % label)


def L(f):
    return io.open('/home/claude/tb/' + f, encoding='utf-8').read()


# ── 1) 상단 메타 박스 2개 삭제 (뒤 공백줄 형태 유지)
rep(L('D1.txt'), '\n', '1) 상단 조문검증 안내 박스 2개 삭제')

# ── 2) 흉기 §116 경고 박스 삭제
rep(L('D2.txt'), '', '2) 흉기 §116 오류 경고 삭제')

# ── 3) 꼬리 이동안내 카드 삭제
rep(L('D3.txt'), '', '3) 「단속처리로 옮겼다」 카드 삭제')

# ── 4) 🚦카드 ② 주민등록증 보강
rep(L('D4.txt'), CARD2, '4) ② 주민등록증·면허증으로 확장')

# ── 4-2) 민원 표준답변 상단 경고문 축약 (형님 지시)
rep('<div style="font-size:12px;color:var(--text-dim);line-height:1.8;padding:8px;background:rgba(180,83,9,.10);border-left:4px solid #b45309;border-radius:6px">\n<b style="color:#b45309">⚠️ 참고자료입니다. 그대로 인용하지 마십시오.</b><br>\n경찰청 「민원 사례별 표준답변」(총 173개 중 교통 59개)을 요약한 것입니다. 원본은 <b>이미지 스캔을 문자변환한 것</b>이라 옮기는 과정에서 조문 번호·금액이 틀렸을 수 있습니다.<br>\n<b>답변서에 조문 번호를 적기 전에 반드시 국가법령정보센터 원문으로 대조하십시오.</b> 아래 <b style="color:#dc2626">🔴 표시</b>는 특히 의심되는 항목입니다.<br>\n지침 조문(교통단속 처리지침 제60·61·67·68·69조)은 <b>경찰청 내부 지침</b>이라 법령정보센터에 없습니다. 원본 지침으로 확인하십시오.\n</div>',
    '<div style="font-size:12px;color:var(--text-dim);line-height:1.8;padding:8px;background:rgba(180,83,9,.10);border-left:4px solid #b45309;border-radius:6px">\n<b style="color:#b45309">⚠️ 참고자료입니다. 필요시 원본을 확인 바랍니다.</b>\n</div>', '4-2) 민원답변 경고문 축약')

# -- 4-3) 지역경찰 상단 안내문 — 담당자 확인 문구 통합 (형님 지시)
rep('<div class="danger-box">🚨 <b>지역경찰 일반 — 교통 외 형사·여청 업무 요약</b><br>교통과 외근이라도 <b>공동대응·최초출동</b>으로 걸리는 사안들이다. 여기는 <b>「무엇을 확인하고 누구에게 넘기느냐」</b>만 적었다. 실제 처리는 해당 기능이 한다.</div>',
    '<div class="danger-box">🚨 <b>지역경찰 일반 — 교통 외 형사·여청 업무 요약</b><br>교통과 외근이라도 <b>공동대응·최초출동</b>으로 걸리는 사안들이다. 여기는 <b>「무엇을 확인하고 누구에게 넘기느냐」</b>만 적었다.<br><b>절차(서류·전산 흐름)는 관서·시기별로 다를 수 있으니 해당 기능 담당자 확인이 필요합니다.</b></div>', '4-3) 상단 안내문 담당자 확인 문구')

# ── 5) 버전 5곳
rep('<title>T-Book v19.8.3 (2026 정식배포판)</title>',
    '<title>T-Book v19.8.4 (2026 정식배포판)</title>', '5a) title')
rep('<span class="ver">v19.8.3</span>', '<span class="ver">v19.8.4</span>', '5b) 상단 배지')
rep('도입기부터 v19.8.3까지', '도입기부터 v19.8.4까지', '5c) 발자취 소제목')
rep('🚔 T-Book v19.8.3 (2026 정식배포판) · 2026.7 · 로컬처리 · 외부',
    '🚔 T-Book v19.8.4 (2026 정식배포판) · 2026.7 · 로컬처리 · 외부', '5d) footer-note')
rep('>T-Book v19.8.3 (2026 정식배포판)</div>',
    '>T-Book v19.8.4 (2026 정식배포판)</div>', '5e) 정보 카드')

# ── 6) 발자취
OLD_TR = ('<details style="margin:6px 0" open><summary style="font-weight:800;cursor:pointer;'
          'padding:6px 0">📱 v19.8.3 — 지역경찰 4단 재작성 + 폰 폭 수정 (2026.7.31)</summary>')
NEW_TR = ('<details style="margin:6px 0" open><summary style="font-weight:800;cursor:pointer;'
          'padding:6px 0">🪪 v19.8.4 — 신분증 확인 보강 + 군더더기 정리 (2026.7.31)</summary>'
          '<div class="u-p8-0"><p class="u-fs13">「지역경찰」 탭에서 <b>현장에서 안 쓰는 안내문을 걷어냈다</b> — '
          '조문 검증 경과 박스, 「형법 §116은 오류」 경고, PM·자전거를 단속처리로 옮겼다는 안내 카드. '
          '검증이 끝난 조문은 <b>해당 죄명 자리에 바로 적혀 있으면 되지</b>, 검증했다는 사실을 따로 알릴 필요가 없다.<br>'
          '대신 <b>「② 남의 주민등록증·면허증을 내민다」</b>를 키웠다. 종전에는 운전면허증만 있었는데 '
          '<b>주민등록증 표를 따로 붙였다</b> — 실물 · 이미지 파일 · 공식 모바일 · 조작 화면 · <b>번호만 부르는 경우</b> 5가지다. '
          '핵심은 <b>주민등록증은 형법 §230(공문서부정행사)이 아니라 주민등록법이 먼저</b>라는 것과, '
          '<b>공식 모바일 신분증은 실물과 같은 효력</b>이라는 것. '
          '현장 확인 요령도 <b>발급일자·주소 변경 이력</b>을 묻는 항목을 더했다 — 남의 것은 대개 여기서 막힌다.<br>'
          '⚠️ <b>주민등록법 §37의 세부 항·호는 아직 원문을 못 찍었다.</b> 제약 11대로 <b>번호를 빼고 내용만</b> 적었다. '
          'v19.7 자배법 「40만원」이 바로 이 자리에서 나온 오류다.</p></div></details>'
          + OLD_TR)
rep(OLD_TR, NEW_TR, '6) 발자취 v19.8.4 항목')

io.open(OUT, 'w', encoding='utf-8').write(s)
print('── patch_v1984.py')
for l in LOG:
    print(l)
print('  → %s  (%d bytes)' % (OUT, len(s.encode('utf-8'))))
