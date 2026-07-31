# -*- coding: utf-8 -*-
"""v19.8.3 패치 조각 1 — #page-police_gen 스코프 CSS + 교통 연결 카드 재작성"""

# ══════════════════════════════════════════════════════════════════
# A. 스코프 CSS — 360px 가로넘침 해소 + 4단 뼈대
#    근본원인: 전역 `.tbl-scroll th,.tbl-scroll td{white-space:nowrap}` +
#    `.tbl-scroll>table{width:max-content}` 가 걸려 표가 1129px까지 늘어났다.
#    #page-doc_manual · #page-sop_season 에 이미 있는 해제 패턴을 그대로 따른다.
# ══════════════════════════════════════════════════════════════════
CSS = '''<style>
/* ═══ v19.8.3 — 좁은 화면 표 줄바꿈 (.pg-narrow) ═══
   원인: 전역 `.tbl-scroll th,.tbl-scroll td{white-space:nowrap}` +
   `.tbl-scroll>table{width:max-content}` 때문에 360px에서 표가 1,129px까지 늘어났다.
   body{overflow-x:hidden} 이라 문서 폭만 재면 정상으로 보여 종전 검사가 못 잡았다.
   #page-doc_manual · #page-sop_season 에 이미 있는 해제 패턴을 그대로 따른다. */
.pg-narrow .tbl-scroll{overflow-x:visible}
.pg-narrow .tbl-scroll>table{width:100%!important;max-width:100%!important;min-width:0!important;table-layout:fixed}
.pg-narrow .tbl-scroll th,.pg-narrow .tbl-scroll td{white-space:normal!important;word-break:keep-all;overflow-wrap:anywhere;font-size:12px!important;line-height:1.55;padding:6px 7px!important;border:1px solid var(--border);vertical-align:top;text-align:left}
.pg-narrow .tbl-scroll th{background:var(--panel-2);font-weight:800;text-align:center}
.pg-narrow .mp-t{border-collapse:collapse;margin:8px 0}
.pg-narrow .mp-t td:first-child{width:31%;text-align:center;font-weight:700;background:var(--bg)}
.pg-narrow .tbl-more{display:none!important}
/* ═══ v19.8.3 — 4단 뼈대 (신고 접수 → 현장 도착 → 무엇으로 갈리나 → 어디로 넘긴다) ═══ */
.pg-f{margin:10px 0 2px}
.pg-s{border-left:4px solid var(--border);border-radius:0 8px 8px 0;background:var(--bg);padding:7px 0 7px 10px;margin:0 0 7px;min-width:0}
.pg-s h6{margin:0 0 3px;font-size:12.5px;font-weight:900;letter-spacing:.2px;color:var(--text-dim)}
.pg-s div{font-size:13.5px;line-height:1.68;word-break:keep-all;overflow-wrap:anywhere;min-width:0}
.pg-s1{border-left-color:var(--text-dim)}
.pg-s2{border-left-color:var(--danger)}.pg-s2 h6{color:var(--danger)}
.pg-s3{border-left-color:var(--warn)}.pg-s3 h6{color:var(--warn)}
.pg-s4{border-left-color:var(--accent)}.pg-s4 h6{color:var(--accent)}
.pg-no{background:rgba(220,38,38,.07);border:1px solid var(--danger);border-radius:9px;padding:7px 9px;margin:0 0 7px;font-size:12.5px;line-height:1.6;word-break:keep-all;overflow-wrap:anywhere}
.pg-case{background:var(--panel-2);border-radius:9px;padding:8px 9px;margin:0 0 4px;font-size:12.5px;line-height:1.65;word-break:keep-all;overflow-wrap:anywhere}
.pg-case b.cs{display:inline-block;background:var(--accent);color:#fff;border-radius:5px;padding:0 5px;margin-right:4px;font-size:11px;font-weight:800}
.pg-sum{font-weight:800;font-size:13.5px;margin:12px 0 2px;padding:8px 6px;cursor:pointer;list-style:none;background:var(--panel-2);border-radius:9px;word-break:keep-all;overflow-wrap:anywhere;min-height:0}
.pg-sum::-webkit-details-marker{display:none}
.pg-sum::after{content:' ▼';font-size:10px;color:var(--text-dim)}
details[open]>.pg-sum::after{content:' ▲'}
.pg-h{font-weight:800;font-size:13.5px;margin:14px 0 2px;word-break:keep-all;overflow-wrap:anywhere}
#page-police_gen .card{padding:13px 12px 11px}
.pg-narrow details>div{word-break:keep-all;overflow-wrap:anywhere;min-width:0}
</style>
'''

# ══════════════════════════════════════════════════════════════════
# B. 「🚦 교통 단속에서 바로 이어지는 3가지」 — 4단 뼈대 + 사례로 전면 재작성
# ══════════════════════════════════════════════════════════════════
CARD_A = '''<div class="card" style="border:2px solid var(--accent-gold)">
  <div class="card-title">🚦 교통 단속에서 바로 이어지는 3가지</div>
  <div class="info-box u-fs13"><b>면허증 한 장에서 다 갈린다.</b> 차 세우고 신분 확인하는 순간 나오는 것들이라 교통 업무와 제일 많이 겹친다. <b>여기 셋만 몸에 붙여도 대부분 막힌다.</b></div>

  <details open><summary class="pg-sum">① 조회했더니 수배가 뜬다 — A / B / C</summary>
  <div class="pg-f">
   <div class="pg-s pg-s1"><h6>📞 이런 신고다</h6><div>신고가 아니라 <b>내가 만든 상황</b>이다. 신호위반·음주·무면허로 차를 세우고 면허증을 받아 조회를 눌렀는데 <b>화면에 수배가 뜬다.</b></div></div>
   <div class="pg-s pg-s2"><h6>🚗 도착해서 먼저</h6><div>① <b>표정을 바꾸지 않는다</b> — 화면을 본 순간 티가 나면 상대가 먼저 움직인다<br>② <b>지원부터 부른다</b> — 무전으로 위치·차량번호·인원. A수배는 혼자 붙지 않는다<br>③ <b>차 열쇠와 동승자</b> — 시동 걸린 채면 도주가 제일 쉽다. 하차 유도 후 열쇠 확보<br>④ <b>고지는 지원 도착 후</b> — 미란다 고지는 신병을 잡을 수 있는 상태에서</div></div>
   <div class="pg-s pg-s3"><h6>🔍 무엇으로 갈리나</h6><div>화면에 뜬 <b>수배 종류 한 글자</b>로 갈린다.
   <table class="mp-t">
    <tr><th>구분</th><th>현장에서 무엇을 하나</th></tr>
    <tr><td><b>A수배</b><br>지명수배</td><td><b>체포한다.</b> 미란다 고지 → 형사팀 인계</td></tr>
    <tr><td><b>B수배</b><br>형집행장</td><td><b>벌금 미납이다.</b> 미란다 고지 후 형집행. <b>납부하면 그 자리에서 귀가</b></td></tr>
    <tr><td><b>C통보</b><br>지명통보</td><td><b>체포하지 않는다.</b> 현장에서 폴리폰으로 끝난다</td></tr>
    <tr><td><b>겹칠 때</b></td><td>여러 건이면 <b>경찰 지명수배 1건만</b> 작성하고 그 안에 전부 기록. <b>A+B면 A서류에 B내용 포함</b></td></tr>
   </table></div></div>
   <div class="pg-s pg-s4"><h6>📮 어디로 넘긴다</h6><div><b>A</b> — 형사팀. KICS <b>기소중지사건접수</b>로 접수.<br>　서류: 검거보고 · 확인서 · 신체확인서 · 체포/구속통지서<br><b>B</b> — 검찰청 <b>징수계 웹팩스</b>로 형집행장 수령. 미납이면 검거보고서 · 확인서 · 구인통지서<br>　⚠️ <b>형집행장 교부확인서를 반드시 받는다</b><br><b>C</b> — 넘기지 않는다. 지명통보사실 통지서 2부 + 지명통보자발견보고 2부<br><b>원 단속(신호·음주·무면허)은 교통에서 그대로 처리</b>한다. 두 갈래로 나가는 것이 정상이다.</div></div>
   <div class="pg-no">⚠️ <b>이것만은 하지 마라</b> — <b>통고처분서만 끊고 보내면 수배자를 놓친 것이 된다.</b> 교통단속으로 세운 차에서 A·B가 뜨면 그때부터 교통 사건이 아니다. <b>단속은 단속대로, 신병은 별건으로.</b></div>
   <div class="pg-case"><b class="cs">사례 1</b> 새벽 음주단속에서 걸린 40대. 수치는 훈방 수준이었는데 조회에 <b>A수배</b>가 떴다. 통고처분서만 발부하고 보냈다면 지명수배자를 그대로 놓친 것이다. — <b>조회 화면을 끝까지 읽는다.</b> 위반 결과만 보고 창을 닫지 않는다.</div>
   <div class="pg-case"><b class="cs">사례 2</b> 신호위반으로 세운 차에서 <b>B수배(벌금 미납)</b>. 미란다 고지 후 형집행장을 받는 동안 가족이 계좌이체로 납부해 <b>그 자리에서 귀가</b>. 이때 <b>교부확인서를 안 받으면</b> 나중에 「받은 적 없다」가 된다. — <b>서명 한 줄이 서류 전체를 지킨다.</b></div>
   <div class="pg-case"><b class="cs">사례 3</b> <b>A와 B가 같이</b> 뜬 경우. 서류를 두 벌 만들지 않는다. <b>A서류에 B내용을 포함</b>해 한 건으로 정리한다. 현행범 + B면 <b>검거보고서만</b>.</div>
  </div>

  </details>
  <details><summary class="pg-sum">② 남의 면허증을 내민다 — 무엇에 썼는지로 갈린다</summary>
  <div class="pg-f">
   <div class="pg-s pg-s1"><h6>📞 이런 신고다</h6><div>「면허증 좀 봅시다」 했는데 <b>사진이 본인과 다르다.</b> 또는 지갑 대신 <b>휴대폰 화면</b>을 내민다.</div></div>
   <div class="pg-s pg-s2"><h6>🚗 도착해서 먼저</h6><div>① <b>사진 대조</b> — 얼굴이 아니라 <b>귀·턱선·눈썹</b>을 본다. 사진은 오래됐어도 골격은 안 변한다<br>② <b>생년월일을 말로 물어본다</b> — 현장에서 제일 빠른 확인이다. 카드 보고 읽으면 눈이 아래로 간다<br>③ <b>주소 뒷부분</b>을 이어서 묻는다 — 앞자리는 외워도 뒷자리는 못 외운다<br>④ 말이 막히면 <b>무면허·음주를 의심</b>한다. 남의 면허증을 내미는 이유는 대개 둘 중 하나다</div></div>
   <div class="pg-s pg-s3"><h6>🔍 무엇으로 갈리나</h6><div><b>「무엇을 내밀었는가」</b>로 죄명이 완전히 갈린다.
   <table class="mp-t">
    <tr><th>제시한 것</th><th>적용</th></tr>
    <tr><td>타인의 <b>실물</b> 면허증</td><td><b>공문서부정행사</b>(형법 §230) — 2년 이하 징역·금고 또는 500만원 이하 벌금 <b>[A등급]</b></td></tr>
    <tr><td>면허증 <b>사진·이미지 파일</b></td><td>공문서부정행사 <b>적용 곤란</b> — 문서 자체를 행사한 것이 아니다. 다른 죄명을 찾아야 한다</td></tr>
    <tr><td><b>공식 모바일</b> 신분증</td><td>도로교통법 계열로 검토 <b>[항·호 미검증]</b></td></tr>
    <tr><td><b>가짜 모바일 화면</b>·조작 캡처</td><td><b>전자기록 위·변조</b> 검토</td></tr>
    <tr><td><b>주민등록번호만</b> 불러줌</td><td>주민등록법(번호 부정사용) 검토 <b>[호 미검증]</b></td></tr>
    <tr><td>면허증 <b>양도·대여</b></td><td>도로교통법 — <b>주는 쪽도 처벌</b>된다</td></tr>
   </table></div></div>
   <div class="pg-s pg-s4"><h6>📮 어디로 넘긴다</h6><div><b>공문서부정행사·전자기록 위변조</b> → 형사팀 발생보고<br><b>원 단속(무면허·음주)</b> → 교통에서 그대로. <b>본인 명의로 다시 특정</b>해 서류를 고쳐 쓴다<br><b>면허증을 빌려준 사람</b>도 별도 입건 대상 — 인적사항을 받아둔다<br>👉 <b>근거 사진 필수</b> — 제시된 면허증·모바일 화면을 <b>그 자리에서 촬영</b>한다. 돌려주면 끝이다</div></div>
   <div class="pg-no">⚠️ <b>이것만은 하지 마라</b> — <b>「본인 맞습니까」로 끝내지 말 것.</b> 그리고 <b>이미지 파일에 §230을 그대로 붙이지 말 것</b> — 실물이 아니면 공문서부정행사는 적용이 곤란하다. 여기서 죄명을 잘못 적으면 뒤에서 전부 무너진다.</div>
   <div class="pg-case"><b class="cs">사례 1</b> 무면허 상태의 동생이 <b>형의 면허증</b>을 내밀었다. 사진이 비슷해 넘어갈 뻔했으나 <b>생년월일을 물으니 막혔다.</b> → 무면허운전 + 공문서부정행사, 빌려준 형도 대여로 검토.</div>
   <div class="pg-case"><b class="cs">사례 2</b> 「모바일 운전면허증 있습니다」 하며 화면을 보여줬는데 <b>캡처 이미지</b>였다. 공식 앱은 <b>실시간 갱신 표시·QR</b>가 있다. <b>새로고침을 시켜보면</b> 바로 갈린다. → 조작 화면이면 전자기록 위·변조 검토.</div>
   <div class="pg-case"><b class="cs">사례 3</b> 대리운전 기사가 <b>업체 다른 기사의 면허증</b>을 소지. 본인 면허가 정지 중이었다. — <b>정지·취소 상태는 면허증 실물로는 안 보인다.</b> 반드시 조회로 확인.</div>
  </div>

  </details>
  <details><summary class="pg-sum">③ 통고처분을 거부한다 — 즉결심판</summary>
  <div class="pg-f">
   <div class="pg-s pg-s1"><h6>📞 이런 신고다</h6><div>「스티커 안 받겠다」 「서명 못 한다」 「법정에서 다투겠다」. PM·자전거 음주나 경범죄 통고에서 제일 많이 나온다.</div></div>
   <div class="pg-s pg-s2"><h6>🚗 도착해서 먼저</h6><div>① <b>강요하지 않는다</b> — 수령을 거부할 권리 자체는 있다. 실랑이가 길어지면 그게 민원이 된다<br>② <b>거부 의사와 경위를 그 자리에서 기록</b> — 시각·발언·태도. 가능하면 <b>영상</b><br>③ <b>인적사항을 먼저 확실히 잡는다</b> — 이게 안 되면 즉결심판도 못 간다<br>④ 「즉결심판으로 넘어가고 <b>법정에서 말씀하시면 된다</b>」고 안내한다. 이 한 마디로 대부분 정리된다</div></div>
   <div class="pg-s pg-s3"><h6>🔍 무엇으로 갈리나</h6><div>
   <table class="mp-t">
    <tr><th>확인</th><th>안 되면</th></tr>
    <tr><td><b>인적사항이 확실한가</b></td><td>불확실하면 <b>통고처분 자체가 불가</b> → 신원 확보가 먼저</td></tr>
    <tr><td><b>통고서 수령을 거부하나</b></td><td>거부면 통고 불가 → <b>즉결심판</b></td></tr>
    <tr><td><b>범칙금 대상 위반인가</b></td><td>형사입건 대상이면 즉결이 아니라 <b>발생보고</b></td></tr>
   </table>
   💡 이 구조는 <b>의무보험 미가입</b>과 똑같다(자배법 §51① 단서). <b>「이름·주소가 확실한가」가 모든 통고처분의 첫 관문</b>이다.</div></div>
   <div class="pg-s pg-s4"><h6>📮 어디로 넘긴다</h6><div><b>폴리폰 순서</b> — 경범단속 → 인적사항 등록 → 수배정보 확인 → 하단 <b>「즉결심판」</b> → 출석장소는 <b>「추후 통보」</b> → 발부<br><b>서류 6종</b> — 즉결심판 청구서 · 적발보고서 · 출석통지서 · <b>112처리표</b> · 단속경위서 · 사진<br>피해자 정보는 필요할 때만. → <b>📝 서류작성 · 🛡️ 무보험 ③카드</b> 참조</div></div>
   <div class="pg-no">⚠️ <b>이것만은 하지 마라</b> — 서명을 받아내려고 붙잡고 있지 말 것. <b>거부는 거부대로 기록하고 즉결로 넘기는 것이 정답</b>이다. 억지 서명은 나중에 전부 다툼거리가 된다.</div>
   <div class="pg-case"><b class="cs">사례 1</b> PM 음주 20대가 「킥보드인데 무슨 음주냐」며 스티커 거부. 실랑이 대신 <b>거부 경위를 영상으로 남기고 즉결심판</b>으로 발부. 현장이 5분 만에 정리됐다.</div>
   <div class="pg-case"><b class="cs">사례 2</b> 무전취식 신고. 상대가 신분증이 없고 진술도 오락가락 — <b>인적사항이 확실하지 않아 통고처분 자체가 불가</b>. 신원 확인이 먼저였다.</div>
   <div class="pg-case"><b class="cs">사례 3</b> 의무보험 미가입 차량. 운전자가 통고서 수령을 거부 → <b>자배법 §51① 단서로 통고 불가</b>. 교통과 경범이 같은 구조라는 것을 알면 현장에서 헷갈리지 않는다.</div>
  </div>
  </details>
 </div>
'''
