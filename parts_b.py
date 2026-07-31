# -*- coding: utf-8 -*-
"""v19.8.3 패치 조각 2 — 지역경찰 19개 항목 4단 재작성 (우선순위 재배열 + 사례)"""

# 우선순위(이사안내 4-3): 4 보이스피싱 · 5 변사/흉기 · 6 여청 · 7 나머지 형사
# 1~3(수배·신분증·즉결)은 맨 위 🚦 카드에서 4단으로 끝냈다. 여기는 전산·서류 심화만 남긴다.

CARDS = '''<div class="card" style="border:2px solid var(--accent-gold)">
  <div class="card-title">🔎 최초출동으로 걸리는 것 — 피싱 · 변사 · 흉기</div>
  <div class="info-box u-fs13">공동대응이 제일 많이 걸리는 순서로 놓았다. <b>돈이 나갔으면 시간, 사람이 쓰러졌으면 생명, 흉기가 있으면 거리</b>가 먼저다.</div>

  <details><summary style="font-weight:800;padding:6px 0">📞 보이스피싱 — 돈이 이미 나갔다</summary><div class="u-p8-0">
   <div class="pg-f">
    <div class="pg-s pg-s1"><h6>📞 이런 신고다</h6><div>「검찰이라며 전화가 왔는데 계좌로 보냈다」 「아들인 줄 알고 보냈다」 「지금 사람을 만나 돈을 건네러 간다」.</div></div>
    <div class="pg-s pg-s2"><h6>🚗 도착해서 먼저</h6><div>① <b>돈이 나간 시각과 방법을 먼저 묻는다</b> — 이체냐 현금이냐로 다음 행동이 완전히 갈린다<br>② <b>이체면 그 자리에서 지급정지</b>. 위로·설명은 그 다음이다. <b>몇 분 차이로 남고 없어진다</b><br>③ <b>휴대폰을 뺏지 않는다</b> — 통화기록·문자·앱이 전부 증거다<br>④ 피해자가 <b>아직 통화 중</b>이면 끊게 하되, 통화내역·상대 번호를 먼저 확보</div></div>
    <div class="pg-s pg-s3"><h6>🔍 무엇으로 갈리나</h6><div><b>돈이 어떻게 나갔는가</b>로 갈린다.
    <table class="mp-t">
     <tr><th>방법</th><th>현장 조치</th></tr>
     <tr><td><b>계좌이체</b></td><td><b>1394</b>(통합대응단) 경유해 은행에 <b>즉시 지급정지</b> → 피해신고확인서 발급 → 피해구제신청 안내. 환급절차는 <b>1332</b>(금감원)</td></tr>
     <tr><td><b>직접전달</b><br>특정장소 보관</td><td><b>수거책을 만날 예정이면 현장출동·검거.</b> 지역경찰·형사팀 공조. 피해자는 <b>평소처럼</b> 행동하게 한다</td></tr>
     <tr><td><b>상품권</b></td><td>PIN을 전송했으면 <b>발행업체에 즉시 취소 가능 여부</b> 확인</td></tr>
    </table></div></div>
    <div class="pg-s pg-s4"><h6>📮 어디로 넘긴다</h6><div>발생보고 → <b>형사팀(수사)</b>. 수거책 검거 예정이면 <b>지역경찰·형사팀 합동</b>.<br>피해자에게는 <b>피해신고확인서 · 피해구제신청 · 1332</b> 세 가지를 반드시 안내한다.</div></div>
    <div class="pg-no">⚠️ <b>이것만은 하지 마라</b> — 「일단 진정하시고 자세히 말씀해 보세요」로 시간을 쓰지 말 것. <b>지급정지가 먼저다.</b> 사연은 정지 걸어두고 들어도 늦지 않다.</div>
    <div class="pg-case"><b class="cs">사례 1</b> 70대 피해자가 「검찰 수사관」에게 3천만원 이체. 신고 접수까지 40분이 걸렸지만 <b>현장에서 바로 1394로 지급정지</b>를 걸어 절반 이상이 계좌에 남아 있었다. — <b>시간이 곧 금액이다.</b></div>
    <div class="pg-case"><b class="cs">사례 2</b> 「금감원 직원이 집으로 현금을 받으러 온다」는 신고. 피해자를 평소대로 행동하게 하고 <b>인근에 잠복해 수거책을 검거</b>. 미리 요란하게 출동했으면 놓쳤을 건이다.</div>
   </div>
  </div></details>

  <details><summary style="font-weight:800;padding:6px 0">📵 보이스피싱·스미싱 — 아직 돈은 안 나갔다</summary><div class="u-p8-0">
   <div class="pg-f">
    <div class="pg-s pg-s1"><h6>📞 이런 신고다</h6><div>「이상한 문자 링크를 눌렀다」 「인증번호를 알려줬다」 「개인정보를 불러줬다」 「전화만 받았는데 불안하다」.</div></div>
    <div class="pg-s pg-s2"><h6>🚗 도착해서 먼저</h6><div>① <b>초기화 전에 증거부터 캡처</b>한다 — 악성파일·통화녹음·문자내역. 지워버리면 아무것도 안 남는다<br>② 악성앱이 의심되면 <b>데이터·와이파이·블루투스 차단</b>이 1순위<br>③ <b>피해 없음을 확실히 말해준다</b> — 불안이 2차 피해를 만든다</div></div>
    <div class="pg-s pg-s3"><h6>🔍 무엇으로 갈리나</h6><div>
    <table class="mp-t">
     <tr><th>무엇을 했나</th><th>조치</th></tr>
     <tr><td><b>통화·문자만</b></td><td>피해 없음 설명. 번호제보는 통합대응단 홈페이지. 예방은 <b>금감원 개인정보노출자 사고예방시스템 · 엠세이퍼 · PASS 명의도용방지</b></td></tr>
     <tr><td><b>개인정보를 알려줌</b></td><td><b>118</b> 신고 + 노출자 시스템 등록</td></tr>
     <tr><td><b>악성앱 설치</b><br>링크 클릭</td><td>통신 차단 → 증거 캡처 → 백신(V3·알약M·싹다잡아)으로 확인·삭제·<b>휴지통 비우기</b> → 신분증 이미지·메모장·다운로드 폴더 점검 → <b>초기화 검토</b></td></tr>
     <tr><td><b>인증번호를 알려줌</b></td><td>통신사·엠세이퍼에서 <b>명의 개통 여부</b> 확인, 콜센터에서 <b>소액결제 차단</b></td></tr>
    </table></div></div>
    <div class="pg-s pg-s4"><h6>📮 어디로 넘긴다</h6><div>금전 피해가 없으면 <b>안내로 종결</b>이 원칙. 명의도용·개통이 확인되면 그때 발생보고.<br>👉 <b>「지금은 피해가 없다」는 것을 명확히 말해주는 것</b>도 조치다.</div></div>
    <div class="pg-case"><b class="cs">사례</b> 택배 사칭 문자 링크를 누른 30대. 곧바로 초기화하려던 것을 막고 <b>악성앱 목록과 문자를 먼저 캡처</b>했다. 이후 같은 번호대의 다발 신고를 묶는 자료가 됐다.</div>
   </div>
  </div></details>

  <details><summary style="font-weight:800;padding:6px 0">🕯️ 변사자 신고</summary><div class="u-p8-0">
   <div class="pg-f">
    <div class="pg-s pg-s1"><h6>📞 이런 신고다</h6><div>「사람이 쓰러져 있는데 안 움직인다」 「연락이 안 돼 문을 열었더니…」 「한강변에 사람이 있다」.</div></div>
    <div class="pg-s pg-s2"><h6>🚗 도착해서 먼저</h6><div>① <b>단정하지 않는다.</b> 사망 판단은 <b>의료전문가 우선</b> — 119 합동 출동<br>② <b>생명구호가 현장보존보다 먼저다.</b> 둘이 충돌하면 사람이 먼저<br>③ 사망이 확인되면 <b>폴리스라인·현장훼손 금지</b><br>④ 노출된 장소면 <b>백색 천</b>으로 가린다 — 유족·행인 2차 충격을 막는다</div></div>
    <div class="pg-s pg-s3"><h6>🔍 무엇으로 갈리나</h6><div>
    <table class="mp-t">
     <tr><th>상태</th><th>처리</th></tr>
     <tr><td><b>아직 사망하지 않음</b></td><td>119 인계·후송. 자살기도 추정이라도 <b>상태·현장을 반드시 확인</b></td></tr>
     <tr><td><b>사망 확인</b></td><td>정밀감식 필요 여부 판단 → 현장보존 → 참고인 인적사항·사건개요 확인 → <b>체크리스트</b> 작성·보고</td></tr>
    </table></div></div>
    <div class="pg-s pg-s4"><h6>📮 어디로 넘긴다</h6><div>변사 발생보고 → <b>형사팀</b>. 감식 필요 시 과학수사 요청.<br>유족에게는 <b>절차를 한 번에 다 말하지 않는다</b> — 지금 필요한 것만.</div></div>
    <div class="pg-no">⚠️ <b>이것만은 하지 마라</b> — 「돌아가신 것 같다」고 현장에서 단정하지 말 것. 그리고 <b>현장을 정리하지 말 것</b> — 치워둔 것이 나중에 전부 문제가 된다.</div>
    <div class="pg-case"><b class="cs">사례</b> 한강공원 순찰 중 벤치에 엎드려 있는 사람. 취객으로 보고 지나쳤다면 놓쳤을 건이었다. <b>흔들어 반응을 확인</b>하는 3초가 전부였다.</div>
   </div>
  </div></details>

  <details><summary style="font-weight:800;padding:6px 0">🔪 공공장소 흉기소지</summary><div class="u-p8-0">
   <div class="pg-f">
    <div class="pg-s pg-s1"><h6>📞 이런 신고다</h6><div>「칼을 들고 다니는 사람이 있다」 「가방에서 흉기가 보였다」 「지하철역에서 쇠파이프를 들고 있다」.</div></div>
    <div class="pg-s pg-s2"><h6>🚗 도착해서 먼저</h6><div>① <b>거리부터 확보한다.</b> 붙지 않는다. 지원 도착 전 단독 접근 금지<br>② <b>흉기와 대상자를 분리</b>하는 것이 1순위. 사람을 잡기 전에 물건을 떼어놓는다<br>③ 주변 <b>일반인을 먼저 물린다</b><br>④ <b>정신질환·자·타해 위험</b>이 의심되면 보호조치·응급입원 요건을 별도로 본다</div></div>
    <div class="pg-s pg-s3"><h6>🔍 무엇으로 갈리나</h6><div><b>세 가지가 모두 맞아야</b> 경범죄가 된다.
    <table class="mp-t">
     <tr><th>확인</th><th>내용</th></tr>
     <tr><td><b>장소</b></td><td>불특정·다수인이 이용·통행하는 <b>공공장소</b>인가</td></tr>
     <tr><td><b>이유</b></td><td><b>정당한 이유 없이</b> 숨겨서 지니고 다녔는가 (직업·용도가 있으면 다르다)</td></tr>
     <tr><td><b>상태</b></td><td>주변이 <b>불안·공포</b>를 느낄 상태였는가</td></tr>
     <tr><td><b>더 있으면</b></td><td>위해를 가할 정황이 더해지면 <b>폭력행위처벌법·특수협박</b> 등 별도 검토</td></tr>
    </table></div></div>
    <div class="pg-s pg-s4"><h6>📮 어디로 넘긴다</h6><div>구성요건이 불명확하면 <b>형사기능과 협의</b> → 주거침입·특수협박 등 병행 검토 → 명백하면 <b>팀장 보고·지휘</b> 후 체포 판단.<br>조사·초기조치를 <b>구체적으로 기록</b>한다.<br><span style="color:var(--text-dim)">근거(A등급 확정): <b>경범죄처벌법 §3①2호(흉기의 은닉휴대)</b> — 「칼·쇠몽둥이·쇠톱 등 사람의 생명 또는 신체에 중대한 위해를 끼치거나 건조물에 침입하는 데에 사용될 수 있는 연장이나 기구를 <b>정당한 이유 없이 숨겨서 지니고 다니는 사람</b>」 → 10만원 이하 벌금·구류·과료</span></div></div>
    <div class="pg-no">⚠️ <b>원본 매뉴얼의 「형법 §116」은 오류다.</b> §116은 <b>다중불해산</b>이라 흉기와 무관하다. 서류에 §116을 적으면 그대로 무너진다. — v19.8.2에서 law.go.kr 원문으로 잡았다.</div>
    <div class="pg-case"><b class="cs">사례</b> 시장 상인이 <b>회칼을 손에 든 채</b> 도로변으로 나온 신고. 직업상 소지라 <b>「숨겨서」</b>에 해당하지 않아 경범죄 구성이 어려웠다. — <b>은닉성이 요건이다.</b> 드러내 들고 있으면 다른 죄명을 봐야 한다.</div>
   </div>
  </div></details>

  <details><summary style="font-weight:800;padding:6px 0">📌 수배처리 — 전산·서류 심화 (현장 4단은 맨 위 🚦카드)</summary><div class="u-p8-0"><div class="u-fs14-lh17">
   <b>[A수배]</b> KICS → 접수 → 지역경찰사건 → 우측상단 <b>기소중지사건접수</b> → 관서·사건번호 → 검색 → 목록에서 접수.<br>서류: <b>검거보고 · 확인서 · 신체확인서 · 체포/구속통지서</b>. 여러 건이면 <b>첫 건만 작성</b>하고 그 안에 전부 기록. 타기관은 <b>원본 발송·사본 보관</b>.<br>
   <b>[B수배]</b> 미란다 고지 후 형집행. 검찰청 <b>징수계 웹팩스</b>로 형집행장 수령. 납부하면 확인 후 귀가.<br>미납 시: 검거보고서 · 확인서 · 구인통지서(유치장이면 <b>신체확인서·입감지휘서</b>). ⚠️ <b>형집행장 교부확인서를 반드시 받는다.</b> 체포통지 원본은 <b>반송불가 도장</b> 후 체송.<br>
   <b>[C통보]</b> 현장에서 폴리폰 처리. 지명통보사실 통지서 2부 + 지명통보자발견보고 2부. 타기관은 전부 오프라인.<br>
   <b>[겹칠 때]</b> 여러 건 → 경찰 지명수배 1건만 / 현행범+A → 기소중지접수 후 인계종결 / 현행범+B → 검거보고서만 / <b>A+B → A서류에 B내용 포함</b>.<br>
   <span style="color:var(--text-dim)">⚠️ KICS 화면 흐름과 서류 목록은 <b>관서·시기별로 다를 수 있다</b> — 형사팀 확인 권장.</span>
  </div></div></details>
 </div>

 <div class="card" style="border:2px solid var(--accent-gold)">
  <div class="card-title">👨‍👩‍👧 여성청소년 — 스토킹 · 가폭 · 아동학대 · 청소년</div>
  <div class="info-box u-fs13">여청 사안은 <b>「지금 떼어놓느냐」</b>가 전부다. 죄명은 나중에 정리되지만 <b>분리를 놓치면 되돌릴 수 없다.</b></div>

  <details><summary style="font-weight:800;padding:6px 0">🏠 가정폭력 초동조치</summary><div class="u-p8-0">
   <div class="pg-f">
    <div class="pg-s pg-s1"><h6>📞 이런 신고다</h6><div>「옆집에서 계속 소리가 난다」 「남편이 때린다」 「아들이 아버지를 밀쳤다」. 신고자가 <b>당사자가 아닌 경우</b>가 절반이다.</div></div>
    <div class="pg-s pg-s2"><h6>🚗 도착해서 먼저</h6><div>① <b>문을 열게 하는 것이 첫 관문</b> — 현장조사 방해는 <b>과태료 대상</b>임을 고지<br>② <b>가해자·피해자를 물리적으로 분리</b>한 뒤 각각 따로 듣는다. 같은 방에서 물으면 진술이 안 나온다<br>③ <b>보이는 상처·깨진 물건을 먼저 촬영</b> — 정리되면 없어진다<br>④ <b>아이가 있는지 반드시 확인</b> — 아동학대가 같이 걸리는 경우가 많다</div></div>
    <div class="pg-s pg-s3"><h6>🔍 무엇으로 갈리나</h6><div>⚠️ <b>처벌의사와 관계없이</b> 발생보고 사안이면 <b>즉시 발생보고</b>다(가정보호사건도 적극 검토).
    <table class="mp-t">
     <tr><th>단계</th><th>내용</th></tr>
     <tr><td><b>응급조치</b></td><td>제지 → <b>가해자·피해자 분리</b> → 상담소·보호시설 인도 → 치료 필요 시 의료기관 → <b>임시조치 청구 가능성 통보</b> → 피해자보호명령·신변보호 고지</td></tr>
     <tr><td><b>긴급임시조치</b></td><td>통합판단조사표에 따라 진행. 현장은 폴리폰으로 <b>확인서·통지서</b>, <b>결정서는 사무실 KICS</b>. <b>퇴거·격리 불응 시 현행범 체포도 검토</b>(여청·팀장 상의)</td></tr>
     <tr><td><b>임시숙소</b></td><td>폴넷 → 케어포털 → 피해자 전담경찰관 업무지원시스템 → 임시숙소. <b>동의서는 체송</b></td></tr>
    </table></div></div>
    <div class="pg-s pg-s4"><h6>📮 어디로 넘긴다</h6><div>발생보고 → <b>여청계</b>. 긴급임시조치 결정서는 복귀 후 KICS.<br><span style="color:var(--text-dim)">⚠️ 긴급임시조치 서류 목록은 <b>여청계 확인 권장</b>.</span></div></div>
    <div class="pg-no">⚠️ <b>이것만은 하지 마라</b> — 「부부싸움이니 알아서 하시라」로 돌아서지 말 것. <b>처벌의사가 없어도 발생보고 사안이면 보고한다.</b> 재신고에서 사람이 죽는다.</div>
    <div class="pg-case"><b class="cs">사례</b> 피해자가 「신고 안 했다, 그냥 가시라」며 문을 닫으려 한 건. <b>가해자가 뒤에 서 있었다.</b> 분리 후 따로 물으니 진술이 완전히 달랐다. — <b>같은 공간에서 들은 말은 진술이 아니다.</b></div>
   </div>
  </div></details>

  <details><summary style="font-weight:800;padding:6px 0">🚷 스토킹</summary><div class="u-p8-0">
   <div class="pg-f">
    <div class="pg-s pg-s1"><h6>📞 이런 신고다</h6><div>「헤어진 사람이 집 앞에 와 있다」 「계속 전화·문자가 온다」 「직장까지 찾아온다」.</div></div>
    <div class="pg-s pg-s2"><h6>🚗 도착해서 먼저</h6><div>① <b>제지 · 중단 통보 · 서면경고</b> — 이 셋이 응급조치다<br>② <b>APO 시스템 확인 필수</b> — 이전 이력이 있으면 판단이 완전히 달라진다<br>③ 피해자에게 <b>상담·보호소</b> 안내<br>④ <b>가해자를 현장에서 그냥 돌려보내지 않는다</b> — 서면경고 기록을 남긴다</div></div>
    <div class="pg-s pg-s3"><h6>🔍 무엇으로 갈리나</h6><div>
    <table class="mp-t">
     <tr><th>조치</th><th>내용</th></tr>
     <tr><td><b>긴급응급조치</b><br>(지역경찰)</td><td><b>100m 이내 접근금지 · 전기통신 접근금지(1개월)</b>. 폴리폰으로 통보확인서 → <b>가해자 서명</b> → 수사서류 첨부 → 통보서 교부 → 상대방 통보. <b>서명을 못 받으면 문자 발송 후 기록 첨부</b>. 복귀 후 KICS로 <b>결정서</b></td></tr>
     <tr><td><b>잠정조치</b><br>(여청)</td><td>여청이 법원에 신청 — 서면경고 · 100m 접근금지 · <b>유치장 유치</b></td></tr>
    </table></div></div>
    <div class="pg-s pg-s4"><h6>📮 어디로 넘긴다</h6><div>사건발생보고 → <b>응급조치보고서(KICS)</b> → 여청계.<br>사건접수를 안 하면 <b>오프라인 서류를 여청계로 체송</b>한다.<br>👉 <b>범죄사실에는 ① 둘 사이의 관계 ② 몇 번 찾아왔는지</b>를 최대한 특정해 적는다. 횟수가 곧 죄질이다.</div></div>
    <div class="pg-case"><b class="cs">사례</b> 「그냥 얘기하러 왔다」는 전 연인. 단발성으로 보였으나 <b>APO 조회에서 3개월간 11회</b>가 나왔다. — <b>이 신고 하나만 보면 안 된다.</b> 조회가 판단을 바꾼다.</div>
   </div>
  </div></details>

  <details><summary style="font-weight:800;padding:6px 0">🧸 아동학대</summary><div class="u-p8-0">
   <div class="pg-f">
    <div class="pg-s pg-s1"><h6>📞 이런 신고다</h6><div>「윗집에서 아이 우는 소리가 계속 난다」 「아이 몸에 멍이 있다」(어린이집·병원 신고). <b>다른 사건으로 갔다가 발견</b>되는 경우도 많다.</div></div>
    <div class="pg-s pg-s2"><h6>🚗 도착해서 먼저</h6><div>① <b>신고이력·시간대역</b>과 <b>범죄피해자·안전조치 대상자 여부</b>를 먼저 조회<br>② 피해아동과 행위자의 <b>안전 확인</b><br>③ <b>분리된 공간</b>에서 아이가 자유롭게 말하도록 한다 — 보호자 앞에서는 아무 말도 안 나온다<br>④ 의심되면 <b>현장조사 체크리스트</b> 작성</div></div>
    <div class="pg-s pg-s3"><h6>🔍 무엇으로 갈리나</h6><div>⚠️ <b>다른 형사사건으로 접수됐더라도 아동학대 정황이 보이면 함께 확인한다.</b> 이것이 가장 많이 놓치는 지점이다.
    <table class="mp-t">
     <tr><th>확인</th><th>내용</th></tr>
     <tr><td><b>즉시 분리</b></td><td>재학대 위험이 있으면 응급조치. <b>망설이면 늦는다</b></td></tr>
     <tr><td><b>상흔·진술</b></td><td>보이는 상처는 촬영. 아이 진술은 <b>유도 없이</b> 그대로</td></tr>
     <tr><td><b>양육환경</b></td><td>방임도 학대다 — 위생·식사·등원 여부</td></tr>
    </table></div></div>
    <div class="pg-s pg-s4"><h6>📮 어디로 넘긴다</h6><div><b>서류</b> — 응급조치 서류 · <b>응급조치 결과보고서 즉시 작성·교부</b>(사유를 구체적으로 진술하도록 안내) · 긴급임시조치 서류<br><b>기록</b> — <b>112 신고출동보고</b> 작성 + 112 시스템에 조치내용·피해자 정보 입력<br>→ <b>여청계</b> 인계. 지자체 아동보호전문기관 연계.</div></div>
    <div class="pg-case"><b class="cs">사례</b> 층간소음 신고로 올라갔다가 아이 팔에 <b>오래된 멍이 여러 개</b>인 것을 봤다. 원 신고는 소음이었지만 <b>아동학대로 전환</b>해 보고했다. — <b>무슨 신고로 갔는지는 중요하지 않다.</b></div>
   </div>
  </div></details>

  <details><summary style="font-weight:800;padding:6px 0">🛏️ 미성년자 혼숙</summary><div class="u-p8-0">
   <div class="pg-f">
    <div class="pg-s pg-s1"><h6>📞 이런 신고다</h6><div>「딸이 모텔에 있는 것 같다」(보호자 신고) 「청소년이 성인과 들어갔다」(업소·행인 신고).</div></div>
    <div class="pg-s pg-s2"><h6>🚗 도착해서 먼저</h6><div>① 청소년의 <b>생년월일·현위치·안전</b> 확인<br>② 상대 남성 <b>인적사항과 연령차</b><br>③ 보호자 <b>신고 경위</b><br>④ <b>청소년 본인의 직접 진술</b> — 거부하면 <b>그 사유를 수사서류에 기재</b></div></div>
    <div class="pg-s pg-s3"><h6>🔍 무엇으로 갈리나</h6><div>
    <table class="mp-t">
     <tr><th>대상</th><th>확인할 것</th></tr>
     <tr><td><b>숙박업소</b></td><td>예약자·결제자·<b>실제 입실자</b> / 성인과 같이 들어갔는지 / 프런트가 봤는지 / <b>신분증 확인 여부</b> / <b>CCTV 동선</b></td></tr>
     <tr><td><b>성인 남성</b></td><td>관계 · <b>나이 인지 여부</b> · 만난 경위 · 숙박 목적 · <b>대가·술 제공·강요·협박·폭행·촬영</b> 여부</td></tr>
     <tr><td><b>증거</b></td><td>CCTV · 객실 시트 · 수건 등 <b>전부 보존</b></td></tr>
    </table></div></div>
    <div class="pg-s pg-s4"><h6>📮 어디로 넘긴다</h6><div>발생보고 → <b>여청계</b>. 대가·강요 정황이 있으면 성범죄로 전환 검토.<br>업주 책임(신분증 미확인)은 별도로 정리한다.</div></div>
    <div class="pg-no">⚠️ <b>영장 없이 객실을 수색하지 않는다.</b> 청소년이 현장에 있다고 확인될 때 <b>안전확인·진술청취 범위</b>에서만 출입을 검토하고, <b>단순 의심만으로는 안 된다.</b> 여기서 무리하면 사건 전체가 날아간다.</div>
   </div>
  </div></details>

  <details><summary style="font-weight:800;padding:6px 0">🧒 청소년 — 연령기준·보호자통지·사례</summary><div class="u-p8-0">
   <div class="pg-f">
    <div class="pg-s pg-s1"><h6>📞 이런 신고다</h6><div>「학생들이 술을 마신다」 「노래방에 청소년이 있다」 「킥보드를 중학생이 탄다」.</div></div>
    <div class="pg-s pg-s2"><h6>🚗 도착해서 먼저</h6><div>① <b>나이를 먼저 확정한다</b> — 여기서 처리 자체가 갈린다<br>② <b>보호자 또는 대체 보호자에게 연락</b>. 복리상 부적당하면 제외하되 <b>사유와 처리절차를 기록</b><br>③ 아이를 <b>여러 명 앞에서 훈계하지 않는다</b></div></div>
    <div class="pg-s pg-s3"><h6>🔍 무엇으로 갈리나</h6><div>
    <table class="mp-t">
     <tr><th>구분</th><th>연령</th></tr>
     <tr><td><b>범죄소년</b></td><td><b>14세 이상 19세 미만</b></td></tr>
     <tr><td><b>촉법소년</b></td><td><b>10세 이상 14세 미만</b></td></tr>
     <tr><td><b>우범소년</b></td><td><b>10세 이상 19세 미만</b> (비협조 시 채증하여 통보)</td></tr>
    </table>
    <b>현장 사례</b><br>· 숙박업소 음주 → <b>음주 사실만으로 업주 처벌은 곤란</b>. 혼숙 여부를 본다<br>· 유해약물 폐기 → 청소년보호법 근거<br>· <b>노래방 22시 이후 청소년실 출입 불가</b>(보호자 동반·출입동의서 등 예외 확인)<br>· <b>PM 운전 — 14세 이상은 범칙금, 그 미만은 보호자에게 과태료</b> 검토</div></div>
    <div class="pg-s pg-s4"><h6>📮 어디로 넘긴다</h6><div>촉법·우범은 <b>여청계</b>. 범죄소년은 사안에 따라 형사팀.<br><span style="color:var(--text-dim)">근거: 소년법·청소년보호법 <b>[항·호 미검증]</b> — 서류에 번호를 인용하기 전 원문 확인</span></div></div>
   </div>
  </div></details>
 </div>

 <div class="card" style="border:2px solid var(--accent-gold)">
  <div class="card-title">⚖️ 형사 — 절도 · 사기 · 풍속</div>
  <div class="info-box u-fs13">교통 외근이 <b>공동대응으로</b> 걸리는 사안들이다. 여기는 <b>「무엇을 확인하고 누구에게 넘기느냐」</b>만 적었다. 실제 처리는 해당 기능이 한다.</div>

  <details><summary style="font-weight:800;padding:6px 0">💳 신용카드 부정사용</summary><div class="u-p8-0">
   <div class="pg-f">
    <div class="pg-s pg-s1"><h6>📞 이런 신고다</h6><div>「카드를 잃어버렸는데 결제 문자가 온다」 「주운 카드를 썼다」 「통장에서 돈이 빠져나갔다」.</div></div>
    <div class="pg-s pg-s2"><h6>🚗 도착해서 먼저</h6><div>① <b>결제 문자·앱 내역을 그 자리에서 캡처</b> — 시각·가맹점·금액<br>② <b>카드사에 정지</b> 안내<br>③ 사용처가 특정되면 <b>가맹점 CCTV 보존</b> 요청 — 하루 이틀이면 덮인다</div></div>
    <div class="pg-s pg-s3"><h6>🔍 무엇으로 갈리나</h6><div><b>어디서 어떻게 썼는지로 죄명이 갈린다.</b>
    <table class="mp-t">
     <tr><th>사용 형태</th><th>죄명</th></tr>
     <tr><td>주워서 <b>반환 안 함</b></td><td>점유이탈물횡령</td></tr>
     <tr><td><b>가게에서 사용</b></td><td>가맹점주 상대 <b>사기</b> + 여신전문금융업법</td></tr>
     <tr><td><b>무인점포·키오스크·POS</b></td><td><b>컴퓨터등사용사기</b> + 여신전문금융업법</td></tr>
     <tr><td><b>ATM 현금인출</b></td><td><b>절도</b></td></tr>
     <tr><td><b>체크·현금카드</b></td><td>전자금융거래법 검토</td></tr>
    </table>
    👉 <b>근거 사진이 필수</b>다. 결제가 안 됐으면 <b>미수</b>도 검토.<br>
    <span style="color:var(--text-dim)">근거: 형법 §347 사기 · <b>§347의2 컴퓨터등 사용사기(2025.12.23 개정 — 20년 이하 징역 또는 5천만원 이하 벌금)</b> · §360 점유이탈물횡령(1년 이하 징역, 300만원 이하 벌금·과료) <b>[A등급]</b> / 여전법·전금법 <b>[항·호 미검증]</b>. 지역화폐는 전금법 검토</span></div></div>
    <div class="pg-s pg-s4"><h6>📮 어디로 넘긴다</h6><div>발생보고 → <b>형사팀</b>. 사용처가 여러 곳이면 <b>건별로 죄명이 달라진다</b>는 점을 보고서에 명시.</div></div>
    <div class="pg-case"><b class="cs">사례</b> 주운 카드로 <b>편의점 결제 3건 + ATM 인출 1건.</b> 앞은 사기, 뒤는 절도다. 한 죄명으로 뭉뚱그려 보고하면 뒤에서 전부 다시 짜야 한다.</div>
   </div>
  </div></details>

  <details><summary style="font-weight:800;padding:6px 0">🪪 신분증(주민증·면허증) 부정사용</summary><div class="u-p8-0">
   <div class="pg-f">
    <div class="pg-s pg-s1"><h6>📞 이런 신고다</h6><div>「남의 신분증으로 계약이 됐다」 「내 명의로 휴대폰이 개통됐다」. 교통에서는 <b>단속 중 면허증 제시</b>로 걸린다(맨 위 🚦카드 ②).</div></div>
    <div class="pg-s pg-s2"><h6>🚗 도착해서 먼저</h6><div><b>세 가지를 먼저 묻는다.</b><br>① 주민등록번호가 <b>본인확인</b>에 쓰였나<br>② 명의자 <b>본인처럼 행세</b>했나<br>③ 그 결과 <b>계약·계좌·대출·가입·송금</b>이 발생했나</div></div>
    <div class="pg-s pg-s3"><h6>🔍 무엇으로 갈리나</h6><div>👉 <b>단순 보관·전송보다 「무엇에 썼는가」가 핵심</b>이다.
    <table class="mp-t">
     <tr><th>제시한 것</th><th>운전면허증 / 주민등록증</th></tr>
     <tr><td><b>실물</b></td><td>공문서부정행사 / 주민등록법</td></tr>
     <tr><td><b>이미지 파일</b></td><td>공문서부정행사 <b>적용 곤란</b> / 주민등록법 별도 호</td></tr>
     <tr><td><b>공식 모바일</b></td><td>도교법 / 주민등록법</td></tr>
     <tr><td><b>조작 화면</b></td><td>전자기록 위·변조</td></tr>
     <tr><td><b>번호만</b></td><td>주민등록법(번호 부정사용)</td></tr>
     <tr><td><b>양도·대여</b></td><td>도교법 — <b>주는 쪽도 처벌</b></td></tr>
    </table>
    <span style="color:var(--text-dim)">근거: <b>형법 §230(공문서 등의 부정행사) — 2년 이하 징역·금고 또는 500만원 이하 벌금 [A등급]</b> / 주민등록법·도교법 <b>[항·호 미검증]</b></span></div></div>
    <div class="pg-s pg-s4"><h6>📮 어디로 넘긴다</h6><div>발생보고 → <b>형사팀</b>. 명의도용 피해자에게는 <b>엠세이퍼·PASS 명의도용방지</b> 안내.</div></div>
   </div>
  </div></details>

  <details><summary style="font-weight:800;padding:6px 0">🍚 무전취식</summary><div class="u-p8-0">
   <div class="pg-f">
    <div class="pg-s pg-s1"><h6>📞 이런 신고다</h6><div>「밥 먹고 돈을 안 낸다」 「술값을 안 내고 버틴다」. 심야 식당가에서 제일 많다.</div></div>
    <div class="pg-s pg-s2"><h6>🚗 도착해서 먼저</h6><div>① <b>인적사항 확보가 1순위</b> — 이게 안 되면 통고도 즉결도 못 간다<br>② <b>신고이력 확인이 필수</b> — 동종 이력이 있으면 그림이 완전히 달라진다<br>③ 술에 취해 있으면 <b>보호조치 요건</b>도 같이 본다</div></div>
    <div class="pg-s pg-s3"><h6>🔍 무엇으로 갈리나</h6><div>
    <table class="mp-t">
     <tr><th>상황</th><th>처리</th></tr>
     <tr><td>결제수단·잔고 <b>없음</b></td><td><b>사기</b> 검토</td></tr>
     <tr><td><b>소액</b>·연락처 교환 가능</td><td>통고처분 검토</td></tr>
     <tr><td><b>도주 우려·기망 정황</b></td><td><b>사기</b> 검토</td></tr>
     <tr><td><b>동종 신고이력</b></td><td>사기죄를 <b>적극</b> 검토</td></tr>
    </table>
    <span style="color:var(--text-dim)">근거(A등급): 경범죄처벌법 <b>§3①39호(무임승차 및 무전취식)</b> — 「영업용 차 또는 배 등을 타거나 다른 사람이 파는 음식을 먹고 정당한 이유 없이 제 값을 치르지 아니한 사람」 10만원 이하 벌금·구류·과료 / 형법 §347 사기</span></div></div>
    <div class="pg-s pg-s4"><h6>📮 어디로 넘긴다</h6><div>통고처분이면 폴리폰 경범단속. 거부하면 <b>즉결심판</b>(맨 위 🚦카드 ③).<br>사기로 가면 발생보고 → 형사팀. <b>변제는 민사 안내</b>.</div></div>
    <div class="pg-case"><b class="cs">사례</b> 「지갑을 두고 왔다」는 50대. 조회하니 <b>같은 상가에서만 4번째</b>였다. 한 건만 보면 통고, 이력을 보면 사기다. — <b>조회가 죄명을 바꾼다.</b></div>
   </div>
  </div></details>

  <details><summary style="font-weight:800;padding:6px 0">🚕 택시비 시비</summary><div class="u-p8-0">
   <div class="pg-f">
    <div class="pg-s pg-s1"><h6>📞 이런 신고다</h6><div>「손님이 요금을 안 낸다」 「기사가 중간에 내리라고 한다」 「요금이 너무 많이 나왔다」 「손님이 토했다」.</div></div>
    <div class="pg-s pg-s2"><h6>🚗 도착해서 먼저</h6><div>① <b>차를 안전한 곳으로</b> — 도로 한복판에서 시비를 정리하지 않는다<br>② <b>승객 인적사항을 먼저 확보</b>. 요금 얘기는 그 다음<br>③ 요금 지불을 <b>재차 권유</b>한다 — 대부분 여기서 끝난다</div></div>
    <div class="pg-s pg-s3"><h6>🔍 무엇으로 갈리나</h6><div>
    <table class="mp-t">
     <tr><th>상황</th><th>처리</th></tr>
     <tr><td><b>기사가 중도 하차 요구</b></td><td>사유가 있으면 <b>이용한 구간 요금은 지급</b>해야 한다</td></tr>
     <tr><td><b>지금 돈이 없다</b></td><td>연락처 교환 후 익일 처리, 안 되면 <b>사기 발생보고</b></td></tr>
     <tr><td><b>요금이 많이 나왔다</b></td><td>우선 결제 유도 후 <b>지자체 교통과 민원</b> 안내</td></tr>
     <tr><td><b>구토</b></td><td>손해배상은 <b>민사</b></td></tr>
    </table>
    👉 비슷한 신고 이력이 있으면 <b>사기 발생보고</b>.</div></div>
    <div class="pg-s pg-s4"><h6>📮 어디로 넘긴다</h6><div>대부분 <b>현장 종결</b>. 사기 정황이면 발생보고 → 형사팀. 요금 다툼은 <b>지자체 교통과</b>, 손해배상은 <b>민사</b>.</div></div>
   </div>
  </div></details>

  <details><summary style="font-weight:800;padding:6px 0">👟 신발절도</summary><div class="u-p8-0">
   <div class="pg-f">
    <div class="pg-s pg-s1"><h6>📞 이런 신고다</h6><div>「식당에 벗어둔 신발이 없어졌다」 「누가 내 신발을 신고 갔다」.</div></div>
    <div class="pg-s pg-s2"><h6>🚗 도착해서 먼저</h6><div>① <b>남아 있는 신발</b>이 있는지 확인 — 바꿔 신은 것이면 절도가 아니다<br>② <b>CCTV 유무</b>를 업주에게 먼저 묻는다</div></div>
    <div class="pg-s pg-s3"><h6>🔍 무엇으로 갈리나</h6><div><b>고의</b>로 가져갔으면 <b>절도</b>, <b>실수</b>면 반환·손해배상 문제다.<br>지역경찰 단계에서 판단이 어려우면 <b>발생보고</b>로 넘긴다.<br>식당의 보관·관리 책임은 <b>민사</b>로 안내.<br><span style="color:var(--text-dim)">근거(A등급): 형법 §329 절도</span></div></div>
    <div class="pg-s pg-s4"><h6>📮 어디로 넘긴다</h6><div>고의가 보이면 발생보고 → 형사팀. 착오면 <b>민사 안내로 종결</b>.</div></div>
   </div>
  </div></details>

  <details><summary style="font-weight:800;padding:6px 0">🎰 게임장(사행성)</summary><div class="u-p8-0">
   <div class="pg-f">
    <div class="pg-s pg-s1"><h6>📞 이런 신고다</h6><div>「불법 게임장이 있다」 「환전을 해준다」. 첩보성 신고가 많다.</div></div>
    <div class="pg-s pg-s2"><h6>🚗 도착해서 먼저</h6><div>① <b>영업 중인 상태를 먼저 채증</b> — 전원이 꺼지면 입증이 어려워진다<br>② <b>출입구를 먼저</b> 확보<br>③ 게임 종류는 <b>게임물관리위원회 홈페이지 「게임찾기」</b>에서 검색</div></div>
    <div class="pg-s pg-s3"><h6>🔍 무엇으로 갈리나</h6><div>
    <table class="mp-t">
     <tr><th>상황</th><th>적용</th></tr>
     <tr><td><b>사행성 게임물</b><br>(바다이야기·야마토·오션파라다이스·에이스경마)</td><td>게임산업법이 아니라 <b>사행행위규제법</b> 검토. 단 <b>환전행위</b>는 게임산업법</td></tr>
     <tr><td><b>전원이 꺼져 있음</b></td><td><b>진열·보관행위</b>로 검토 후 발생보고</td></tr>
     <tr><td><b>점수보관증·무기명 카드</b></td><td>게임산업법 위반 검토. <b>단순 점수보관</b>은 행정처분(지자체 통보)</td></tr>
    </table></div></div>
    <div class="pg-s pg-s4"><h6>📮 어디로 넘긴다</h6><div>발생보고 → <b>형사팀</b>. 행정처분 사안은 <b>지자체 통보</b>.<br>⚠️ <b>미단속 보고도 누락하지 말 것.</b> 안 잡았다는 기록이 다음 단속의 근거가 된다.</div></div>
   </div>
  </div></details>

  <details><summary style="font-weight:800;padding:6px 0">🎤 노래방·단란·유흥 구분</summary><div class="u-p8-0">
   <div class="pg-f">
    <div class="pg-s pg-s1"><h6>📞 이런 신고다</h6><div>「일반음식점에서 노래를 부른다」 「접대부가 있다」 「영업정지 중인데 문을 열었다」.</div></div>
    <div class="pg-s pg-s2"><h6>🚗 도착해서 먼저</h6><div><b>정의부터 갈린다.</b><br>· <b>노래방</b> = 연주자 없이 기계<br>· <b>단란주점</b> = 주류 판매 + 손님 노래<br>· <b>유흥주점</b> = 주류 + <b>유흥종사자</b> + 노래·춤<br>👉 <b>업종 허가와 실제 영업형태가 다른 것</b>이 핵심이다.</div></div>
    <div class="pg-s pg-s3"><h6>🔍 무엇으로 갈리나</h6><div><b>접수해야 하는 것</b><br>· 무허가·영업정지 중 영업<br>· <b>일반음식점에 노래방기기</b> 설치·사용<br>· 7080 라이브에서 손님 연주<br>· 단란에서 유흥 형태<br>· 일반식당의 단란·유흥 영업·접대부 고용<br>· <b>동석작배·접객행위·알선</b><br>· 노래방에서 접대부 발견<br><span style="color:var(--text-dim)">근거(항·호 미검증): 식품위생법 · 음악산업법 — 서류에 번호를 인용하기 전 원문 확인</span></div></div>
    <div class="pg-s pg-s4"><h6>📮 어디로 넘긴다</h6><div>발생보고 → <b>형사팀(생활질서)</b>. 행정처분 병행이면 <b>지자체 위생과</b> 통보.</div></div>
   </div>
  </div></details>

  <details><summary style="font-weight:800;padding:6px 0">🃏 홀덤펍</summary><div class="u-p8-0">
   <div class="pg-f">
    <div class="pg-s pg-s1"><h6>📞 이런 신고다</h6><div>「홀덤펍에서 도박을 한다」 「칩을 술로 바꿔준다」.</div></div>
    <div class="pg-s pg-s2"><h6>🚗 도착해서 먼저</h6><div><b>입증 포인트 2개만 본다.</b><br>① 업주가 <b>입장료·참가비·주류 주문액</b>에 따라 게임 기회를 줬는가<br>② 손님이 낸 돈이 <b>경품 재원</b>이 되는가<br>👉 <b>증거·입증이 전부다.</b> 칩·정산표·안내문을 먼저 확보.</div></div>
    <div class="pg-s pg-s3"><h6>🔍 무엇으로 갈리나</h6><div><b>칩의 환금성</b>이 쟁점이다.
    <table class="mp-t">
     <tr><th>형태</th><th>검토</th></tr>
     <tr><td>1만원 받고 참여권·칩·주류 제공 후 우승자에게 양주</td><td><b>도박</b> 검토</td></tr>
     <tr><td>순위에 따라 <b>시드권</b> 지급 → 칩 교환·개인간 교환</td><td><b>도박</b> 검토</td></tr>
     <tr><td><b>칩을 맥주로 교환</b></td><td>재산상 가치 인정 → <b>도박</b> 검토</td></tr>
    </table>
    👉 <b>돈 내고 참가</b>하거나 <b>결과물을 재산으로 교환</b>할 수 있으면 도박개장·도박죄 발생보고 검토.</div></div>
    <div class="pg-s pg-s4"><h6>📮 어디로 넘긴다</h6><div>발생보고 → <b>형사팀</b>.</div></div>
   </div>
  </div></details>
 </div>
'''
